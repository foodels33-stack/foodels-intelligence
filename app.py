import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import urllib.parse
import urllib.request

# הגדרת תצורת עמוד
st.set_page_config(
    page_title="פודלס - מערכת מודיעין עסקי",
    page_icon="🧠",
    layout="wide"
)

# CSS מותאם למובייל ולעברית (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
    }
    [data-testid="stMainBlockContainer"], [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B00;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# תפריט צד (Sidebar)
st.sidebar.title("🧠 פודלס מודיעין")
st.sidebar.subheader("מרכז שליטה")

# טעינת המפתחות מתוך ה-Secrets
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
places_key = st.secrets.get("PLACES_API_KEY", "")

if gemini_key:
    st.sidebar.success("🔑 מפתח Gemini מחובר")
else:
    gemini_key = st.sidebar.text_input("מפתח Gemini API:", type="password")

if places_key:
    st.sidebar.success("📍 מפתח Places API מחובר")
else:
    places_key = st.sidebar.text_input("מפתח Places API:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("המערכת מנטרת מתחרים בבאר שבע ומפיקה תובנות AI בזמן אמת.")

# כותרת ראשית
st.title("🎯 מערכת מודיעין תחרותי - פודלס")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 מחולל קמפיינים", 
    "⭐ סורק ביקורות גוגל (אוטומטי)", 
    "💡 יועץ עסקי אישי", 
    "👁️ ניטור מודעות Meta"
])

# --- פונקציית עזר לחיבור ל-AI ---
def get_ai_response(prompt_text, api_key_val):
    genai.configure(api_key=api_key_val)
    try:
        model = genai.GenerativeModel('gemini-3.8-flash')
        return model.generate_content(prompt_text).text
    except Exception:
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model.generate_content(prompt_text).text

# --- פונקציה לשליפת ביקורות אוטומטית מגוגל מפות ---
def fetch_google_reviews(business_name, api_key_val):
    try:
        encoded_query = urllib.parse.quote(business_name)
        search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_query}&key={api_key_val}&language=he"
        
        req = urllib.request.Request(search_url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if not data.get("results"):
            return None, "לא נמצא עסק בשם זה בגוגל מפות. נסה להקליד שם מדויק יותר (למשל: 'שם החנות באר שבע')."
            
        place = data["results"][0]
        place_id = place["place_id"]
        found_name = place.get("name", business_name)
        
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,reviews,rating&key={api_key_val}&language=he"
        
        req_det = urllib.request.Request(details_url)
        with urllib.request.urlopen(req_det) as response_det:
            det_data = json.loads(response_det.read().decode())
            
        result = det_data.get("result", {})
        reviews = result.get("reviews", [])
        
        if not reviews:
            return None, f"נמצא העסק '{found_name}', אך אין עבורו ביקורות טקסטואליות פומביות ב-API."
            
        formatted_reviews = ""
        for r in reviews:
            author = r.get("author_name", "לקוח")
            rating = r.get("rating", 5)
            text = r.get("text", "")
            if text:
                formatted_reviews += f"- [{rating} כוכבים] {author}: {text}\n"
                
        return found_name, formatted_reviews
        
    except Exception as e:
        return None, f"שגיאה בשליפת נתונים מגוגל מפות: {e}"

# --- כרטיסיה 1: מחולל קמפיינים ---
with tab1:
    st.header("מחולל הצעות ערך וקמפיינים")
    st.write("בחר מיקוד, וה-AI ייצר עבורך קמפיין שיווקי מלא לפודלס.")
    
    focus_area = st.selectbox("בחר מוקד אסטרטגי:", [
        "מענה לחולשת מתחרה (עיכוב במשלוחים)",
        "קידום מזון רפואי/טיפולי",
        "מבצע מחיר אגרסיבי למשיכת לקוחות חדשים",
        "חיזוק המותג ושירות הלקוחות האישי"
    ])
    
    target_audience = st.selectbox("קהל יעד:", [
        "בעלי כלבים בבאר שבע והסביבה",
        "בעלי חתולים",
        "לקוחות שנוטשים מתחרים באזור",
        "סטודנטים וצעירים בשכונת רמות"
    ])
        
    if st.button("גזור תובנות והפק רעיון לקמפיין ✨"):
        if not gemini_key:
            st.warning("⚠️ לא נמצא מפתח Gemini API.")
        else:
            try:
                prompt = f"""
                אתה מומחה שיווק וקופירייטר שעובד עבור חנות חיות בשם 'פודלס' בבאר שבע (שכונת רמות).
                צור רעיון לקמפיין שיווקי ממוקד וקצר על בסיס הנתונים הבאים:
                מוקד אסטרטגי: {focus_area}
                קהל יעד: {target_audience}
                
                הצג את התשובה בעברית קלילה ושיווקית, עם אמוג'ים, במבנה הבא:
                🎯 **כותרת קליטה לקמפיין**
                📝 **טקסט לפוסט/סטורי (כולל הומור קל)**
                💡 **הצעה לפעולה (Call to Action) להזמנה מהירה**
                """
                
                with st.spinner('ה-AI מנתח ומייצר קמפיין... 🧠'):
                    response_text = get_ai_response(prompt, gemini_key)
                    
                st.success("✅ הקמפיין מוכן!")
                st.markdown(response_text)
                
            except Exception as e:
                st.error(f"שגיאה: {e}")

# --- כרטיסיה 2: סורק ביקורות גוגל אוטומטי ---
with tab2:
    st.header("⭐ סורק ביקורות גוגל אוטומטי")
    st.write("הקלד שם של חנות מתחרה בבאר שבע – המערכת תסרוק את הביקורות שלה בגוגל מפות ותפיק ניתוח מודיעיני.")
    
    target_store = st.text_input(
        "שם החנות לסריקה:", 
        placeholder="למשל: חנות חיות באר שבע / שם המתחרה"
    )
    
    if st.button("סרוק ביקורות ונתח אוטומטית 🚀"):
        if not target_store.strip():
            st.warning("אנא הקלד שם של חנות.")
        elif not places_key:
            st.warning("⚠️ לא נמצא מפתח Places API ב-Secrets.")
        elif not gemini_key:
            st.warning("⚠️ לא נמצא מפתח Gemini API ב-Secrets.")
        else:
            with st.spinner(f'שולף ביקורות גוגל עבור "{target_store}"... 🔍'):
                store_name, reviews_data = fetch_google_reviews(target_store, places_key)
                
            if not store_name:
                st.error(reviews_data)
            else:
                st.success(f"✅ נשלפו ביקורות עבור: **{store_name}**")
                
                with st.expander("צפה בביקורות הגולמיות שנשלפו מגוגל"):
                    st.text(reviews_data)
                
                analysis_prompt = f"""
                אתה יועץ אסטרטגי ואיש מודיעין עסקי לחנות החיות 'פודלס' בבאר שבע.
                להלן ביקורות גוגל שנשלפו בזמן אמת עבור המתחרה '{store_name}':
                
                {reviews_data}
                
                אנא הפק דוח מודיעיני קצר וחד בעברית במבנה הבא:
                🔴 **חולשות ונקודות תורפה של המתחרה** (מתוך תלונות הלקוחות)
                🟢 **הזדמנות זהב עבור 'פודלס'** (איך למשוך את הלקוחות שלהם)
                ⚡ **מסר שיווקי/פוסט מומלץ למענה מיידי**
                """
                
                with st.spinner('מנתח את הביקורות עם AI... 🧠'):
                    try:
                        ai_analysis = get_ai_response(analysis_prompt, gemini_key)
                        st.markdown(ai_analysis)
                    except Exception as e:
                        st.error(f"שגיאה בניתוח ה-AI: {e}")

# --- כרטיסיה 3: יועץ עסקי אישי ---
with tab3:
    st.header("💡 יועץ עסקי וקופירייטר אישי לפודלס")
    st.write("שאל כל שאלה עסקית, בקש רעיון למבצע, פוסט, או התייעצות לגבי החנות.")
    
    user_query = st.text_area(
        "מה תרצה לשאול היום?",
        height=100,
        placeholder="למשל: תן לי 3 רעיונות לסטוריז לקידום חול לחתולים, או איך לתמחר ערכת סטרטר לגורים?"
    )
    
    if st.button("התייעץ עם ה-AI 🧠"):
        if not user_query.strip():
            st.warning("אנא כתוב שאלה.")
        elif not gemini_key:
            st.warning("⚠️ לא נמצא מפתח Gemini API ב-Secrets.")
        else:
            try:
                consultant_prompt = f"""
                אתה היועץ העסקי והשיווקי הבכיר של חנות החיות 'פודלס' (Foodels) בשכונת רמות, באר שבע.
                ענה בצורה מקצועית, מעשית, ממוקדת ויצירתית לשאלה הבאה:
                "{user_query}"
                """
                
                with st.spinner('מנסח תשובה אסטרטגית... 💡'):
                    answer_text = get_ai_response(consultant_prompt, gemini_key)
                    
                st.success("✅ התשובה מוכנה:")
                st.markdown(answer_text)
                
            except Exception as e:
                st.error(f"שגיאה בקבלת תשובה: {e}")

# --- כרטיסיה 4: ניטור מודעות Meta ---
with tab4:
    st.header("👁️ ניטור מודעות Meta וטרנדים")
    ad_text = st.text_area(
        "הדבק טקסט של מודעה ממומנת שראית אצל מתחרה:",
        height=100,
        placeholder="למשל: 'רק בסוף השבוע! 20% הנחה על כל מזונות הכלבים + משלוח חינם מעל 150 ש\"ח...'"
    )
    
    if st.button("פרק מודעה וקבל הצעת נגד 💥"):
        if not ad_text.strip():
            st.warning("אנא הדבק טקסט מודעה.")
        elif not gemini_key:
            st.warning("⚠️ לא נמצא מפתח Gemini API ב-Secrets.")
        else:
            try:
                ad_prompt = f"""
                נתח את המודעה הבאה של מתחרה:
                "{ad_text}"
                
                תן פירוק קצר:
                1. 🎯 **מה ההצעה (Offer) המרכזית?**
                2. 🎣 **מה ה-Hook (הפיתיון)?**
                3. 🥊 **איך 'פודלס' יכולה להעמיד הצעה מתחרה אטרקטיבית יותר?**
                """
                with st.spinner('מפרק את המודעה... 🔍'):
                    ad_res = get_ai_response(ad_prompt, gemini_key)
                st.success("✅ הניתוח מוכן!")
                st.markdown(ad_res)
            except Exception as e:
                st.error(f"שגיאה בניתוח המודעה: {e}")
