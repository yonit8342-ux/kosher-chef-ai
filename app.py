import streamlit as st
import requests
import streamlit.components.v1 as components

# Google Analytics
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
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, תפוחי אדמה, פטריות...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון טעים...'):
            api_key = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
            
            # שימוש במודל היציב ביותר text-bison-001
            url = f"https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText?key={api_key}"
            
            data = {
                "prompt": {
                    "text": f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית הכולל את המצרכים הבאים: {ingredients}"
                },
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "candidateCount": 1
            }
            
            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    result = response.json()
                    recipe_text = result['candidates'][0]['output']
                    st.success("הנה המתכון שמצאתי:")
                    st.write(recipe_text)
                else:
                    st.error("השרת של גוגל לא זיהה את המודל. מנסה גרסה חלופית...")
                    # ניסיון אחרון עם Gemini-1.0-pro (לעיתים זה השם שמתקבל)
                    url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={api_key}"
                    data_alt = {"contents": [{"parts": [{"text": f"צור מתכון כשר בעברית עבור: {ingredients}"}]}]}
                    resp_alt = requests.post(url_alt, json=data_alt)
                    if resp_alt.status_code == 200:
                        st.write(resp_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"שגיאה: {resp_alt.status_code}. יש לבדוק אם ה-API Key מופעל ב-Google AI Studio.")
            except Exception as e:
                st.error(f"שגיאת תקשורת: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
