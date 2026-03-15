import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח האישי שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. חיבור ל-Google Analytics (המזהה שלך)
GA_ID = "G-4WZTVRVRHX" 
st.markdown(f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
    </script>
    """, unsafe_allow_html=True)

# 4. עיצוב יישור לימין (RTL)
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
        border-radius: 10px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("שלום! כתבו את המצרכים שיש לכם בבית, והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, בצל, ביצים...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף חושב על מתכון...'):
            try:
                # התיקון: שימוש בנתיב מפורש למודל כדי למנוע שגיאת v1beta
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                
                # יצירת התוכן
                prompt = f"צור מתכון כשר, פשוט וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כתוב את המתכון עם רשימת מצרכים מסודרת והוראות הכנה ברורות."
                
                # שליחת הבקשה עם הגדרת בטיחות בסיסית
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("לא התקבל תוכן מהבינה המלאכותית. נסו שוב.")
                    
            except Exception as e:
                # הצגת הודעה ידידותית למשתמש
                st.error("השף נתקל בבעיה בחיבור.")
                # הדפסת השגיאה הטכנית בקטן
