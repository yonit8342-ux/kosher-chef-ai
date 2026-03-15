import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח האישי שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף ויישור לימין (RTL)
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# הזרקת CSS ליישור כל האפליקציה לימין
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"], .stAlert {
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
    /* יישור הודעות שגיאה והצלחה */
    div[data-testid="stNotificationContent"] {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. חיבור ל-Google Analytics
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

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("שלום! כתבו את המצרכים שיש לכם בבית, והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, בצל, ביצים...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף חושב על מתכון...'):
            try:
                # שימוש במודל בגרסה היציבה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"צור מתכון כשר, פשוט וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כתוב את המתכון עם רשימת מצרכים מסודרת והוראות הכנה ברורים."
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("לא התקבל תוכן. נסה שוב.")
                    
            except Exception as e:
                # הודעת שגיאה מיושרת לימין
                st.error("חלה שגיאה בחיבור לשרת ה-AI.")
                st.info("אנא וודאו שהמפתח הופעל כראוי ב-Google AI Studio ושהגדרתם Billing (גם אם בחינם).")
                st.caption(f"פרטים טכניים: {str(e)}")
    else:
        st.warning("נא להזין לפחות מצרך אחד.")

st.markdown("---")
st.caption("השף הדיגיטלי | יישור לימין פעיל")
