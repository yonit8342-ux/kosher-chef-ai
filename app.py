import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# פונקציית Google Analytics
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

# עיצוב RTL
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# המפתח האחרון שסיפקת
API_KEY = "AIzaSyB32ZAV7A7TFi8bg694V056In2z42_MZuc"
genai.configure(api_key=API_KEY)

st.title("🍲 שף בינה מלאכולית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, תפוחי אדמה, פפריקה...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף בודק את המודלים הזמינים...'):
            # רשימת שמות מודלים אפשריים - המערכת תנסה את כולם
            possible_models = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
            
            recipe_found = False
            for model_name in possible_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                    if response.text:
                        st.success(f"המתכון מוכן! (נוצר באמצעות {model_name})")
                        st.write(response.text)
                        recipe_found = True
                        break
                except Exception:
                    continue
            
            if not recipe_found:
                st.error("שגיאה 404: המודל לא נמצא. וודא שה-API Key מופעל ב-Google AI Studio ושהגדרת את המודל לשימוש חופשי.")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
