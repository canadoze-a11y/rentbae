import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURE THE BRAIN
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# The "Twin-Verify" System Prompt
SYSTEM_PROMPT = """
You are an Expert Fraud Analyst for a student housing platform. 
Your goal is to protect international students from rental scams.

Analyze the provided text or images (rental ad, lease, chat history) for these RED FLAGS:
1. Price is too good to be true (e.g., $500 for a 2-bedroom in Toronto).
2. Landlord claims to be "out of the country" or "missionary".
3. Requests for wire transfer / Western Union / Cash before signing.
4. Poor grammar or excessive urgency ("Must decide now").
5. The text looks like a standard "scam script" used on Facebook Marketplace.
6. Inconsistencies between images (e.g. view out window doesn't match location).

OUTPUT FORMAT:
- RISK LEVEL: [LOW / MEDIUM / HIGH / CRITICAL]
- SCORE: [0-100% Risk]
- EXPLANATION: Bullet points citing specific suspicious parts of the input.
- ADVICE: One sentence on what the student should do next (e.g., "Do not pay. Ask for a video tour.")
"""

def analyze_content(content_list):
    # Using the exact working model
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    # We construct the request with the prompt first, then all the user's images/text
    full_request = [SYSTEM_PROMPT] + content_list
    response = model.generate_content(full_request)
    return response.text

# 2. THE WEBSITE FRONTEND
st.set_page_config(page_title="RentBae Lease Verifier", page_icon="🛡️")

# Clean Header
col1, col2 = st.columns([1, 5])
with col1:
    st.write("🛡️") 
with col2:
    st.title("RentBae Lease Verifier")

st.markdown("### Stop Getting Scammed. Check before you pay.")
st.caption("Powered by Canadoze & Gemini AI")
st.markdown("---")

# Input Section
option = st.radio("What do you want to check?", ["Paste Text of Ad", "Upload Screenshots/Lease (Max 4)"])

user_content = [] # This will hold the data we send to AI

if option == "Paste Text of Ad":
    text_input = st.text_area("Paste the landlord's message or ad description here:", height=150)
    if text_input:
        user_content.append(text_input)
else:
    # UPDATED: accept_multiple_files=True
    uploaded_files = st.file_uploader(
        "Upload screenshots of the chat, lease, or house (PNG/JPG)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Limit to 4 images to prevent crashing/slowness
        if len(uploaded_files) > 4:
            st.warning("⚠️ Maximum 4 images allowed. Only the first 4 will be analyzed.")
            uploaded_files = uploaded_files[:4]
            
        # Display images in a row
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            image = Image.open(file)
            user_content.append(image) # Add to analysis list
            with cols[idx]:
                st.image(image, caption=f"Image {idx+1}", use_column_width=True)

# The "Check Now" Button
if st.button("Analyze for Scams", type="primary"):
    if user_content:
        with st.spinner("🕵️ Agent is analyzing all evidence for red flags..."):
            try:
                result = analyze_content(user_content)
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(result)
                st.info("NOTE: This is AI advice, not legal advice. If you are unsure, never send money.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please provide some text or upload an image first.")

# 3. PROFESSIONAL FOOTER
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        <p>
            <a href='https://rentbae.io' target='_blank' style='text-decoration: none; color: #FF4B4B; font-weight: bold;'>Find Verified Rooms on RentBae.io</a> 
            | 
            <a href='https://instagram.com/canadoze' target='_blank' style='text-decoration: none; color: grey;'>Follow Canadoze</a>
        </p>
        <p style='font-size: 12px;'>© 2025 RentBae. Built for Students.</p>
    </div>
    """,
    unsafe_allow_html=True
)
