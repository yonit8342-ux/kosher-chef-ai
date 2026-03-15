import streamlit as st
import google.generativeai as genai

# הגדרת המפתח
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# עיצוב RTL
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")
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
        with st.spinner('מתחבר לשרת...'):
            try:
                # שימוש בגרסה יציבה בלבד
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"צור מתכון כשר ופשוט בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error("השגיאה עדיין מופיעה? וודא שקובץ ה-requirements.txt נמצא בתיקייה הראשית.")
                st.caption(f"פרטים: {str(e)}")
