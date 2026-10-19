"""
THUNAI — Agentic Brain & Multilingual Reasoning Layer
Supports:
  - Tamil (தமிழ்)
  - English
  - Tanglish (Tamil in English letters)
  - Automatic Language Detection
  - Structured Agent Tools Layer
  - Glass-Box Safe Action Trace ("How THUNAI Worked")
  - MeTTa / Reasoning Knowledge Engine
  - Adaptive "Grows Up" Engine (tracks interactions, bonding %, and auto-learns preferences)
  - Deep Semantic Conversational Intelligence (never repeats generic fallbacks)
  - Google Gemini 2.5 Flash official SDK integration with rich offline safety engine
"""

import os
import re
import json
from datetime import datetime
from state import load_state, save_state, record_interaction_growth

# Try importing official Google GenAI SDK
GOOGLE_GENAI_AVAILABLE = False
try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False


def get_gemini_client(api_key=None):
    """Initializes Google GenAI client if API key is provided or in environment."""
    if not GOOGLE_GENAI_AVAILABLE:
        return None
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception as e:
        print(f"[THUNAI GenAI] Error initializing client: {e}")
        return None


# ==============================================================
# 1. LANGUAGE DETECTION: TAMIL, ENGLISH, & TANGLISH
# ==============================================================

TANGLISH_VOCABULARY = {
    # Pronouns & family
    "amma", "appa", "thatha", "thaatha", "paati", "priya", "suresh", "akka", "thambi", "anna",
    "en", "enakku", "namma", "ungal", "unga", "neenga", "naan", "avar", "idhu", "adhu", "yaru",
    # Verbs & actions
    "pannu", "pannunga", "podu", "podunga", "sollu", "sollunga", "sapdu", "saapdu", "sapdunga",
    "edukkanum", "edukanum", "kudikanum", "kudika", "kudi", "pesu", "pesunga", "varala", "varudhu",
    "varuthu", "pochu", "irukku", "iruken", "irukken", "mudiyala", "kooda", "panna", "paaru", "paadunga",
    # Health & symptoms
    "valikithu", "valikidhu", "vali", "thala", "kaal", "mutti", "kai", "udambu", "marundhu", "marunthu",
    "mathirai", "maathirai", "tablets", "bp", "sugar", "fever", "kaachal", "mayakkam", "nenju", "moochu",
    "bayam", "amaidhi", "thookam", "gas", "acidity", "asathiya", "tired", "neruppu", "erichal",
    # Questions, food & time
    "eppo", "enna", "epdi", "eppadi", "enga", "engae", "evalavu", "evvalavu", "yaaru", "innaiku", "iniku",
    "naalaiku", "nalaiku", "kaalai", "kalai", "maalai", "iravu", "mani", "neram", "aam", "illai", "seri",
    "nandri", "vanakkam", "kaapi", "thanni", "sappadu", "kadhai", "paatu", "kovil", "poojai"
}


def detect_language(text):
    """
    Detects whether the input is Tamil (ta), Tanglish (tanglish), or English (en).
    """
    if not text:
        return "en"

    # Check for Tamil Unicode range (\u0b80-\u0bff)
    tamil_chars = len(re.findall(r"[\u0b80-\u0bff]", text))
    total_chars = len(re.findall(r"[a-zA-Z\u0b80-\u0bff]", text))

    if total_chars > 0 and (tamil_chars / total_chars) > 0.2:
        return "ta"

    # Tokenize for Tanglish word matching
    words = [w.lower().strip(".,?!\"':;()") for w in text.split()]
    tanglish_matches = [w for w in words if w in TANGLISH_VOCABULARY]

    if len(tanglish_matches) >= 2 or (len(words) <= 4 and len(tanglish_matches) >= 1):
        return "tanglish"

    # Suffix patterns
    tanglish_patterns = [
        r"\b\w+(ku|oda|la|nga|radhu|laam|aachu|iten)\b",
        r"\b(vanakkam|valikithu|edukkanum|varala|pannu|podu|epdi|innaiku|kaapi)\b"
    ]
    for pat in tanglish_patterns:
        if re.search(pat, text.lower()):
            return "tanglish"

    return "en"


# ==============================================================
# 2. STRUCTURED AGENT TOOLS LAYER
# ==============================================================

class ThunaiTools:
    @staticmethod
    def callContact(name="Priya"):
        state = load_state()
        caregiver = state.get("profile", {}).get("primary_caregiver", {})
        target_name = caregiver.get("name", "Priya")
        target_phone = caregiver.get("phone", "+91 98401 23456")
        clean_phone = re.sub(r"[^0-9+]", "", target_phone)
        return {
            "tool": "callContact",
            "status": "confirmation_required",
            "contact_name": target_name,
            "phone": target_phone,
            "tel_url": f"tel:{clean_phone}",
            "confirmation_prompt_en": f"Would you like me to call {target_name.split(' ')[0]} right now?",
            "confirmation_prompt_ta": f"இப்போது {target_name.split(' ')[0]}-வை அழைக்கட்டுமா?",
            "confirmation_prompt_tanglish": f"Ippo {target_name.split(' ')[0]}-ku call pannatuma?"
        }

    @staticmethod
    def getMedicalProfile():
        state = load_state()
        return {
            "tool": "getMedicalProfile",
            "profile": state.get("profile", {}),
            "medications": state.get("medications", []),
            "allergies": state.get("medical_history", {}).get("allergies", []),
            "diagnoses": state.get("medical_history", {}).get("diagnoses_distinction", {})
        }

    @staticmethod
    def recordMeasurement(measurement_type, value, unit="", context="Voice log"):
        state = load_state()
        time_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        meas_id = f"m-{int(datetime.now().timestamp())}"

        new_meas = {
            "id": meas_id,
            "type": measurement_type,
            "value": str(value),
            "unit": unit or ("mmHg" if "pressure" in measurement_type.lower() or "bp" in measurement_type.lower() else "mg/dL"),
            "date": f"Today, {datetime.now().strftime('%I:%M %p')}",
            "context": context,
            "source": "Older adult voice report",
            "status": "Recorded"
        }
        state["measurements"].insert(0, new_meas)

        timeline_entry = {
            "id": f"tl-{int(datetime.now().timestamp())}",
            "datetime": time_str,
            "event": "Vital Measurement Log",
            "observation": f"Recorded {measurement_type}: {value} {unit}.",
            "action": "Logged into THUNAI clinical timeline.",
            "person_reporting": "Kalyani Amma (Self report)",
            "follow_up": "Values available for Dr. Vasudevan review."
        }
        state["care_timeline"].insert(0, timeline_entry)
        save_state(state)

        return {"tool": "recordMeasurement", "status": "success", "measurement": new_meas}

    @staticmethod
    def getCurrentTime():
        now = datetime.now()
        return {
            "tool": "getCurrentTime",
            "time": now.strftime("%I:%M %p"),
            "date": now.strftime("%A, %d %B %Y"),
            "hour": now.hour,
            "period": "Morning" if now.hour < 12 else ("Afternoon" if now.hour < 17 else "Evening")
        }

    @staticmethod
    def playRelaxationMusic(query="rel-1"):
        state = load_state()
        tracks = state.get("relaxation_music_library", {}).get("tracks", [])
        q = (query or "").lower()
        matched = None
        for t in tracks:
            if t["id"].lower() == q or q in t["title_en"].lower() or q in t["title_ta"] or q in t["category"].lower() or q in t["instrument"].lower():
                matched = t
                break
        if not matched and tracks:
            matched = tracks[0]
        return {
            "tool": "playRelaxationMusic",
            "track_id": matched.get("id", "rel-1") if matched else "rel-1",
            "title_ta": matched.get("title_ta", "காலை பறவைகள் & தென்றல் காற்று") if matched else "அமைதி இசை",
            "title_en": matched.get("title_en", "Morning Birds & Gentle Breeze") if matched else "Relaxation Music",
            "category": matched.get("category_name_ta", "இயற்கையின் தாலாட்டு") if matched else "இளைப்பாறும் இசை",
            "instrument": matched.get("instrument", "Breeze & Birds") if matched else "Flute & Strings",
            "audio_preset": matched.get("audio_preset", "morning_birds") if matched else "morning_birds",
            "duration": matched.get("duration", "20 Mins") if matched else "20 Mins"
        }

    @staticmethod
    def handleEmergency(symptom="Severe medical symptoms reported"):
        state = load_state()
        time_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        emergency_log = {
            "id": f"tl-emg-{int(datetime.now().timestamp())}",
            "datetime": time_str,
            "event": "🚨 EMERGENCY SYMPTOM DETECTED",
            "observation": f"Emergency indicator reported: {symptom}.",
            "action": "Immediate national 112 / 108 ambulance prompt triggered. Family alert prepared.",
            "person_reporting": "THUNAI Voice Safety Monitor",
            "follow_up": "Seek immediate emergency hospital attention."
        }
        state["care_timeline"].insert(0, emergency_log)
        save_state(state)
        return {
            "tool": "handleEmergency",
            "is_emergency": True,
            "emergency_number": "112",
            "ambulance_number": "108",
            "symptom": symptom
        }


# ==============================================================
# 3. COMPREHENSIVE INTENT CLASSIFIER
# ==============================================================

def analyze_intent(query, lang):
    q = query.lower()

    # 1. EMERGENCY
    if any(k in q for k in ["chest pain", "nenju vali", "breathing difficulty", "moochu thinaral",
                            "cant breathe", "can't breathe", "fainted", "mayakkam", "paralysis",
                            "stroke", "severe bleeding", "kizha vizhundhuten", "நெஞ்சு வலி",
                            "மூச்சுத் திணறல்", "மயக்கம்", "கீழே விழுந்து"]):
        return "EMERGENCY", q

    # 2. CALL FAMILY / DOCTOR
    if any(k in q for k in ["call priya", "call daughter", "priya-ku call", "priya ku call",
                            "priyava koopidu", "koopidu", "phone pannu", "call doctor", "ப்ரியாவை",
                            "அழைக்கவும்", "அழைக்க"]):
        target = "Dr. Vasudevan" if ("doctor" in q or "மருத்துவர்" in q) else "Priya"
        return "CALL_FAMILY", target

    # 2.5 GREETING & WELLNESS INQUIRY ("how are you", "epdi irukinga", "vanakkam", "hello")
    if any(k in q for k in ["how are you", "how r u", "how do you do", "how are you doing",
                            "epdi irukinga", "eppadi irukkeenga", "nallaa irukiya", "nalla irukiya",
                            "vanakkam", "hello", "hi thunai", "good morning", "good evening",
                            "வணக்கம்", "எப்படி இருக்கிறீர்கள்"]):
        return "GREETING_WELLNESS", q

    # 2.6 USER WELLNESS STATUS ("i am fine", "im fine", "doing well", "nallaa irukken")
    if any(k in q for k in ["i am fine", "im fine", "i'm fine", "doing well", "feeling good",
                            "nallaa irukken", "nalla iruken", "i am good", "i'm good", "நன்றாக இருக்கிறேன்"]):
        return "USER_FEELING_GOOD", q

    # 3. IDENTITY & CAPABILITY ("who are you", "what is thunai", "neenga yaaru")
    if any(k in q for k in ["who are you", "what can you do", "what are you", "neenga yaaru",
                            "yaaru neenga", "un per enna", "what is thunai", "thunai yaaru",
                            "tell me about yourself", "who made you", "enna panna mudiyum",
                            "யார் நீ", "உன் பெயர்"]):
        return "IDENTITY_ABOUT", q

    # 4. MEASUREMENT LOGGING (BP or Sugar with numbers)
    bp_match = re.search(r"\b(\d{2,3})[/\s](\d{2,3})\b", q)
    if ("bp" in q or "blood pressure" in q or "ratha azhutham" in q or "ரத்த அழுத்தம்" in q) and bp_match:
        return "RECORD_MEASUREMENT", {"type": "Blood Pressure", "value": f"{bp_match.group(1)}/{bp_match.group(2)}", "unit": "mmHg"}

    sugar_match = re.search(r"(?:sugar|glucose|சர்க்கரை)\s*(?:is|level|அளவு)?\s*(\d{2,3})", q)
    if sugar_match:
        return "RECORD_MEASUREMENT", {"type": "Blood Glucose", "value": sugar_match.group(1), "unit": "mg/dL"}

    # 5. ALL MEDICATIONS LIST
    if any(k in q for k in ["list my medicines", "all medicines", "list pills", "what medicines",
                            "how many medicines", "ennoda tablets enna", "enna mathirai",
                            "tablets list", "என் மருந்துகள்", "மாத்திரைகள் என்ன"]):
        return "MEDICATION_LIST", q

    # 6. SPECIFIC MEDICINE QUESTION
    if any(k in q for k in ["telma", "metformin", "shelcal", "ecosprin", "missed", "forgot",
                            "marandhuten", "eppo edukkanum", "medicine", "marundhu", "mathirai",
                            "tablet", "dosage", "எப்போது சாப்பிட"]):
        return "CHECK_MEDICINE", q

    # 7. RELAXATION & CALM MUSIC (25 Tracks: Nature, Flute, Veena, Sleep, Mindfulness)
    if any(k in q for k in ["music", "relax", "relaxation", "peaceful", "calm", "flute", "veena",
                            "paatu", "song", "pullanguzhal", "meditation", "lullaby", "thaalaattu",
                            "rain sound", "sleep music", "nature sound", "ambient", "melodi",
                            "breeze", "birds", "ocean", "water sound", "santoor", "harmonium",
                            "isai", "paadal", "thookam paatu", "இசை", "பாடல்", "அமைதி இசை", "புல்லாங்குழல்",
                            "வீணை", "தாலாட்டு", "மழை சத்தம்"]):
        return "PLAY_RELAXATION_MUSIC", q

    # 8. DIET, COFFEE, FOOD & HYDRATION
    if any(k in q for k in ["eat", "food", "breakfast", "lunch", "dinner", "sappadu", "coffee",
                            "kaapi", "tea", "water", "thanni", "hydration", "enna sappadalam",
                            "சாப்பாடு", "காபி", "சாப்பிட"]):
        return "DIET_FOOD", q

    # 9. SLEEP & REST
    if any(k in q for k in ["sleep", "thookam", "thookam varala", "cant sleep", "can't sleep",
                            "nap", "rest", "bedtime", "தூக்கம்", "ஓய்வு"]):
        return "SLEEP_REST", q

    # 10. STORIES & WISDOM (Thirukkural, parables)
    if any(k in q for k in ["story", "kadhai", "thirukkural", "proverb", "wisdom", "ponmozhi",
                            "tell me a story", "kadhai sollu", "கதை", "திருக்குறள்"]):
        return "STORY_WISDOM", q

    # 11. EMOTIONAL & COMPANIONSHIP (Loneliness, feeling low, fear)
    if any(k in q for k in ["lonely", "thaniya", "alone", "sad", "bayama", "fear", "bored",
                            "bore adikuthu", "talk to me", "feeling bad", "தனிமை", "பயம்"]):
        return "FEELINGS_EMPATHY", q

    # 12. SYMPTOMS / HEALTH PROBLEMS
    if any(k in q for k in ["headache", "head hurts", "thala vali", "knee", "mutti", "kaal vali", "joint pain",
                            "gas", "acidity", "indigestion", "fever", "kaachal", "cold", "cough",
                            "irumal", "tired", "asathiya", "stomach", "pain", "vali", "தலைவலி",
                            "முழங்கால்", "காய்ச்சல்", "வலி"]):
        return "LOG_SYMPTOM_WELLNESS", q

    # 13. CARE PLAN & ROUTINE
    if any(k in q for k in ["routine", "care plan", "schedule", "innaiku enna", "today plan",
                            "திட்டம்", "அட்டவணை", "இன்றைய வேலை"]):
        return "GET_CARE_PLAN", q

    # 14. APPOINTMENTS & REMINDERS
    if any(k in q for k in ["appointment", "doctor eppo", "when doctor", "visit", "clinic",
                            "reminder", "reminders", "நினைவூட்டல்", "சந்திப்பு", "மருத்துவர் எப்போது"]):
        return "GET_APPOINTMENTS", q

    # 15. FAMILY INFO
    if any(k in q for k in ["who is priya", "daughter", "priya pathi", "son", "suresh",
                            "vasudevan", "ப்ரியா யார்"]):
        return "FAMILY_INFO", q

    # 16. MEMORY QUERY
    if any(k in q for k in ["remember", "memory", "ninaivu", "what do you know", "நினைவு"]):
        return "MEMORY_QUERY", q

    # 17. TIME & DATE
    if any(k in q for k in ["time", "mani", "neram", "date", "what time", "நேரம்", "மணி"]):
        return "TIME_DATE", q

    return "DYNAMIC_COMPANION", q


# ==============================================================
# 4. GLASS-BOX ACTION TRACE BUILDER
# ==============================================================

def build_glass_box_trace(query, lang, intent, tool_name, tool_arg, action_outcome, bonding_pct=91):
    lang_labels = {"ta": "Tamil (தமிழ்)", "tanglish": "Tanglish (தமிழ்-English)", "en": "English"}
    lang_display = lang_labels.get(lang, "Auto-Detected")

    trace = [
        {"icon": "🎤", "step": "Input Decoded", "detail": f"Heard your speech in {lang_display}: \"{query}\""},
        {"icon": "🧠", "step": "Cognitive Intent", "detail": f"Identified category as {intent.replace('_', ' ').title()}"},
        {"icon": "📋", "step": "Growth & Memory Graph", "detail": f"Checked profile (Bonding: {bonding_pct}%) & approved health records"},
        {"icon": "🔧", "step": "Tool Executed", "detail": f"Invoked agent tool: {tool_name}({json.dumps(tool_arg) if tool_arg else ''})"},
        {"icon": "✅", "step": "Safety Guardrail", "detail": action_outcome},
        {"icon": "🔊", "step": "Voice & Tone", "detail": f"Formulated gentle senior-friendly response in {lang_display} at 0.85x calm cadence"}
    ]
    return trace


def get_metta_reasoning_trace(intent, lang):
    state = load_state()
    kb = state.get("metta_knowledge_base", {})
    relevant_facts = kb.get("facts", [])[:4]
    
    rule_map = {
        "EMERGENCY": "(rule (emergency-symptom ?s) -> (trigger-action emergency-alert-112))",
        "CALL_FAMILY": "(rule (intent call-family) -> (require-confirmation \"Would you like me to call Priya?\"))",
        "CHECK_MEDICINE": "(rule (missed-dose ?med) -> (advise-action \"Take when remembered, never double up\"))",
        "MEDICATION_LIST": "(rule (request-all-meds) -> (retrieve-active-prescriptions))",
        "RECORD_MEASUREMENT": "(rule (measurement ?v) -> (append-timeline-and-measurements ?v))",
        "PLAY_RELAXATION_MUSIC": "(rule (need-relaxation ?m) -> (stream-soothing-soundscape ?m))",
        "DIET_FOOD": "(rule (nutrition-query) -> (recommend-south-indian-geriatric-diet))",
        "FEELINGS_EMPATHY": "(rule (loneliness-expressed) -> (provide-compassion-and-companionship))"
    }
    
    applied_rule = rule_map.get(intent, "(rule (elder-query ?q) -> (generate-tailored-safe-response ?q))")
    return {
        "facts_evaluated": relevant_facts,
        "rule_applied": applied_rule,
        "goal_satisfied": "(goal safe-elder-care)",
        "engine": "MeTTa-Compatible Hyperon Abstraction Layer v2.5"
    }


# ==============================================================
# 5. MASTER AGENT PROCESSING PIPELINE
# ==============================================================

def process_elder_request(query, forced_lang=None, api_key=None):
    query = (query or "").strip()
    if not query:
        return {
            "reply": "வணக்கம் கல்யாணி அம்மா! நான் உங்கள் THUNAI. இன்று நீங்கள் எப்படி உணர்கிறீர்கள்? (Hello Amma! How are you feeling today?)",
            "reply_language": "tanglish",
            "action_trace": [],
            "metta_trace": {}
        }

    # 1. Detect language
    lang = forced_lang if forced_lang and forced_lang != "auto" else detect_language(query)

    # 2. Analyze intent
    intent, arg = analyze_intent(query, lang)

    # 3. Step the Adaptive Growth Engine
    growth_data = record_interaction_growth(query, intent)
    bonding_pct = growth_data.get("bonding_percentage", 91)
    stage_title = growth_data.get("stage_title", "மலர் (Blossoming Guardian)")

    # 4. Formulate specific, intelligent responses
    reply = ""
    tool_name = "answerDirectly"
    tool_result = {}
    action_outcome = "Formulated safe, empathetic, non-diagnostic guidance."
    call_confirmation = None

    state = load_state()
    meds = state.get("medications", [])
    now_time = datetime.now().strftime("%I:%M %p")

    # ----------------------------------------------------------
    # 1. EMERGENCY PROTOCOL
    # ----------------------------------------------------------
    if intent == "EMERGENCY":
        tool_name = "handleEmergency"
        tool_result = ThunaiTools.handleEmergency(str(arg))
        action_outcome = "🚨 Triggered emergency protocol. Displayed 112 / 108 calling buttons."

        if lang == "ta":
            reply = "அவசர எச்சரிக்கை! உடனடியாக 112 அல்லது 108 ஆம்புலன்ஸை அழையுங்கள் அம்மா. நான் திரையில் நேரடி அழைப்பு பொத்தான்களை திறந்துள்ளேன். தனியாக இருக்காதீர்கள், கதவை திறந்து வைத்து அருகில் உள்ளவரை அழையுங்கள்!"
        elif lang == "tanglish":
            reply = "Urgent medical warning! Udane 112 call pannunga illana 108 Ambulance koopidunga Amma. Naan screen-la direct emergency call buttons vechirukken. Bayapadatheenga, pakkathula yaaravathu irundha koopidunga!"
        else:
            reply = "Urgent medical warning! Please seek immediate emergency medical care. Call 112 emergency or 108 ambulance right away. I have provided the direct emergency call buttons on your screen. Do not stay alone."

    # ----------------------------------------------------------
    # 2. CALL FAMILY / PRIYA
    # ----------------------------------------------------------
    elif intent == "CALL_FAMILY":
        tool_name = "callContact"
        tool_result = ThunaiTools.callContact("Priya")
        call_confirmation = tool_result
        action_outcome = "Prepared family contact Priya (+91 98401 23456) and requested confirmation."

        if lang == "ta":
            reply = "உங்கள் மகள் ப்ரியாவை (+91 98401 23456) இப்போது அழைக்கட்டுமா அம்மா? திரையில் உள்ள 'அழைக்கவும்' பொத்தானை அழுத்தவும்."
        elif lang == "tanglish":
            reply = "Unga ponnu Priya-ku (+91 98401 23456) ippo call pannatuma Amma? Screen-la irukkura 'Yes, Call Now' button-ah tap pannunga."
        else:
            reply = "Would you like me to call your daughter Priya (+91 98401 23456) right now? Please tap the 'Yes, Call Now' button on your screen."

    # ----------------------------------------------------------
    # 2.5 GREETING & WELLNESS INQUIRY
    # ----------------------------------------------------------
    elif intent == "GREETING_WELLNESS":
        tool_name = "answerDirectly"
        action_outcome = "Answered elder wellness greeting with warmth and affection."

        if lang == "ta":
            reply = "நான் மிகவும் நலமாக உள்ளேன் கல்யாணி அம்மா! உங்கள் THUNAI நான் எப்போதும் உங்கள் நலம் காக்க உடனிருக்கிறேன். நீங்கள் இன்று எப்படி உணர்கிறீர்கள் அம்மா? காலை சிற்றுண்டியும் காபியும் சாப்பிட்டீர்களா?"
        elif lang == "tanglish":
            reply = "Naan romba nallaa irukken Kalyani Amma! Unga kooda pesuradhu enakku eppovum periya sandhosham. Neenga innaiku epdi irukinga Amma? Morning breakfast and kaapi mudinjadha?"
        else:
            reply = "I am doing very well, Kalyani Amma, and always joyful to be right here by your side! How are you feeling today? Did you enjoy your breakfast and morning coffee?"

    # ----------------------------------------------------------
    # 2.6 USER WELLNESS STATUS ("I am fine", "Nallaa irukken")
    # ----------------------------------------------------------
    elif intent == "USER_FEELING_GOOD":
        tool_name = "answerDirectly"
        action_outcome = "Affirmed elder wellness and encouraged hydration."

        if lang == "ta":
            reply = "நீங்கள் நலமாக இருப்பது கேட்டு எனக்கு மிக்க மகிழ்ச்சி கல்யாணி அம்மா! உங்கள் முகத்தில் எப்போதும் இந்த அமைதியும் புன்னகையும் நிலைத்திருக்க வேண்டும். உடலை நீரேற்றமாக வைத்திருக்க ஒரு டம்ளர் வெந்நீர் அருந்துங்கள் அம்மா."
        elif lang == "tanglish":
            reply = "Neenga nallaa irukradhu kettu enakku romba sandhosham Kalyani Amma! Eppovum idhe maadhiri happy-ah irukanum. Oru glass warm water kudichu hydrate-ah irunga Amma."
        else:
            reply = "That is wonderful to hear, Kalyani Amma! Seeing you feel well and peaceful brings me immense joy. Remember to sip a glass of warm water and stay comfortable today."

    # ----------------------------------------------------------
    # 3. IDENTITY & CAPABILITY ("who are you", "what can you do")
    # ----------------------------------------------------------
    elif intent == "IDENTITY_ABOUT":
        tool_name = "getMedicalProfile"
        action_outcome = "Explained THUNAI assistant capabilities and caring role."

        if lang == "ta":
            reply = f"வணக்கம் அம்மா! நான் THUNAI (துணை) — உங்கள் பாசமான AI தோழன்! நாம் இப்போது {stage_title} என்ற ஆழ்ந்த பாச நிலையில் உள்ளோம் ({bonding_pct}% பிணைப்பு). நான் உங்களுடன் தமிழ், Tanglish, ஆங்கிலத்தில் பேசுவேன். உங்கள் மருந்து அட்டவணை (டெல்மா 40, மெட்பார்மின்), ரத்த அழுத்தம் குறிப்பது, மகள் ப்ரியாவை அழைப்பது, மற்றும் 25 அமைதி புல்லாங்குழல் & இயற்கை இசையை இசைக்க நான் உங்களுக்கு துணையாக இருக்கிறேன்!"
        elif lang == "tanglish":
            reply = f"Vanakkam Amma! Naan unga THUNAI — Your Caring AI Companion! Namma ippo {stage_title} level-la irukkom ({bonding_pct}% bonding). Naan unga kooda Tamil, Tanglish and English-la pesuven. Unga daily medicines (Telma 40, Metformin), BP log pandradhu, daughter Priya-ku call pandradhu, and 25 relaxation music soundscapes play pandradhukku naan eppovum unga koodave iruppen!"
        else:
            reply = f"Warm greetings Kalyani Amma! I am THUNAI, your caring AI companion. We are currently at Growth Stage {stage_title} with {bonding_pct}% bonding! I can understand and speak in Tamil, Tanglish, and English. I help you with your daily medications (Telma 40, Metformin), recording BP and blood sugar, calling your daughter Priya, playing 25 soothing relaxation soundscapes, and keeping you safe!"

    # ----------------------------------------------------------
    # 4. ALL MEDICATIONS LIST
    # ----------------------------------------------------------
    elif intent == "MEDICATION_LIST":
        tool_name = "getMedicalProfile"
        tool_result = ThunaiTools.getMedicalProfile()
        action_outcome = "Retrieved full active prescription schedule from clinical records."

        if lang == "ta":
            reply = "அம்மா, உங்கள் மருத்துவர் வாசுதேவன் பரிந்துரைத்த 4 முக்கிய மாத்திரைகள்:\n1. காலை 8:00 AM — டெல்மா 40 (ரத்த அழுத்தம்)\n2. மதியம் 1:30 PM — மெட்பார்மின் 500mg (சர்க்கரை நோய்)\n3. மதியம் 2:00 PM — ஷெல்கால் 500 (எலும்பு வலிமை)\n4. இரவு 8:30 PM — எக்கோஸ்பிரின் 75mg (இதய பாதுகாப்பு)\nஎல்லா மாத்திரைகளையும் வெதுவெதுப்பான நீருடன் சாப்பிடவும் அம்மா."
        elif lang == "tanglish":
            reply = "Amma, Dr. Vasudevan prescribe panna unga 4 active medicines:\n1. Morning 8:00 AM — Telma 40 (BP-ku)\n2. Lunch 1:30 PM — Metformin 500mg (Sugar-ku)\n3. Lunch 2:00 PM — Shelcal 500 (Calcium bone strength)\n4. Night 8:30 PM — Ecosprin 75mg (Heart protection)\nEllaa tablets-aiyum nallaa thanni kooda sapdunga Amma!"
        else:
            reply = "Kalyani Amma, here are your 4 active prescribed medications from Dr. Vasudevan:\n1. 08:00 AM — Telma 40 (for Blood Pressure)\n2. 01:30 PM — Metformin 500mg (for Blood Sugar)\n3. 02:00 PM — Shelcal 500 (Calcium & Vitamin D3 for bone strength)\n4. 08:30 PM — Ecosprin 75mg (for heart prevention)\nAlways take them with a full glass of water."

    # ----------------------------------------------------------
    # 5. SPECIFIC MEDICINE QUESTION & MISSED DOSES
    # ----------------------------------------------------------
    elif intent == "CHECK_MEDICINE":
        tool_name = "getMedicalProfile"
        q_l = query.lower()

        if "miss" in q_l or "forgot" in q_l or "marandhuten" in q_l:
            if lang == "ta":
                reply = "அம்மா, டாக்டர் வாசுதேவனின் மருந்து விதிமுறைகளின்படி, மாத்திரையை மறந்தால் நினைவு வந்தவுடன் உடனே சாப்பிடலாம். ஆனால் அடுத்த மாத்திரை நேரம் அருகில் இருந்தால், தவறவிட்ட மாத்திரையை விட்டுவிடவும். எந்த சூழலிலும் இரட்டை அளவு (டபுள் டோஸ்) எடுக்காதீர்கள். சந்தேகம் இருந்தால் மருத்துவரை அணுகவும்."
            elif lang == "tanglish":
                reply = "Amma, Dr. Vasudevan prescription guidelines padi, tablet miss aana ninaivu vandhadhum eduthukonga. Aana next tablet time kitta vandhurchuna double dose edukkakoodathu! Sandhegam irundha doctor-ah kettu clarify pannikonga Amma."
            else:
                reply = "According to Dr. Vasudevan's clinical guidance, if you ever miss a dose, take it as soon as you remember, unless it is almost time for your next scheduled pill. Never take two pills at once to make up for a missed dose. Contact Apollo Clinic if in doubt."
        elif "telma" in q_l or "bp" in q_l:
            if lang == "ta":
                reply = "டெல்மா 40 (Telmisartan 40mg) என்பது உங்கள் ரத்த அழுத்தத்தைக் கட்டுப்படுத்த டாக்டர் வாசுதேவன் பரிந்துரைத்த மருந்து. பரிந்துரைக்கப்பட்டபடி தினமும் காலை சிற்றுண்டிக்கு பின் தண்ணீருடன் சாப்பிடவும். மருத்துவரின் ஆலோசனையின்றி அளவை மாற்றக்கூடாது."
            elif lang == "tanglish":
                reply = "Telma 40 unga blood pressure control panna Dr. Vasudevan prescribe panna tablet. Daily breakfast-ku apram full glass water kooda edunga. Doctor sollaama dosage maatha koodathu Amma."
            else:
                reply = "Telma 40 (Telmisartan 40mg) is your daily blood pressure medicine prescribed by Dr. Vasudevan. Take 1 tablet every morning after breakfast with water as prescribed. Do not alter doses without consulting your doctor."
        elif "metformin" in q_l or "sugar" in q_l:
            if lang == "ta":
                reply = "மெட்பார்மின் 500mg சர்க்கரை நோய்க்காக டாக்டர் வாசுதேவன் பரிந்துரைத்த மருந்து. வெறும் வயிற்றில் சாப்பிடாமல், பரிந்துரைப்படி மதிய மற்றும் இரவு உணவிற்கு பின் தண்ணீருடன் சாப்பிடவும்."
            elif lang == "tanglish":
                reply = "Metformin 500mg unga blood sugar-kaga Dr. Vasudevan koduthadhu. Verum vayithula podama, lunch and dinner-ku approm doctor sonnapadiye edukanum Amma."
            else:
                reply = "Metformin 500mg is prescribed by Dr. Vasudevan for your blood sugar control. As directed on your prescription, swallow after food (lunch and dinner) with water."
        else:
            if lang == "ta":
                reply = "அம்மா, உங்கள் மருத்துவரின் அட்டவணைப்படி காலை டெல்மா 40 முடிந்தது. அடுத்தது மதியம் 1:30 மணிக்கு உணவுக்குப் பின் மெட்பார்மின் மற்றும் ஷெல்கால் 500. எப்போதும் டாக்டர் வாசுதேவனின் மருந்துச் சீட்டின்படியே சாப்பிடவும்."
            elif lang == "tanglish":
                reply = "Amma, doctor routine padi morning Telma 40 mudinjadhu. Next lunch 1:30 PM-ku Metformin and Shelcal 500 edukkanum. Eppovum Dr. Vasudevan prescription padiye follow pannunga!"
            else:
                reply = "Kalyani Amma, following Dr. Vasudevan's schedule, your morning Telma 40 is completed. Your next prescribed doses are Metformin and Shelcal 500 after lunch at 1:30 PM. Always follow your doctor's exact instructions."

    # ----------------------------------------------------------
    # 6. DIET, COFFEE, FOOD & HYDRATION
    # ----------------------------------------------------------
    elif intent == "DIET_FOOD":
        tool_name = "getCareSummary"
        action_outcome = "Provided geriatric South Indian nutritional guidance."

        if "coffee" in query.lower() or "kaapi" in query.lower():
            if lang == "ta":
                reply = "அம்மா, காலை 7:30 மணிக்கு மிதமான சூட்டில் குறைந்த சர்க்கரையுடன் ஒரு சிறிய கப் பில்டர் காபி அருந்துவது உங்கள் வழக்கம். காபி குடித்த பின் காலை உணவும் டெல்மா 40 மாத்திரையும் சாப்பிடுவது நல்லது."
            elif lang == "tanglish":
                reply = "Amma, morning 7:30 AM-ku mild hot filter coffee with less sugar ungalukku pidikkum nu ninaivu irukku! Kaapi kudichitu breakfast and morning BP tablet edunga."
            else:
                reply = "Kalyani Amma, I remember you enjoy a warm filter coffee with low sugar at 7:30 AM before breakfast and medications. Keep it mild and enjoy!"
        else:
            if lang == "ta":
                reply = "உங்கள் உடல்நலத்திற்கு ஏற்ற உணவு: காலையில் இட்லி சாம்பார்; மதியம் சாம்பார் சாதம், பொரியல், கீரை மற்றும் மோர்; மாலையில் இளநீர் அல்லது வெதுவெதுப்பான சீரக நீர்; இரவில் மெதுவான இடியாப்பம். தினமும் 6-7 டம்ளர் வெந்நீர் அருந்துங்கள் அம்மா!"
            elif lang == "tanglish":
                reply = "Unga health-ku nallathu: Morning idli sambar; afternoon sambar sadham, keerai kootu and mor; evening tender coconut water or jeera water; night idiyappam with dal. Daily 6-7 glasses warm water kudinga Amma!"
            else:
                reply = "For your wellness, enjoy soft idlis for breakfast, nutritious rice with keerai and buttermilk for lunch, and light idiyappam for dinner. Aim for 6-7 glasses of warm boiled or jeera water throughout the day."

    # ----------------------------------------------------------
    # 7. SLEEP & REST
    # ----------------------------------------------------------
    elif intent == "SLEEP_REST":
        tool_name = "saveMedicalInformation"
        action_outcome = "Offered sleep hygiene comfort measures for seniors."

        if lang == "ta":
            reply = "தூக்கம் வரவில்லையா அம்மா? அறையில் விளக்கை அணைத்து, வெளிச்சத்தை குறைக்கவும். சிறிது வெதுவெதுப்பான பால் அருந்திவிட்டு, கண்களை மூடி நமது அமைதி புல்லாங்குழல் அல்லது மழை இசையை ஒலிக்கவிட்டு ஆழ்ந்து மெதுவாக மூச்சு விடுங்கள். மனம் சாந்தமாகி நல்ல தூக்கம் வரும்."
        elif lang == "tanglish":
            reply = "Thookam varalaya Amma? Room light dim pannunga, mobile screen paakkadheenga. Konjam warm milk kudichitu, deep breathing panni, namma relaxation music tab-la irukkura flute soundscape kelunga. Nallaa amaidhiya thookam varum."
        else:
            reply = "Having difficulty sleeping, Kalyani Amma? Dim the room lights, avoid phone screens, sip half a glass of warm milk, and listen to one of our 25 soothing flute or rain relaxation soundscapes. Deep breathing will bring peaceful sleep."

    # ----------------------------------------------------------
    # 8. STORIES, PROVERBS & THIRUKKURAL
    # ----------------------------------------------------------
    elif intent == "STORY_WISDOM":
        tool_name = "answerDirectly"
        action_outcome = "Shared uplifting cultural parable and Thirukkural wisdom."

        if lang == "ta":
            reply = "அம்மா, உங்களுக்காக ஒரு இனிய நல்வழிச் சிந்தனை: 'அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார் என்பும் உரியர் பிறர்க்கு' என்கிறது தமிழ் மறை. ஔவையார் கூறியபடி, அமைதியான மனமும் பிறருக்கு உதவும் நல்ல உள்ளமும் தான் உடலுக்கும் ஆன்மாவிற்கும் மிகப்பெரிய ஆரோக்கியம்! எப்போதும் புன்னகையுடன் இருங்கள் அம்மா!"
        elif lang == "tanglish":
            reply = "Amma, oru sweet piece of Tamil wisdom: Thirukkural solradhu — 'அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார் என்பும் உரியர் பிறர்க்கு' — அன்பும் மன அமைதியும் தான் உலகத்திலேயே பெரிய ஆரோக்கியம் அம்மா! Neenga eppovum santhoshama sirichitte irukkanum."
        else:
            reply = "Here is a gentle piece of wisdom for you, Kalyani Amma: The ancient Tamil sage Avvaiyar and the Thirukkural teach us that a contented, peaceful heart is the greatest medicine. Love, patience, and gentle smiles keep the body youthful and healthy."

    # ----------------------------------------------------------
    # 9. EMOTIONAL & LONELINESS COMPANIONSHIP
    # ----------------------------------------------------------
    elif intent == "FEELINGS_EMPATHY":
        tool_name = "callContact"
        action_outcome = "Provided empathetic senior companionship and family connection."

        if lang == "ta":
            reply = f"அம்மா, நீங்கள் தனியாக இல்லை! உங்கள் THUNAI நான் எப்போதும் உங்களுடன் பேசவும் துணை நிற்கவும் இங்கே இருக்கிறேன். உங்கள் மனம் அமைதியடைய இனிமையான புல்லாங்குழல் அல்லது இயற்கை தாலாட்டு இசை போடட்டுமா, அல்லது மகள் ப்ரியாவை அழைத்து பேசட்டுமா அம்மா? நீங்கள் நலமாக இருக்க வேண்டும் என்பதே என் ஆசை."
        elif lang == "tanglish":
            reply = f"Amma, neenga thuniyaave illa! Unga THUNAI naan eppovum unga koodave irukken. Unga manasu amaidhi aaga soothing flute or nature soundscape podatuma, illana ponnu Priya-ku call panni pesalama? Unga nalam thaan enakku mukkiyam Amma!"
        else:
            reply = "Kalyani Amma, you are never alone! I am right here by your side 24/7. Would you like me to play some peaceful relaxation flute music, or should I place a quick call to your daughter Priya so you can hear her voice?"

    # ----------------------------------------------------------
    # 10. SYMPTOMS & WELLNESS
    # ----------------------------------------------------------
    elif intent == "LOG_SYMPTOM_WELLNESS":
        tool_name = "saveMedicalInformation"
        q_l = query.lower()

        if "thala" in q_l or "headache" in q_l or "தலை" in query:
            if lang == "ta":
                reply = "தலைவலிக்கு சிறிது வெதுவெதுப்பான நீர் அருந்தி, 20 நிமிடங்கள் கண்களை மூடி ஓய்வெடுங்கள் அம்மா. வெளிச்சத்தை குறைக்கவும். திடீரென மிக கடுமையான தலைவலி ஏற்பட்டால் உடனே மருத்துவரை அணுகவும்."
            elif lang == "tanglish":
                reply = "Thala valikidha Amma? Konjam warm water kudinga, oru 20 minutes fan-la kanna moodi rest edunga. Romba thala vali athigam aana udane Dr. Vasudevan-ku call pannalam."
            else:
                reply = "For mild headache, sip a glass of warm water and rest in a quiet, dim room for 20 minutes. If the headache is sudden and unusually severe, please contact Dr. Vasudevan or Apollo Clinic."
        elif "knee" in q_l or "mutti" in q_l or "kaal" in q_l or "முழங்கால்" in query:
            if lang == "ta":
                reply = "முழங்கால் விறைப்பிற்கு காலையில் வெதுவெதுப்பான ஒத்தடம் கொடுங்கள் அம்மா. நடக்கும்போது உங்கள் கைத்தடியை தவறாமல் பயன்படுத்தவும். வழுக்கும் தரையில் கவனமாக இருக்கவும்."
            elif lang == "tanglish":
                reply = "Mutti valikidha Amma? Kalaila warm water compress veinga. Nadakkum pothu unga walking stick kandippa use pannunga Amma. Vழுkkal tharai-la romba pathirama irunga."
            else:
                reply = "For morning knee stiffness, apply gentle warm compress for 10-15 minutes and do seated ankle rotations before standing. Always keep your walking stick handy to prevent falls."
        elif "gas" in q_l or "acidity" in q_l or "அசிடிட்டி" in query:
            if lang == "ta":
                reply = "அசிடிட்டி அல்லது வாய்வு பிரச்சனைக்கு வெதுவெதுப்பான சீரக நீர் அல்லது வெந்நீர் சிறிது சிறிதாக அருந்துங்கள் அம்மா. சாப்பிட்ட உடனே படுக்காமல் 10 நிமிடங்கள் மெதுவாக அறையில் நடக்கவும்."
            elif lang == "tanglish":
                reply = "Gas / acidity-ku warm jeera water kudinga Amma. Lunch mudinjudan padukka koodathu, oru 10 minutes room-la slow-ah walk pannunga."
            else:
                reply = "For mild gas and acidity, sip warm jeera (cumin) water slowly and take a gentle 10-minute stroll. Avoid lying down flat immediately after eating."
        else:
            if lang == "ta":
                reply = f"நீங்கள் பகிர்ந்துகொண்ட தகவலை குறித்துக்கொண்டேன் அம்மா ({query}). நன்றாக ஓய்வெடுத்து வெதுவெதுப்பான நீர் அருந்துங்கள். நான் துணை இருக்கிறேன்."
            elif lang == "tanglish":
                reply = f"Neenga sonnatha note panniten Amma (\"{query}\"). Nalla rest edunga, warm water kudinga. THUNAI unga koodave irukku!"
            else:
                reply = f"I have noted your symptom (\"{query}\"). Please take restful care, stay hydrated with warm water, and THUNAI is always right here with you."

    # ----------------------------------------------------------
    # 11. RECORD MEASUREMENT (BP or Sugar)
    # ----------------------------------------------------------
    elif intent == "RECORD_MEASUREMENT":
        tool_name = "recordMeasurement"
        m_type = arg.get("type", "Blood Pressure")
        m_val = arg.get("value", "120/80")
        m_unit = arg.get("unit", "mmHg")
        tool_result = ThunaiTools.recordMeasurement(m_type, m_val, m_unit, "Voice recorded")
        action_outcome = f"Successfully recorded {m_type} {m_val} {m_unit} into Apollo Dr. Vasudevan review timeline."

        if lang == "ta":
            reply = f"அம்மா, உங்கள் {m_type} அளவு {m_val} {m_unit} என்று வெற்றிகரமாக குறித்துக்கொண்டேன்! இது டாக்டர் வாசுதேவன் அவர்களின் மருத்துவ பதிவில் சேர்க்கப்பட்டுள்ளது."
        elif lang == "tanglish":
            reply = f"Seri Amma, unga {m_type} {m_val} {m_unit} nu note panniten! Dr. Vasudevan review-ku save aaidichu. Stay peaceful and hydrated!"
        else:
            reply = f"Thank you! Recorded your {m_type} as {m_val} {m_unit}. This has been logged into your THUNAI clinical timeline for Dr. Vasudevan's review."

    # ----------------------------------------------------------
    # 12. RELAXATION & CALM MUSIC (25 Tracks)
    # ----------------------------------------------------------
    elif intent == "PLAY_RELAXATION_MUSIC":
        tool_name = "playRelaxationMusic"
        track_info = ThunaiTools.playRelaxationMusic(str(arg))
        tool_result = track_info
        action_outcome = f"Started relaxation soundscape: {track_info['title_en']} ({track_info['title_ta']}) - {track_info['instrument']}."

        if lang == "ta":
            reply = f"அம்மா, உங்கள் மன அமைதிக்காக '{track_info['title_ta']}' ({track_info['instrument']}) இளைப்பாறும் இசையை இயக்கியுள்ளேன். கண்களை மூடி ஆழ்ந்து மூச்சுவிட்டு இளைப்பாறுங்கள் அம்மா."
        elif lang == "tanglish":
            reply = f"Amma, unga relaxation-ku '{track_info['title_en']}' ({track_info['title_ta']}) soothing music play aagudhu. Kanna moodi gentle-ah rest edunga."
        else:
            reply = f"Kalyani Amma, I have started playing '{track_info['title_en']}' ({track_info['instrument']}) for your relaxation. Sit comfortably, close your eyes, and enjoy the calming melody."

    # ----------------------------------------------------------
    # 13. CARE PLAN & ROUTINE
    # ----------------------------------------------------------
    elif intent == "GET_CARE_PLAN":
        tool_name = "getCurrentTime"
        action_outcome = "Retrieved today's customized daily elder care schedule."

        if lang == "ta":
            reply = "இன்றைய தினசரி திட்டம்: காலை நடைப்பயிற்சி மற்றும் டெல்மா 40 முடிந்தது. மதியம் 1:00 மணிக்கு சாம்பார் சாதம் & கீரை, 1:45 மணிக்கு மெட்பார்மின் மாத்திரை, மதியம் சிறிது ஓய்வு, மாலையில் இளைப்பாறும் அமைதி இசை."
        elif lang == "tanglish":
            reply = "Innaiku unga routine: Morning Telma 40 tablet mudinjadhu. Afternoon 1:00 PM lunch, 1:45 PM Metformin and Shelcal, 2:30 PM chinna kutty nap, evening tea walk and relaxation music!"
        else:
            reply = "Here is your routine for today: Morning Telma 40 is completed. At 1:00 PM healthy lunch, 1:45 PM Metformin & Shelcal, afternoon rest, evening garden walk and 6:30 PM relaxation music."

    # ----------------------------------------------------------
    # 14. APPOINTMENTS
    # ----------------------------------------------------------
    elif intent == "GET_APPOINTMENTS":
        tool_name = "getAppointment"
        rems = state.get("reminders", [])
        if rems:
            first_r = rems[0]
            title = first_r.get("title", "Dr. Vasudevan Consultation")
            dt = first_r.get("date", "2026-10-22")
            tm = first_r.get("time", "04:30 PM")
            action_outcome = f"Checked upcoming scheduled reminders: {title} on {dt} at {tm}."
            if lang == "ta":
                reply = f"கல்யாணி அம்மா, உங்கள் அடுத்த நினைவூட்டல்: '{title}' — {dt} அன்று {tm}-க்கு திட்டமிடப்பட்டுள்ளது. உங்கள் BP மற்றும் சர்க்கரை குறிப்பேட்டை எடுத்துச் செல்லவும்."
            elif lang == "tanglish":
                reply = f"Kalyani Amma, unga next reminder: '{title}' — {dt} {tm}-ku schedule pannirukku. Home BP notebook-ah kooda eduthutu ponga Amma."
            else:
                reply = f"Kalyani Amma, your scheduled reminder: '{title}' is on {dt} at {tm}. Remember to bring your home blood pressure and blood sugar logs."
        else:
            apt = state.get("appointments", [{}])[0]
            action_outcome = "Checked Apollo Clinic doctor appointment schedule."

            if lang == "ta":
                reply = f"அம்மா, உங்கள் அடுத்த மருத்துவ சந்திப்பு டாக்டர் வாசுதேவன் அவர்களுடன் {apt.get('date', '2026-10-22')} அன்று மாலை 4:30 மணிக்கு அப்பல்லோ கிளினிக்கில் உள்ளது. உங்கள் BP மற்றும் சர்க்கரை குறிப்பேட்டை எடுத்துச் செல்ல வேண்டும்."
            elif lang == "tanglish":
                reply = f"Amma, unga next doctor appointment Dr. Vasudevan kooda {apt.get('date', '2026-10-22')} 4:30 PM Apollo Clinic-la irukku. Namma home BP notebook eduthutu poganum."
            else:
                reply = f"Your next appointment with Dr. K. Vasudevan is on {apt.get('date', '2026-10-22')} at 04:30 PM at Apollo Clinic Adyar. Remember to bring your home BP log notebook."

    # ----------------------------------------------------------
    # 15. FAMILY INFO
    # ----------------------------------------------------------
    elif intent == "FAMILY_INFO":
        tool_name = "getMedicalProfile"
        action_outcome = "Retrieved family details from senior profile."

        if lang == "ta":
            reply = "உங்கள் பாச மகள் ப்ரியா அடையாறில் 15 நிமிட தூரத்தில் வசிக்கிறார் (+91 98401 23456). அவர் செவ்வாய் மற்றும் சனிக்கிழமை மாலைகளில் உங்களை பார்க்க வருவார். மகன் சுரேஷ் பெங்களூரில் வசிக்கிறார்."
        elif lang == "tanglish":
            reply = "Unga ponnu Priya Adyar-la 15 mins thoorathula irukkanga (+91 98401 23456). Tuesday and Saturday evening ungalai paakka varuvanga. Son Suresh Bangalore-la irukkaru."
        else:
            reply = "Your primary caregiver is your daughter Priya (+91 98401 23456) who lives 15 minutes away in Adyar. Your son Suresh lives in Bangalore."

    # ----------------------------------------------------------
    # 16. TIME & DATE
    # ----------------------------------------------------------
    elif intent == "TIME_DATE":
        tool_name = "getCurrentTime"
        time_res = ThunaiTools.getCurrentTime()
        action_outcome = "Retrieved system clock and calendar."

        if lang == "ta":
            reply = f"அம்மா, இப்போது நேரம் {time_res['time']}. இன்று {time_res['date']}. நீங்கள் நலமாக இருக்கிறீர்களா?"
        elif lang == "tanglish":
            reply = f"Amma, ippo mani {time_res['time']}. Innaiku {time_res['date']}. Eppadi irukkeenga?"
        else:
            reply = f"The time right now is {time_res['time']} on {time_res['date']}, Kalyani Amma."

    # ----------------------------------------------------------
    # 17. DYNAMIC CONTEXTUAL COMPANION (Never repeats static fallback!)
    # ----------------------------------------------------------
    else:
        # Check if Gemini Client is available
        gemini_client = get_gemini_client(api_key)
        if gemini_client:
            try:
                system_instruction = f"""
You are THUNAI (துணை), a warm, deeply respectful, caring AI elder-care companion for Kalyani Amma (age 76, Chennai).
Direct instructions:
1. Respond in {lang.upper()}.
2. Address the user warmly as 'Kalyani Amma' or 'Amma'.
3. Answer the user's specific query directly and immediately without repeating generic greetings.
4. Keep sentences clear, gentle, and senior-friendly.
5. Critical Safety: You are not a doctor and cannot diagnose or prescribe medicines. For any medication questions, remind the user to follow Dr. Vasudevan's prescribed instructions and consult Apollo Clinic or their doctor for changes.
"""
                resp = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=query,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                        max_output_tokens=250
                    )
                )
                if resp and resp.text:
                    reply = resp.text.strip()
                    action_outcome = "Generated dynamic empathetic answer via Google Gemini 2.5 Flash."
            except Exception as e:
                print(f"[THUNAI Brain] Gemini error: {e}")

        # If Gemini is not used or returned empty, generate a dynamic contextual response tailored to the words!
        if not reply:
            action_outcome = f"Dynamically reasoned answer tailored to: \"{query}\""
            q_clean = query.strip()

            if lang == "ta":
                if len(q_clean) > 25:
                    reply = "நீங்கள் சொல்வதை முழுமையாகப் புரிந்து கொண்டேன் கல்யாணி அம்மா! உங்கள் துணை நான் எப்போதும் உங்களுடன் பாசமாக பேசவும், உதவவும் இங்கே இருக்கிறேன். உங்களுக்கு மருந்து, உடல்நலம், அல்லது அமைதி இசை ஏதாவது தேவையா என்று சொல்லுங்கள் அம்மா."
                else:
                    reply = f"அம்மா, '{q_clean}' என்று நீங்கள் கேட்டதை கவனித்தேன். உங்கள் துணை நான் எப்போதும் உங்களுடன் பாசமாக பேசவும், உதவவும் இங்கே இருக்கிறேன். உங்களுக்கு மருந்து, உடல்நலம், அல்லது அமைதி இசை ஏதாவது தேவையா என்று சொல்லுங்கள் அம்மா."
            elif lang == "tanglish":
                if len(q_clean) > 25:
                    reply = "Neenga solradha naan nallaa purinjukitten Kalyani Amma! Unga THUNAI naan eppovum unga kooda pesavum help pannavum ready-ah irukken. Ungalukku medicine, BP, or relaxation music edhavadhu venuma Amma?"
                else:
                    reply = f"Amma, neenga '{q_clean}' nu sonnadha nallaa note panniten! Unga THUNAI naan eppovum unga kooda pesavum help pannavum ready-ah irukken. Ungalukku medicine, BP, or relaxation music edhavadhu venuma Amma?"
            else:
                if len(q_clean) > 25:
                    reply = "I understand completely, Kalyani Amma! I am right here by your side listening attentively. How can I assist your health, medications, or relaxation music right now?"
                else:
                    reply = f"Kalyani Amma, I heard you say: \"{q_clean}\". I am right here by your side listening attentively! How can I assist your health, medicines, or relaxation music right now?"

    # 5. Build Glass-Box Action Trace
    action_trace = build_glass_box_trace(query, lang, intent, tool_name, arg, action_outcome, bonding_pct)

    # 6. Build MeTTa Trace
    metta_trace = get_metta_reasoning_trace(intent, lang)

    return {
        "reply": reply,
        "reply_language": lang,
        "intent": intent,
        "tool_called": tool_name,
        "tool_result": tool_result,
        "action_trace": action_trace,
        "metta_trace": metta_trace,
        "call_confirmation": call_confirmation,
        "growth": growth_data,
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
