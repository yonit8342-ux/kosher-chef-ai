import streamlit as st
import requests

# 1. הגדרות דף ועיצוב לממשק בעברית (RTL)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.markdown("""
    <style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    div.stButton > button { 
        width: 100%; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold; 
        height: 3em;
        border-radius: 10px;
    }
    .stMarkdown { direction: RTL; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. משיכת המפתח מה-Secrets
api_key = st.secrets.get("GEMINI_KEY")

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו את המצרכים שיש לכם בבית, והשף יבנה לכם מתכון כשר וטעים!")

ingredients = st.text_input("מה המצרכים שלך?", placeholder="למשל: עוף, תפוחי אדמה, סילאן...")

if st.button("צור מתכון כשר עכשיו"):
    if not api_key:
        st.error("חסר מפתח API בתוך ה-Secrets של Streamlit!")
    elif ingredients:
        with st.spinner('השף מגבש מתכון...'):
            # הגדרת ה-URL והנתונים לשליחה (כאן ההזחה קריטית!)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"אתה שף מומחה לכשרות. כתוב מתכון כשר, ברור וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    # חילוץ הטקסט מהתשובה
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון שמצאתי עבורך:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("הגענו למכסה המקסימלית של המודל הזה. נסה שוב בעוד דקה או החלף מודל.")
                else:
                    error_msg = data.get('error', {}).get('message', 'שגיאה לא ידועה')
                    st.error(f"שגיאת API: {error_msg}")
                    
            except Exception as e:
                st.error("חלה שגיאה בתקשורת עם השרת.")
                st.code(str(e))
    else:
        st.warning("בבקשה הזינו לפחות מצרך אחד.")

# הערה לניהול גרסאות
st.sidebar.markdown("---")
st.sidebar.write("מערכת שף כשר AI - גרסה 2.2")
st.sidebar.info("הקוד מתוקן עם הזחות נכונות ומודל 2.0-flash.")
