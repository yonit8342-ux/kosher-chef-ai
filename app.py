import streamlit as st
import google.generativeai as genai

# הגדרות דף
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# חיבור למפתח מה-Secrets
try:
    # כאן הקוד מחפש את השם המדויק שהגדרת בשלב 2
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("שגיאה: המפתח 'GEMINI_KEY' לא נמצא ב-Secrets של Streamlit.")
    st.stop()

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בשר, סילאן, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון...'):
            try:
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error("חלה שגיאה בחיבור. וודא שהמפתח ב-Secrets תקין ולא 'דלף' לגיטהאב.")
