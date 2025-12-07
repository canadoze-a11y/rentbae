import streamlit as st
import google.generativeai as genai

# 1. SETUP
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("🔍 Gemini Model Scanner")
st.write("This tool will ask Google which models your API key can actually use.")

if st.button("Scan for Available Models"):
    try:
        found_any = False
        st.write("---")
        # List all models
        for m in genai.list_models():
            # We only care about models that can generate content (chat/text)
            if 'generateContent' in m.supported_generation_methods:
                st.success(f"✅ AVAILABLE: {m.name}")
                found_any = True
        
        if not found_any:
            st.error("No models found. Your API Key might be invalid or have no quota.")
            
    except Exception as e:
        st.error(f"Error scanning: {e}")
