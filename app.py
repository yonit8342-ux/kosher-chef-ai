import streamlit as st
import google.generativeai as genai

# 1. הגדרות דף ועיצוב לממשק בעברית (RTL)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.markdown("""
    <style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { 
        width: 100%; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold; 
        height: 3em;
        border-radius: 10px;
    }
    .stMarkdown { direction: RTL; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. חיבור ל-API של Gemini בצורה מאובטחת
try:
    # הקוד מושך את המפתח מה-Secrets של Streamlit Cloud
    if "GEMINI_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=api_key)
        
        # שימוש במודל יציב למניעת שגיאת 404
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("שגיאה: המפתח 'GEMINI_KEY' לא נמצא ב-Secrets של Streamlit.")
        st.stop()
except Exception as e:
    st.error(f"חלה שגיאה בהגדרת המערכת: {e}")
    st.stop()

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו את המצרכים שיש לכם בבית, והשף יבנה לכם מתכון כשר וטעים!")

ingredients = st.text_input("מה המצרכים שלך?", placeholder="למשל: עוף, תפוחי אדמה, סילאן...")

if st.button("צור מתכון כשר עכשיו"):
    if ingredients:
        with st.spinner('השף שוקד על המתכון...'):
            try:
                # יצירת המתכון עם הגדרות זמן המתנה נכונות
                prompt = f"אתה שף מומחה לכשרות. כתוב מתכון כשר, ברור וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}"
                
                response = model.generate_content(
                    prompt,
                    request_options={"timeout": 600}
                )
                
                if response.text:
                    st.success("הנה המתכון שמצאתי עבורך:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f0f2f6; padding: 20px; border-radius: 10px;">{response.text}</div>', unsafe_allow_html=True)
                else:
                    st.warning("השף לא הצליח לגבש מתכון. נסה לשנות את רשימת המצרכים.")
                    
            except Exception as e:
                st.error("חלה שגיאה בחיבור לבינה המלאכותית.")
                if "403" in str(e) or "API_KEY_INVALID" in str(e):
                    st.info("נראה שמפתח ה-API נחסם או שאינו תקין. יש להחליף אותו ב-Secrets.")
                else:
                    st.code(str(e))
    else:
        st.warning("בבקשה הזינו לפחות מצרך אחד כדי שנוכל להתחיל.")

# הערה לניהול גרסאות
st.sidebar.markdown("---")
st.sidebar.write("גרסה: 1.2 (יציבה)")
st.sidebar.info("פותח עבור פרויקט שף כשר AI")
