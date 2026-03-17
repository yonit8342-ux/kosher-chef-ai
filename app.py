import streamlit as st
import requests
import streamlit.components.v1 as components

# אנטילקס ויישור לימין
def setup_ui():
    st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
    components.html("""
        <script async src="https://www.googletagmanager.com/gtag/js?id=4WZTVRVRHX"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '4WZTVRVRHX');
        </script>
    """, height=0)
    st.markdown("""<style>
        .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
        input { direction: RTL !important; text-align: right !important; }
        div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>""", unsafe_allow_html=True)

setup_ui()

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה המצרכים שלך?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('מכין את המתכון...'):
            # המפתח החדש שלך - וודא שהוא הועתק נכון מ-AI Studio
            api_key = "AIzaSyB32ZAV7A7TFi8bg694V056In2z42_MZuc"
            
            # כתובת ה-API הכי יציבה למניעת 404
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                res_json = response.json()
                
                if response.status_code == 200:
                    recipe = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.write(recipe)
                else:
                    # הצגת השגיאה בצורה ברורה כדי שנדע מה לתקן ב-3 דקות שנשארו
                    error_msg = res_json.get('error', {}).get('message', 'Unknown error')
                    st.error(f"שגיאה: {error_msg}")
                    if "leaked" in error_msg.lower():
                        st.warning("גוגל חסמה את המפתח כי הוא גלוי בגיטהאב. צור מפתח חדש ב-AI Studio והדבק אותו כאן במקום הקודם.")
            except Exception as e:
                st.error("תקלה בחיבור. נסה שוב.")
    else:
        st.warning("הכנס מצרכים קודם.")
