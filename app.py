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

# הגדרות דף ועיצוב
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
add_analytics("4WZTVRVRHX")

st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכולית כשר")
st.subheader("הכנס מצרכים וקבל מתכון טעים")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: בשר בקר, בצל, יין אדום...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף שוקד על המתכון עבורך...'):
            # המפתח החדש שסיפקת
            api_key = "AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M"
            
            # ניסיון דרך מספר נתיבים כדי למנוע שגיאות 404
            urls = [
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            ]
            
            data = {
                "contents": [{"parts": [{"text": f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. הקפד על הוראות הכנה ברורות."}]}]
            }
            
            success = False
            for url in urls:
                try:
                    response = requests.post(url, json=data, timeout=10)
                    if response.status_code == 200:
                        result = response.json()
                        recipe_text = result['candidates'][0]['content']['parts'][0]['text']
                        st.success("הנה המתכון שמצאתי:")
                        st.write(recipe_text)
                        success = True
                        break
                except Exception:
                    continue
            
            if not success:
                st.error("חל עיכוב קטן בחיבור לשרת. אנא נסה ללחוץ שוב על הכפתור בעוד רגע.")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
