import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURE THE BRAIN
# We access the API key from Streamlit's secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# The "Twin-Verify" System Prompt
SYSTEM_PROMPT = """
You are an Expert Fraud Analyst for a student housing platform. 
Your goal is to protect international students from rental scams.

Analyze the provided text or image (rental ad/lease) for these RED FLAGS:
1. Price is too good to be true (e.g., $500 for a 2-bedroom in Toronto).
2. Landlord claims to be "out of the country" or "missionary".
3. Requests for wire transfer / Western Union / Cash before signing.
4. Poor grammar or excessive urgency ("Must decide now").
5. The text looks like a standard "scam script" used on Facebook Marketplace.

OUTPUT FORMAT:
- RISK LEVEL: [LOW / MEDIUM / HIGH / CRITICAL]
- SCORE: [0-100% Risk]
- EXPLANATION: Bullet points citing specific suspicious parts of the input.
- ADVICE: One sentence on what the student should do next (e.g., "Do not pay. Ask for a video tour.")
"""

def analyze_content(content):
    # Using the exact model name we found in your scan
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content([SYSTEM_PROMPT, content])
    return response.text

# 2. THE WEBSITE FRONTEND
st.set_page_config(page_title="RentBae Lease Verifier", page_icon="🛡️")

st.title("🛡️ RentBae Lease Verifier")
st.markdown("### Stop Getting Scammed. Check before you pay.")
st.caption("Powered by Canadoze & Gemini AI")

# Input Section
option = st.radio("What do you want to check?", ["Paste Text of Ad", "Upload Screenshot/Lease"])

user_input = None
if option == "Paste Text of Ad":
    user_input = st.text_area("Paste the landlord's message or ad description here:")
else:
    uploaded_file = st.file_uploader("Upload a screenshot of the chat or lease (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        user_input = Image.open(uploaded_file)
        st.image(user_input, caption="Uploaded Image", use_column_width=True)

# The "Check Now" Button
if st.button("Analyze for Scams"):
    if user_input:
        with st.spinner("🕵️ Agent is analyzing for red flags..."):
            try:
                result = analyze_content(user_input)
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(result)
                st.info("NOTE: This is AI advice, not legal advice. If you are unsure, never send money.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please provide some text or an image first.")

# Footer to drive traffic back to your main site
st.markdown("---")
st.markdown("[Find Verified Rooms on RentBae.com](https://rentbae.com) | [Follow Canadoze](https://instagram.com/canadoze)")
