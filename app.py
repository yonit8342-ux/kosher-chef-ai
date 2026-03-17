import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# אנטילקס (Analytics)
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

# עיצוב RTL מלא
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px; }
</style>""", unsafe_allow_html=True)

# המפתח האחרון שסיפקת
API_KEY = "AIzaSyB32ZAV7A7TFi8bg694V056In2z42_MZuc"
genai.configure(api_key=API_KEY)

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, סילאן, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מתחבר למערכת...'):
            try:
                # בדיקה אילו מודלים באמת זמינים עבור המפתח הזה
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not available_models:
                    st.error("לא נמצאו מודלים זמינים למפתח זה. וודא שהגדרת את המפתח ב-AI Studio כראוי.")
                else:
                    # שימוש במודל הראשון שזמין (לרוב זה יהיה ה-Flash או ה-Pro)
                    model_to_use = available_models[0]
                    model = genai.GenerativeModel(model_to_use)
                    
                    response = model.generate_content(f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                    
                    st.success(f"המתכון מוכן! (באמצעות {model_to_use})")
                    st.write(response.text)
            except Exception as e:
                st.error("שגיאה קריטית בחיבור לגוגל.")
                st.code(str(e))
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
