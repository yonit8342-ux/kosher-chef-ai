import streamlit as st
import requests

# עיצוב האתר (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# משיכת המפתח
api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר - תיקון סופי")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים כאן...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("שגיאה: חסר מפתח API ב-Secrets.")
    elif ingredients:
        with st.spinner('השף מכין את המתכון...'):
            # הכתובת המדויקת למניעת שגיאת 404
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{
                    "parts": [{"text": f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    recipe = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{recipe}</div>', unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("הגענו למכסה המקסימלית. גוגל מגבילה את הגרסה החינמית, נסה שוב בעוד דקה.")
                else:
                    st.error(f"שגיאה מהשרת ({response.status_code}): נסה להחליף מפתח API.")
            except Exception as e:
                st.error(f"חלה שגיאה בחיבור: {e}")
    else:
        st.warning("נא להזין מצרכים.")
