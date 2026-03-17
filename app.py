import streamlit as st
import google.generativeai as genai

# הגדרות RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; }
</style>""", unsafe_allow_html=True)

# בדיקה אם המפתח קיים ב-Secrets
if "GEMINI_KEY" not in st.secrets:
    st.error("שגיאה: GEMINI_KEY חסר ב-Secrets של Streamlit!")
    st.stop()

# הגדרת המודל
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בקר, בצל, תפוחי אדמה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מכין מתכון...'):
            try:
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error("חלה שגיאה בחיבור. וודא שהמפתח ב-Secrets תקין ולא נחסם.")
                st.info("אם מופיע 403, המפתח דלף לגיטהאב. עליך ליצור חדש ולהחליף ב-Secrets.")
