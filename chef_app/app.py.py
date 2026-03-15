import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח של גוגל בינה מלאכותית (API Key)
GOOGLE_API_KEY = "AIzaSyDl0NKD7aRmNGUmVKQQAxUpDdCgEo3RSjU"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף (חובה להופיע ראשון)
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. חיבור ל-Google Analytics (הקוד האישי שלך)
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

# 4. עיצוב האתר ליישור לימין (RTL) ושיפור המראה
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
st.write("ברוכים הבאים! הזינו מצרכים וקבלו מתכון כשר וטעים תוך שניות.")

# תיבת קלט מהמשתמש
ingredients = st.text_input("מה המצרכים שיש לך היום?", placeholder="למשל: תפוחי אדמה, פטריות, בצל...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף מכין לך משהו טעים...'):
            try:
                # קריאה למודל Gemini Flash
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                # הנחיה לבינה המלאכותית
                prompt = f"יש לי את המצרכים הבאים: {ingredients}. תכתוב לי בבקשה מתכון כשר, טעים ופשוט להכנה בשפה העברית. הקפד על שלבי הכנה ברורים ומפורטים."
                
                response = model.generate_content(prompt)
                
                st.success("הנה המתכון שהכנתי עבורך:")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                st.error("חלה שגיאה בחיבור לשרת הבינה המלאכותית.")
                st.info("נסה לרענן את הדף או לבדוק את החיבור לאינטרנט.")
    else:
        st.warning("בבקשה תכתוב לפחות מצרך אחד.")

st.markdown("---")
st.caption("נוצר על ידי השף הדיגיטלי | המדידה פעילה")
