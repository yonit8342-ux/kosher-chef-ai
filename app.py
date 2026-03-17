import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# פונקציית Google Analytics (אנטילקס)
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

# הגדרות דף ועיצוב RTL
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
add_analytics("4WZTVRVRHX")

st.markdown("""
    <style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# הגדרת ה-API הרשמי עם המפתח שלך
genai.configure(api_key="AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בשר, תפוחי אדמה, פטריות...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מחשב את המרכיבים...'):
            try:
                # שימוש במודל 1.5 פלאש דרך ה-SDK (מונע שגיאות URL)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("המתכון מוכן!")
                    st.write(response.text)
            except Exception as e:
                # ניסיון גיבוי עם מודל Pro אם פלאש לא זמין
                try:
                    model_pro = genai.GenerativeModel('gemini-pro')
                    response_pro = model_pro.generate_content(f"מתכון כשר עבור: {ingredients}")
                    st.write(response_pro.text)
                except Exception as final_error:
                    st.error("לא ניתן להתחבר למודל. אנא וודא שהמפתח פעיל ב-Google AI Studio.")
                    st.code(str(final_error))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
