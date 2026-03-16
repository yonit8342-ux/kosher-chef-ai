import streamlit as st
import google.generativeai as genai

# הגדרת המפתח
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# עיצוב RTL
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, עוף...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף חושב...'):
            try:
                model = genai.GenerativeModel('gemini-flash')
                prompt = f"אתה שף מומחה. צור מתכון כשר, ברור וטעים בעברית עבור: {ingredients}"
                response = model.generate_content(prompt)
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
