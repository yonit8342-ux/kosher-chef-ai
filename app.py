import streamlit as st
import google.generativeai as genai

# הגדרות דף ועיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# אתחול ה-API
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    
    # התיקון הסופי: הוספת "models/" לפני שם המודל
    # זה מכריח את ה-API להשתמש בנתיב הנכון
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
except Exception as e:
    st.error("שגיאה בהגדרת המפתח. וודא שקיים GEMINI_KEY ב-Secrets.")
    st.stop()

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, אורז...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון...'):
            try:
                # יצירת התוכן
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("חלה שגיאה בחיבור.")
                # הדפסת השגיאה המדויקת כדי שנדע אם זה שוב 404
                st.code(str(e))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
