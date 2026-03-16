import streamlit as st
import google.generativeai as genai

# 1. הגדרת מפתח ה-API שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף ועיצוב למראה עברי (יישור לימין)
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

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
        border-radius: 8px;
    }
    .stSpinner {
        direction: RTL;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית")
st.write("הזינו את המצרכים שיש לכם בבית, והשף יציע לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, תפוחי אדמה, בצל...")

# 4. לוגיקה של יצירת המתכון
if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף חושב על מתכון...'):
            try:
                # שימוש במודל העדכני ביותר ללא v1beta
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # יצירת התוכן
                prompt = f"אתה שף מומחה. צור מתכון כשר, ברור וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כלול רשימת מצרכים והוראות הכנה."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שמצאתי עבורך:")
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.error("לא הצלחתי לייצר מתכון. נסה שוב.")
            
            except Exception as e:
                # הצגת שגיאה ידידותית במידה ויש בעיה בחיבור
                st.error("חלה שגיאה בחיבור לשרת.")
                st.info("טיפ: אם אתה רואה שגיאת 404, וודא שביצעת Reboot לאפליקציה ב-Streamlit Cloud.")
                st.caption(f"פרטים טכניים: {str(e)}")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")

# הערה בתחתית הדף
st.markdown("---")
st.caption("המתכונים נוצרים על ידי בינה מלאכותית - יש לוודא כשרות וטריות המצרכים.")
