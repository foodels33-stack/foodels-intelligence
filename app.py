import streamlit as st
import pandas as pd
import google.generativeai as genai

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

# בדיקה וטעינה מתוך ה-Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("🔑 מפתח API מחובר מ-Secrets")
else:
    api_key = st.sidebar.text_input("מפתח API (Gemini):", type="password")

st.sidebar.markdown("---")
st.sidebar.info("המערכת מנטרת מתחרים בבאר שבע ומפיקה תובנות AI בזמן אמת.")

# כותרת ראשית
st.title("🎯 מערכת מודיעין תחרותי - פודלס")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 מחולל קמפיינים", 
    "⭐ מנתח ביקורות מתחרים", 
    "💡 יועץ עסקי אישי", 
    "👁️ ניטור מודעות וטרנדים"
])

# --- פונקציית עזר לחיבור ל-AI ---
def get_ai_response(prompt_text, api_key_val):
    genai.configure(api_key=api_key_val)
    try:
        model = genai.GenerativeModel('gemini-3.8-flash')
        return model.generate_content(prompt_text).text
    except Exception as e:
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            return model.generate_content(prompt_text).text
        except Exception:
            raise e

# --- כרטיסיה 1: מחולל קמפיינים מבוסס AI ---
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
        if not api_key:
            st.warning("⚠️ לא נמצא מפתח API. ודא שהגדרת GEMINI_API_KEY ב-Secrets ב-Streamlit.")
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
                    response_text = get_ai_response(prompt, api_key)
                    
                st.success("✅ הקמפיין מוכן!")
                st.markdown(response_text)
                
            except Exception as e:
                st.error(f"שגיאה בחיבור ל-API. ודא שהמפתח ב-Secrets תקין. שגיאה: {e}")

# --- כרטיסיה 2: מנתח ביקורות ומודיעין תחרותי ---
with tab2:
    st.header("⭐ מנתח ביקורות גוגל ומודיעין מתחרים")
    st.write("הדבק ביקורות גוגל/פייסבוק של מתחרים בבאר שבע, וה-AI יחלץ נקודות תורפה והזדמנויות לפודלס.")
    
    competitor_name = st.text_input("שם המתחרה (רשות):", placeholder="למשל: חנות X באר שבע")
    reviews_text = st.text_area(
        "הדבק כאן טקסט של ביקורות (אפשר להעתיק כמה ביקורות ביחד מגוגל):",
        height=150,
        placeholder="למשל: 'הזמנתי אוכל לכלב ביום ראשון והגיע רק ברביעי...', 'אין מענה בטלפון', 'יקרים מאוד מול חנויות אחרות'"
    )
    
    if st.button("נתח ביקורות וגזור תובנות תחרותיות 🔍"):
        if not reviews_text.strip():
            st.warning("אנא הדבק טקסט של ביקורות כדי לבצע ניתוח.")
        elif not api_key:
            st.warning("⚠️ לא נמצא מפתח API ב-Secrets.")
        else:
            try:
                analysis_prompt = f"""
                אתה יועץ אסטרטגי ואיש מודיעין עסקי לחנות החיות 'פודלס' בבאר שבע.
                נתח את הביקורות הבאות שנכתבו על מתחרה בשם '{competitor_name}':
                
                "{reviews_text}"
                
                אנא הפק דוח מודיעיני קצר וחד בעברית במבנה הבא:
                🔴 **תלונות מרכזיות וחולשות שזוהו** (נקודות תורפה קריטיות)
                🟢 **הזדמנות זהב עבור 'פודלס'** (איך לנצל את התלונה לטובתנו)
                ⚡ **מסר שיווקי/צעד מומלץ למענה מיידי** (משפט מחץ לפוסט או למודעה)
                """
                
                with st.spinner('סורק ומנתח את הביקורות... 🔍'):
                    res_text = get_ai_response(analysis_prompt, api_key)
                    
                st.success("✅ הניתוח המודיעיני הושלם!")
                st.markdown(res_text)
                
            except Exception as e:
                st.error(f"שגיאה בניתוח הביקורות: {e}")

# --- כרטיסיה 3: יועץ עסקי אישי ---
with tab3:
    st.header("💡 יועץ עסקי וקופירייטר אישי לפודלס")
    st.write("שאל כל שאלה עסקית, בקש רעיון למבצע, פוסט, או התייעצות לגבי החנות.")
    
    user_query = st.text_area(
        "מה תרצה לשאול או לפתח היום?",
        height=120,
        placeholder="למשל: תן לי 3 רעיונות לסטוריז מצחיקים לקידום חול החתולים, או איך לתמחר ערכת סטרטר לגורים?"
    )
    
    if st.button("התייעץ עם ה-AI 🧠"):
        if not user_query.strip():
            st.warning("אנא כתוב שאלה או נושא התייעצות.")
        elif not api_key:
            st.warning("⚠️ לא נמצא מפתח API ב-Secrets.")
        else:
            try:
                consultant_prompt = f"""
                אתה היועץ העסקי והשיווקי הבכיר של חנות החיות 'פודלס' (Foodels) הנמצאת בשכונת רמות, באר שבע.
                אתה מכיר את השוק המקומי בבאר שבע, את קהל הלקוחות (בעלי כלבים, חתולים, סטודנטים, משפחות).
                
                ענה בצורה מקצועית, מעשית, ממוקדת ויצירתית לשאלה הבאה:
                "{user_query}"
                """
                
                with st.spinner('חושב ומנסח תשובה אסטרטגית... 💡'):
                    answer_text = get_ai_response(consultant_prompt, api_key)
                    
                st.success("✅ התשובה מוכנה:")
                st.markdown(answer_text)
                
            except Exception as e:
                st.error(f"שגיאה בקבלת תשובה: {e}")

# --- כרטיסיה 4: ניטור מודעות Meta וטרנדים ---
with tab4:
    st.header("👁️ ניטור מודעות Meta וטרנדים")
    st.info("כאן תוכל להדביק טקסט או קישור ממודעה של מתחרה בפייסבוק/אינסטגרם לקבלת פירוק של ה-Offer והרעיון השיווקי.")
    
    ad_text = st.text_area(
        "הדבק טקסט של מודעה ממומנת שראית אצל מתחרה:",
        height=100,
        placeholder="למשל: 'רק בסוף השבוע! 20% הנחה על כל מזונות הכלבים + משלוח חינם מעל 150 ש\"ח...'"
    )
    
    if st.button("פרק מודעה וקבל הצעת נגד 💥"):
        if not ad_text.strip():
            st.warning("אנא הדבק טקסט מודעה לניתוח.")
        elif not api_key:
            st.warning("⚠️ לא נמצא מפתח API ב-Secrets.")
        else:
            try:
                ad_prompt = f"""
                נתח את המודעה הממומנת הבאה של מתחרה בתחום החנויות חיות:
                "{ad_text}"
                
                תן פירוק קצר:
                1. 🎯 **מה ההצעה (Offer) המרכזית?**
                2. 🎣 **מה ה-Hook (הפיתיון)?**
                3. 🥊 **איך 'פודלס' יכולה להעמיד הצעה מתחרה אטרקטיבית יותר?**
                """
                with st.spinner('מפרק את המודעה... 🔍'):
                    ad_res = get_ai_response(ad_prompt, api_key)
                st.success("✅ הניתוח מוכן!")
                st.markdown(ad_res)
            except Exception as e:
                st.error(f"שגיאה בניתוח המודעה: {e}")
