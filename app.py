import streamlit as st
import google.generativeai as genai

# הגדרות דף
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL (יישור לימין)
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# אתחול ה-API
try:
    # משיכת המפתח מה-Secrets
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    
    # התיקון לשגיאת ה-404: הגדרת מודל ספציפי ויציב
    model = genai.GenerativeModel('gemini-1.5-flash')
    
except Exception as e:
    st.error("שגיאה בהגדרת המפתח. וודא שקיים GEMINI_KEY ב-Secrets של Streamlit.")
    st.stop()

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בשר, תפוחי אדמה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון...'):
            try:
                # הנחיה ברורה למודל
                prompt = f"כתוב מתכון כשר וטעים בעברית עבור המצרכים הבאים: {ingredients}"
                
                # יצירת התוכן
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("חלה שגיאה בחיבור למודל.")
                st.code(str(e))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
