import streamlit as st
import google.generativeai as genai

# הגדרות עיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; height: 3em; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# המפתח החדש שיצרת - שים אותו כאן בין המירכאות
# וודא שזה מפתח חדש לגמרי מ-AI Studio!
MY_KEY = "הכנס_כאן_מפתח_חדש_לגמרי"

if MY_KEY == "AIzaSyBJu0xP78jqt3P_CwFFfR3v7_cE0B3A6zw":
    st.warning("עליך להכניס את המפתח החדש בקוד כדי שזה יעבוד.")
    st.stop()

genai.configure(api_key=MY_KEY)

st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים וקבלו מתכון כשר ברגע:")

ingredients = st.text_input("מה נבשל?", placeholder="למשל: עוף, בצל, דבש...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('מכין מתכון...'):
            try:
                # ניסיון שימוש במודל יציב
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("החיבור נכשל. כנראה שהמפתח נחסם שוב.")
                st.info("אם זה קורה, הפתרון היחיד הוא לעשות Reboot לאפליקציה בלוח הבקרה של Streamlit.")
