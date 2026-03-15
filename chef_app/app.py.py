import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. הגדרת המפתח שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. עיצוב RTL
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL;
        text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("הזינו מצרכים והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, תפוחי אדמה, סילאן...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף מתחבר לשרת היציב...'):
            try:
                # התיקון הקריטי: הכרחת הקוד להשתמש בגרסה v1 ולא ב-v1beta שגורמת לשגיאה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"צור מתכון כשר, פשוט וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כתוב את המתכון עם רשימת מצרכים מסודרת והוראות הכנה ברורות."
                
                # שימוש ב-RequestOptions כדי לעקוף את שגיאת ה-404
                response = model.generate_content(
                    prompt,
                    request_options=RequestOptions(api_version='v1')
                )
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
                
            except Exception as e:
                st.error("שגיאת התחברות.")
                if "404" in str(e):
                    st.warning("גוגל עדיין מפנה אותך לגרסה ישנה. נסה ללחוץ שוב על הכפתור בעוד רגע.")
                else:
                    st.caption(f"פרטים: {str(e)}")
    else:
        st.warning("נא להזין מצרכים.")
