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

# הגדרות דף ועיצוב
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
add_analytics()

# הצמדה לימין (RTL) ועיצוב ממשק
st.markdown("""
    <style>
    .main, .stTextInput, .stButton { direction: RTL; text-align: right; }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { 
        width: 100%; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold; 
        border-radius: 8px;
        height: 3em;
    }
    .stAlert { direction: RTL; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# הגדרת המפתח החדש שסיפקת
NEW_API_KEY = "AIzaSyB32ZAV7A7TFi8bg694V056In2z42_MZuc"

try:
    genai.configure(api_key=NEW_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("שגיאה בתצורת המערכת. וודא שהמפתח תקין.")

st.title("🍲 שף בינה מלאכותית כשר")
st.write("הכניסו את המצרכים שיש לכם בבית וקבלו מתכון כשר ומהיר!")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: חזה עוף, בצל, פפריקה, דבש...")

if st.button("צור מתכון טעים"):
    if ingredients:
        with st.spinner('השף מגבש עבורך מתכון כשר...'):
            try:
                # יצירת התוכן מהמודל
                prompt = f"אתה שף מומחה. כתוב מתכון כשר, טעים וברור בעברית המבוסס על המצרכים הבאים: {ingredients}. כלול רשימת מצרכים והוראות הכנה."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("המתכון מוכן!")
                    st.markdown("---")
                    st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
                else:
                    st.error("המודל לא החזיר תשובה. נסה שוב בעוד רגע.")
            except Exception as e:
                if "API_KEY_INVALID" in str(e) or "400" in str(e):
                    st.error("המפתח לא תקין או שפג תוקפו. יש להנפיק מפתח חדש ב-AI Studio.")
                else:
                    st.error(f"חל עיכוב קטן בחיבור: {str(e)}")
    else:
        st.warning("בבקשה הזינו לפחות מצרך אחד כדי שנוכל להתחיל.")

st.markdown("---")
st.caption("נוצר בעזרת בינה מלאכותית • שף כשר AI 2026")
