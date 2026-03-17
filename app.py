import streamlit as st
import requests
import streamlit.components.v1 as components

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

# עיצוב מותאם לעברית
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
            # עקיפה ישירה: פנייה ל-API בלי הספרייה הבעייתית של גוגל
            api_key = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
            
            # שים לב שכאן אנחנו מכריחים אותו להשתמש ב-v1 היציב!
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": f"אתה שף מומחה. צור מתכון כשר וטעים בעברית עבור המצרכים הבאים: {ingredients}"}]}]
            }
            
            try:
                # שליחת הבקשה הישירה
                response = requests.post(url, headers=headers, json=data)
                
                # אם הכל תקין, נציג את המתכון
                if response.status_code == 200:
                    result = response.json()
                    recipe_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון שמצאתי:")
                    st.write(recipe_text)
                else:
                    # אם עדיין יש שגיאה, נדפיס בדיוק מה גוגל אומרים לנו
                    st.error("הייתה בעיה בחיבור לגוגל.")
                    st.code(f"קוד שגיאה: {response.status_code}\n{response.text}")
                    
            except Exception as e:
                st.error(f"שגיאת תקשורת: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
