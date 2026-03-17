import streamlit as st
import google.generativeai as genai

# הגדרות דף
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>.main { direction: RTL; text-align: right; }</style>""", unsafe_allow_html=True)

# הגדרת המפתח
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # נשתמש במודל 1.5-flash כי הוא הכי יציב ב-SDK
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף כשר - ניסיון אחרון")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים...")

if st.button("נסה לייצר מתכון"):
    if not api_key:
        st.error("חסר מפתח API!")
    elif ingredients:
        try:
            with st.spinner('השף מנסה גישה רשמית...'):
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("זה עבד!")
                st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("גוגל עדיין מזהה עומס. יכול להיות שהמפתח זקוק להפסקה ארוכה יותר או שמדובר במגבלה של Streamlit.")
            else:
                st.error(f"שגיאה חדשה: {e}")
