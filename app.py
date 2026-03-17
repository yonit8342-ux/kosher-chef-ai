import streamlit as st
import requests
import streamlit.components.v1 as components

# פונקציית Google Analytics
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

st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: דג סלמון, לימון, שום...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מחשב מסלול מחדש...'):
            api_key = "AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M"
            
            # ניסיון אחרון עם פורמט ה-URL המדויק ביותר ל-2026
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            
            data = {
                "contents": [{"parts": [{"text": f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור המצרכים הבאים: {ingredients}"}]}]
            }
            
            try:
                response = requests.post(url, json=data, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    recipe_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון שמצאתי:")
                    st.write(recipe_text)
                else:
                    # אם עדיין יש 404, ננסה מודל שתמיד זמין
                    url_fallback = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                    response_fb = requests.post(url_fallback, json=data, timeout=15)
                    if response_fb.status_code == 200:
                        st.write(response_fb.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"שגיאה {response_fb.status_code}: המודל לא מגיב. בדוק אם ה-API Key פעיל ב-AI Studio.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
