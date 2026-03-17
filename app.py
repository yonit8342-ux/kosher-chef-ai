import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# הגדרת המפתח - המערכת עכשיו תשתמש בגרסה היציבה אוטומטית
genai.configure(api_key="AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY")

# הוספת Google Analytics
def add_analytics(tag_id):
    if not tag_id.startswith("G-"): tag_id = f"G-{tag_id}"
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
add_analytics("4WZTVRVRHX")

# עיצוב RTL
st.markdown("""
    <style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, בצל, תפוחי אדמה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון טעים...'):
            try:
                # עכשיו כשהספרייה מעודכנת, 1.5 פלאש יעבוד מצוין
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"צור מתכון כשר וטעים בעברית עבור המצרכים: {ingredients}")
                st.success("הנה המתכון שמצאתי:")
                st.write(response.text)
            except Exception as e:
                st.error(f"חלה שגיאה: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
