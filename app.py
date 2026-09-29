import pandas as pd
import requests
import streamlit as st

# הגדרת תצורת עמוד
st.set_page_config(
    page_title="פודלס - מודיעין שוק וטרנדים חינם", page_icon="📡", layout="wide"
)

# CSS מותאם למובייל ולעברית (RTL)
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


# פונקציה לשליפת מגמות והשלמות חיפוש אמיתיות מגוגל (כולל מיקוד באר שבע)
@st.cache_data(ttl=3600)
def get_google_suggestions(query):
  try:
    full_query = f"{query} באר שבע" if "באר שבע" not in query else query
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={full_query}&hl=he"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
      data = response.json()
      return data[1] if len(data) > 1 else []
  except Exception:
    pass
  return []


# תפריט צד (Sidebar)
st.sidebar.title("📡 רדאר פודלס")
st.sidebar.subheader("מודיעין עורפי - באר שבע (רמות)")
st.sidebar.success("✅ ממוקד אזורית וחינמי")
st.sidebar.markdown("---")
st.sidebar.info(
    "המערכת מנתחת חיפושים אמיתיים ברשת ומכוונת אותם ישירות ללקוחות שלך בבאר"
    " שבע."
)

# כותרת ראשית
st.title("📡 רדאר מודיעין וטרנדים - פודלס (באר שבע)")

tab1, tab2, tab3 = st.tabs([
    "🔍 בדיקת מילות מפתח ממוקדות דרום",
    "📊 השוואת מוצרים מבוקשים",
    "🎯 מחולל קמפיינים מבוסס מחקר",
])

# --- כרטיסיה 1: בדיקת מילות מפתח ממוקדות ---
with tab1:
  st.header("🔍 חיפוש חי ממוקד באר שבע והסביבה")
  st.write(
      "הזן מוצר או תחום. המערכת תוסיף אוטומטית את אזור באר שבע ותציג לך את"
      " מדד העוצמה."
  )

  search_term = st.text_input(
      "הקלד נושא לחיפוש (למשל: אוכל לכלבים, חול לחתולים, חטיפים):",
      "אוכל לכלבים",
  )

  if st.button("שלוף נתוני אמת מגוגל 🚀"):
    with st.spinner("מנתח חיפושים באזור באר שבע..."):
      suggestions = get_google_suggestions(search_term)

    if suggestions:
      st.success(f"✅ נמצאו {len(suggestions)} חיפושים חמים שרצים עכשיו בדרום:")
      for i, item in enumerate(suggestions, 1):
        if i == 1:
          power = "🔥 חם מאוד (ביקוש שיא)"
        elif i <= 3:
          power = "⚡ ביקוש גבוה"
        else:
          power = "💡 ביקוש מתון"
        st.markdown(f"**{i}.** 🔎 `{item}` — *{power}*")
    else:
      st.warning("לא נמצאו תוצאות כרגע, נסה מילה כללית יותר.")

# --- כרטיסיה 2: השוואת מוצרים מבוקשים ---
with tab2:
  st.header("📊 מגמות חיפוש לפי קטגוריות בבאר שבע")
  category_choice = st.selectbox("בחר קטגוריה לניתוח:", [
      "מזון יבש רפואי והיפואלרגני",
      "ציוד ופתרונות לחתולים",
      "חטיפי אילוף ומוצרי פינוק",
  ])

  if st.button("הצג תמונת מצב ביקושים 📈"):
    if "מזון יבש" in category_choice:
      queries = ["אוכל היפואלרגני לכלב", "אוכל רפואי לחתולים באר שבע"]
    elif "ציוד ופתרונות לחתולים" in category_choice:
      queries = ["חול מתגבש לחתולים", "שירותים לחתולים באר שבע"]
    else:
      queries = ["חטיפי אילוף לכלבים", "עצמות לכלבים באר שבע"]

    for q in queries:
      sub_sug = get_google_suggestions(q)
      st.markdown(f"📌 **בדיקה עבור:** `{q}`")
      if sub_sug:
        st.write(
            f"השלמות מובילות מהשטח: {', '.join([f'`{s}`' for s in sub_sug[:3]])}"
        )
      else:
        st.caption("אין כרגע נתונים נוספים להשלמה זו.")

# --- כרטיסיה 3: מחולל קמפיינים מבוסס מחקר ---
with tab3:
  st.header("🎯 מחולל קמפיינים חכם מבוסס מילות מפתח")
  st.write(
      "הזן את נושא הקמפיין. המערכת תשלוף אוטומטית את מילות החיפוש החמות ביותר"
      " מגוגל ותשלב אותן בטקסט שיווקי מוכן לחנות (רחוב נחום שריג 33, שכונת"
      " רמות)."
  )

  campaign_topic = st.text_input(
      "על איזה מוצר או תחום תרצה לכתוב את הקמפיין?", "חול לחתולים"
  )
  target_audience = st.selectbox("בחר קהל יעד / זווית פרסומית:", [
      "תושבי שכונת רמות (דגש על קירבה ונוחות איסוף)",
      "מענה מהיר ופתרון מיידי (למי שנלחץ שנגמר)",
      "פינוקים והתאמה אישית לחיות המחמד",
  ])

  if st.button("צור קמפיין מבוסס מחקר חי ✨"):
    with st.spinner("שואב מילות מפתח ובונה קמפיין..."):
      # שליפת מילות החיפוש האמיתיות מגוגל ברגע זה ממש
      live_keywords = get_google_suggestions(campaign_topic)

    # בחירת מילות המפתח המובילות לשילוב בטקסט
    top_keywords_str = (
        ", ".join([f'"{kw}"' for kw in live_keywords[:3]])
        if live_keywords
        else campaign_topic
    )

    st.success("📋 הפוסט השיווקי שלך מוכן ומבוסס על נתוני החיפוש האמיתיים:")

    if "רמות" in target_audience:
      post_text = f"""
🐾 **תושבי שכונת רמות והסביבה!** 🐾  
שמים לב שרבים מחפשים לאחרונה {top_keywords_str}? בדיוק בשביל זה אנחנו כאן!  
לא צריך לנסוע רחוק, לעמוד בפקקים או לחכות למשלוחים. קפצו אלינו ל**פודלס** ברחוב נחום שריג 33, חונים ממש ליד, לוקחים ויוצאים בשתי דקות!  
📞 דברו איתנו או הגיעו לבקר: 054-5652422 / 08-6655443. מחכים לכם! ❤️
"""
    elif "מהיר" in target_audience:
      post_text = f"""
🚨 **נגמר פתאום? אל דאגה!** 🚨  
אנחנו רואים שבימים האחרונים יש ביקוש גבוה ל-{top_keywords_str}. אם החבר הפרוותי צריך את זה דחוף להיום – אין צורך לחכות למשלוח.  
קפצו אלינו לפודלס ברחוב נחום שריג 33 (שכונת רמות, באר שבע) ותאספו את מה שצריך מיד.  
📞 זמינים עבורכם: 054-5652422 / 08-6655443. נתראה בחנות! 🐕🐈
"""
    else:
      post_text = f"""
✨ **המוצרים המבוקשים ביותר מחכים לכם בפודלס!** ✨  
מחפשים את הפתרונות שכולם מדברים עליהם כמו {top_keywords_str}? הבאנו עבורכם את האיכות הגבוהה ביותר ישירות לחנות ברחוב נחום 33 (רמות, באר שבע).  
בואו לבחור את מה שהכי מתאים לפרוותי שלכם.  
📞 קפצו להכיר או התקשרו: 054-5652422 / 08-6655443. מחכים לכם! 🐾
"""

    st.markdown(post_text)

    if live_keywords:
      st.info(
          "🔎 **מילות המפתח שנשלפו מגוגל ושולבו בקמפיין:** "
          + " | ".join([f"`{kw}`" for kw in live_keywords[:4]])
      )
