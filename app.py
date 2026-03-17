import streamlit as st
import requests

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: עוף, תפוחי אדמה, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('מתחבר לשרת...'):
            api_key = "AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M"
            
            # ✔️ מודל שעובד
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"אתה שף מומחה. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"
                            }
                        ]
                    }
                ]
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    try:
                        recipe_text = result['candidates'][0]['content']['parts'][0]['text']
                        
                        st.success("הנה המתכון!")
                        
                        # ✔️ הצמדה לימין
                        st.markdown(
                            f"<div style='text-align: right; direction: rtl;'>{recipe_text}</div>",
                            unsafe_allow_html=True
                        )
                        
                    except (KeyError, IndexError):
                        st.error("התגובה מהשרת לא בפורמט צפוי")
                        st.json(result)
                else:
                    st.error(f"שגיאה מהשרת: {response.status_code}")
                    st.json(response.json())
                    
            except Exception as e:
                st.error(f"שגיאת חיבור: {str(e)}")
