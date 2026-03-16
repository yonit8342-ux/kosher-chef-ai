import streamlit as st
import google.generativeai as genai

# הגדרת המפתח
genai.configure(api_key="AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY")

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש במטבח?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מכין את המתכון...'):
            try:
                # יצירת המודל בצורה המעודכנת ביותר
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                response = model.generate_content(f"צור מתכון כשר ופשוט בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
