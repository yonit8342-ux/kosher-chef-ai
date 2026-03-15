import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח של גוגל בינה מלאכותית
GOOGLE_API_KEY = "AIzaSyDl0NKD7aRmNGUmVKQQAxUpDdCgEo3RSjU"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרת דף (חובה ראשון)
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. חיבור ל-Google Analytics (החלף את ה-G-XXXXXXXXXX בקוד שלך)
GA_ID = "G-XXXXXXXXXX" 
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
    </style>
    """, unsafe_allow_html=True)

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("הזינו מצרכים וקבלו מתכון כשר וטעים!")

ingredients = st.text_input("מה המצרכים שיש לך?", "תפוחי אדמה, שמן, מלח")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף בעבודה...'):
            try:
                model = genai.GenerativeModel('models/gemini-flash-latest')
                prompt = f"יש לי את המצרכים הבאים: {ingredients}. תכתוב לי בבקשה מתכון כשר, טעים ופשוט להכנה בשפה העברית."
                response = model.generate_content(prompt)
                st.success("הנה המתכון המנצח:")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error("חלה שגיאה בחיבור.")
    else:
        st.warning("נא להזין מצרכים.")

st.markdown("---")
st.caption("מבוסס על Gemini Flash | המדידה פעילה")
