import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. עיצוב יישור לימין (RTL)
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL;
        text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("הזינו מצרכים והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, בצל, עוף...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף בודק את המזווה...'):
            try:
                # התיקון: שימוש בשם המודל בלבד ללא קידומות שגורמות לשגיאות גרסה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"צור מתכון כשר, פשוט וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כתוב את המתכון עם רשימת מצרכים מסודרת והוראות הכנה ברורות."
                
                # יצירת התוכן
                response = model.generate_content(prompt)
                
                if response and response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("השרת לא החזיר תשובה. נסו שוב בעוד רגע.")
                
            except Exception as e:
                st.error("השף נתקל בבעיה טכנית.")
                # מציג את השגיאה בקטן כדי שנדע מה קרה אם זה עדיין לא עובד
                st.caption(f"פרטי שגיאה: {str(e)}")
    else:
        st.warning("נא להזין מצרכים.")

st.markdown("---")
st.caption("השף הדיגיטלי | גרסה יציבה")
