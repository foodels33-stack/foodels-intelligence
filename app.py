import json
import urllib.parse
import urllib.request
import google.generativeai as genai
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="פודלס - מערכת מודיעין עסקי", page_icon="🧠", layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rubik', sans-serif; }
    [data-testid="stMainBlockContainer"], [data-testid="stSidebar"] { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; background-color: #FF6B00; color: white; font-weight: bold; border-radius: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("🧠 פודלס מודיעין")
st.sidebar.subheader("מרכז שליטה")

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

st.title("🎯 מערכת מודיעין תחרותי - פודלס")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 מחולל קמפיינים",
    "⭐ סורק ביקורות גוגל (אוטומטי)",
    "💡 יועץ עסקי אישי",
    "👁️ ניטור מודעות Meta",
])


def get_ai_response(prompt_text, api_key_val):
  genai.configure(api_key=api_key_val)
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content(prompt_text)
  return response.text


def fetch_google_reviews(business_name, api_key_val):
  try:
    url_new = "https://places.googleapis.com/v1/places:searchText"
    headers_new = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key_val,
        "X-Goog-FieldMask": "places.displayName,places.reviews",
    }
    body_new = json.dumps(
        {"textQuery": business_name, "languageCode": "he"}
    ).encode("utf-8")
    req_new = urllib.request.Request(
        url_new, data=body_new, headers=headers_new, method="POST"
    )
    with urllib.request.urlopen(req_new) as resp_new:
      data_new = json.loads(resp_new.read().decode())
    places = data_new.get("places", [])
    if places:
      place = places[0]
      found_name = place.get("displayName", {}).get("text", business_name)
      reviews = place.get("reviews", [])
      if reviews:
        formatted_reviews = ""
        for r in reviews:
          author = r.get("authorAttribution", {}).get("displayName", "לקוח")
          rating = r.get("rating", 5)
          text = r.get("text", {}).get("text", "")
          if text:
            formatted_reviews += f"- [{rating} כוכבים] {author}: {text}\n"
        if formatted_reviews:
          return found_name, formatted_reviews
  except Exception:
    pass
  return None, "לא נמצאו ביקורות"


with tab1:
  st.header("מחולל הצעות ערך וקמפיינים")
  focus_area = st.selectbox("בחר מוקד אסטרטגי:", [
      "מענה לחולשת מתחרה (עיכוב במשלוחים)",
      "קידום מזון רפואי/טיפולי",
      "מבצע מחיר אגרסיבי למשיכת לקוחות חדשים",
      "חיזוק המותג ושירות הלקוחות האישי",
  ])
  target_audience = st.selectbox("קהל יעד:", [
      "בעלי כלבים בבאר שבע והסביבה",
      "בעלי חתולים",
      "לקוחות שנוטשים מתחרים באזור",
      "סטודנטים וצעירים בשכונת רמות",
  ])

  if st.button("גזור תובנות והפק רעיון לקמפיין ✨"):
    if not gemini_key:
      st.warning("⚠️ לא נמצא מפתח Gemini API.")
    else:
      try:
        prompt = f"""
                אתה מומחה שיווק וקופירייטר שעובד עבור חנות החיות 'פודלס' בבאר שבע (שכונת רמות).
                צור רעיון לקמפיין שיווקי ממוקד וקצר על בסיס הנתונים הבאים:
                מוקד אסטרטגי: {focus_area}
                קהל יעד: {target_audience}
                הצג את התשובה בעברית קלילה ושיווקית עם אמוג'ים במבנה הבא:
                🎯 **כותרת לקמפיין**
                📝 **טקסט לפוסט/סטורי**
                💡 **הצעה לפעולה**
                """
        with st.spinner("ה-AI מנתח ומייצר קמפיין... 🧠"):
          response_text = get_ai_response(prompt, gemini_key)
        st.success("✅ הקמפיין מוכן!")
        st.markdown(response_text)
      except Exception as e:
        st.error(f"שגיאה: {e}")

with tab2:
  st.header("⭐ סורק ביקורות גוגל אוטומטי")
  target_store = st.text_input("שם החנות לסריקה:")
  if st.button("סרוק ביקורות 🚀"):
    st.info("ניתן לדלג על סעיף הביקורות אם אינו קריטי כרגע.")

with tab3:
  st.header("💡 יועץ עסקי וקופירייטר אישי לפודלס")
  user_query = st.text_area("מה תרצה לשאול היום?", height=100)
  if st.button("התייעץ עם ה-AI 🧠"):
    if not user_query.strip():
      st.warning("אנא כתוב שאלה.")
    elif not gemini_key:
      st.warning("⚠️ לא נמצא מפתח Gemini API.")
    else:
      try:
        consultant_prompt = f"""
                אתה היועץ העסקי והשיווקי של חנות החיות 'פודלס' בבאר שבע.
                ענה בצורה מקצועית ומעשית לשאלה: "{user_query}"
                """
        with st.spinner("מנסח תשובה... 💡"):
          answer_text = get_ai_response(consultant_prompt, gemini_key)
        st.success("✅ התשובה מוכנה:")
        st.markdown(answer_text)
      except Exception as e:
        st.error(f"שגיאה: {e}")

with tab4:
  st.header("👁️ ניטור מודעות Meta וטרנדים")
  ad_text = st.text_area("הדבק טקסט של מודעה:", height=100)
  if st.button("פרק מודעה 💥"):
    if not ad_text.strip():
      st.warning("אנא הדבק טקסט מודעה.")
    elif not gemini_key:
      st.warning("⚠️ לא נמצא מפתח Gemini API.")
    else:
      try:
        ad_prompt = f"נתח בקצרה את המודעה הבאה לחנות חיות ותן הצעת נגד: '{ad_text}'"
        with st.spinner("מפרק את המודעה... 🔍"):
          ad_res = get_ai_response(ad_prompt, gemini_key)
        st.success("✅ הניתוח מוכן!")
        st.markdown(ad_res)
      except Exception as e:
        st.error(f"שגיאה: {e}")
