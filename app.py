import streamlit as st
import google.generativeai as genai
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

# הגדרת המפתח שסיפקת
genai.configure(api_key="AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M")

st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: חזה עוף, סילאן, שקדים...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף בודק את המזווה...'):
            try:
                # שימוש בשיטה הרשמית שמונעת שגיאות URL
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("המתכון מוכן!")
                    st.write(response.text)
                else:
                    st.error("לא התקבל טקסט מהמודל.")
            except Exception as e:
                # אם יש שגיאה, ננסה את מודל ה-Pro כגיבוי
                try:
                    model_pro = genai.GenerativeModel('gemini-pro')
                    response_pro = model_pro.generate_content(f"מתכון כשר עבור: {ingredients}")
                    st.write(response_pro.text)
                except:
                    st.error("שגיאה סופית בחיבור למודל. וודא שהמפתח פעיל ב-Google AI Studio.")
                    st.code(str(e))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
