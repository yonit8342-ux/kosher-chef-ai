import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# פונקציית Google Analytics (אנטילקס)
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

# עיצוב RTL והצמדה לימין
st.markdown("""<style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# משיכת המפתח בצורה מאובטחת
try:
    # אם הגדרת ב-Secrets
    api_key = st.secrets.get("GOOGLE_API_KEY")
    # אם לא הגדרת ב-Secrets, ניתן לשים כאן זמנית לבדיקה (אך זה עלול להיחסם שוב)
    if not api_key:
        api_key = "הכנס_כאן_את_המפתח_החדש_רק_לבדיקה_זמנית"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("שגיאה בהגדרת ה-API. וודא שהמפתח הוזן כראוי.")
    st.stop()

st.title("🍲 שף בינה מלאכולית כשר")
ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: בשר, תפוחי אדמה, פטריות...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף מגבש מתכון כשר וטעים...'):
            try:
                response = model.generate_content(f"כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון שמצאתי:")
                st.write(response.text)
            except Exception as e:
                st.error("חלה שגיאה בחיבור למודל. וודא שהמפתח בתוקף.")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")
