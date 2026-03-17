import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# הגדרת המפתח ועקיפת בעיית ה-Beta
genai.configure(api_key="AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY", transport='rest')

# הוספת Analytics (המזהה שלך)
def add_analytics(tag_id):
    if not tag_id.startswith("G-"): tag_id = f"G-{tag_id}"
    script = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={tag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date()); gtag('config', '{tag_id}');
        </script>
    """
    components.html(script, height=0)

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
add_analytics("4WZTVRVRHX")

# עיצוב RTL
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: בשר, תפוחי אדמה, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מכין את המתכון...'):
            try:
                # שימוש במודל הפרו היציב ביותר
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה בחיבור: {str(e)}")
