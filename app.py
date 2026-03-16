import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. הגדרת מפתח ה-API
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# 3. הוספת Google Analytics
def add_analytics(tag_id):
    # הוספת G- אם המשתמש לא הזין אותו
    if not tag_id.startswith("G-"):
        tag_id = f"G-{tag_id}"
    
    analytics_script = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={tag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{tag_id}');
        </script>
    """
    components.html(analytics_script, height=0)

# הטמעת המזהה שלך
add_analytics("4WZTVRVRHX")

# 4. עיצוב RTL (יישור לימין)
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL; 
        text-align: right;
    }
    input { 
        direction: RTL !important; 
        text-align: right !important; 
    }
    div.stButton > button { 
        width: 100%; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. ממשק משתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים וקבלו מתכון כשר לשבת או ליום חול.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, אורז, תפוחי אדמה...")

# 6. לוגיקה של יצירת המתכון
if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף בודק במטבח...'):
            try:
                # שימוש במודל 1.5 פלאש בצורה ישירה למניעת שגיאת v1beta
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"אתה שף מומחה. צור מתכון כשר, ברור וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כלול רשימת מצרכים והוראות הכנה."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שמצאתי עבורך:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("לא הצלחתי לייצר מתכון. נסה שוב.")
            
            except Exception as e:
                st.error("חלה שגיאה טכנית.")
                st.caption(f"פרטי שגיאה: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")

st.markdown("---")
st.caption("המתכון נוצר על ידי בינה מלאכותית. יש לוודא כשרות וטריות.")
