import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Google Analytics
def add_analytics(tag_id="4WZTVRVRHX"):
    script = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={tag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{tag_id}');
        </script>
    """
    components.html(script, height=0)

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
add_analytics()

# עיצוב RTL והצמדה לימין
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# המפתח החדש שלך
genai.configure(api_key="AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M")

st.title("🍲 שף בינה מלאכולית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, דבש, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.write(response.text)
            except Exception as e:
                st.error("שגיאה בחיבור. וודא שהמפתח הוכנס נכון.")
                st.code(str(e))
