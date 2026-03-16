import streamlit as st
import google.generativeai as genai

# 1. הגדרת מפתח ה-API
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף ועיצוב RTL (יישור לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL; 
        text-align: right;
    }
    input { 
        direction: RTL !important; 
        text-align: right !important; 
    }
    div.stButton > button { 
        width: 100%; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ממשק משתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הכניסו את המצרכים שיש לכם בבית וקבלו מתכון פשוט וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: חזה עוף, פתיתים, בצל...")

# 4. לוגיקה
if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף בודק בספר המתכונים...'):
            try:
                # שימוש במודל 1.5-flash היציב
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # הנחיה ברורה למודל
                prompt = f"אתה שף מומחה. כתוב מתכון כשר, ברור ופשוט בעברית המבוסס על המצרכים הבאים: {ingredients}. כלול רשימת רכיבים והוראות הכנה."
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שמצאתי:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("לא התקבל תוכן מהשרת. נסה שוב.")
                    
            except Exception as e:
                # טיפול בשגיאות בצורה ברורה
                st.error("חלה שגיאה בחיבור למודל.")
                if "404" in str(e):
                    st.warning("נראה שהשרת עדיין מנסה להשתמש בגרסה ישנה. וודא שביצעת Reboot לאפליקציה.")
                st.caption(f"פרטי השגיאה: {str(e)}")
    else:
        st.warning("אנא הזן לפחות מצרך אחד.")

# הערת סיום
st.markdown("---")
st.caption("שימו לב: יש לוודא את כשרות וטריות המוצרים לפני הבישול.")
