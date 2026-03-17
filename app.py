import streamlit as st
import google.generativeai as genai

# הגדרת ה-API
genai.configure(api_key="AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY")

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# יישור לימין
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש במטבח?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מכין מתכון...'):
            try:
                # שימוש במודל 1.5 פלאש - בגרסת פייתון 3.11 זה יעבוד תקין
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
