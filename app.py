import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# הגדרת ה-API
try:
    # וודא שהמפתח ב-Secrets תקין ושמו GEMINI_KEY
    api_key = st.secrets.get("GEMINI_KEY", "כאן_שמים_מפתח_חדש_רק_לבדיקה")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"שגיאה בהגדרת המפתח: {e}")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: חזה עוף, בצל, סילאן...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון...'):
            try:
                # התיקון: ה-request_options נשלח בנפרד מה-config
                response = model.generate_content(
                    f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}",
                    request_options={"timeout": 600} # הגדרת זמן המתנה ארוך יותר
                )
                
                if response.text:
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                if "403" in str(e) or "API_KEY_INVALID" in str(e):
                    st.error("המפתח נחסם או אינו תקין. יש להחליף מפתח ב-Secrets.")
                else:
                    st.error("חלה שגיאה בחיבור.")
                    st.code(str(e))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
