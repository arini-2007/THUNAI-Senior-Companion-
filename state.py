"""
THUNAI — State & Persistent Data Store
Maintains the structured elder profile, caregiver info, medical history,
medication management, measurements, ADLs, appointments, care timeline,
relaxation music library (25 tracks), user-approved memory, and MeTTa knowledge graph.
"""

import os
import json
from datetime import datetime
import sys
import shutil

if getattr(sys, 'frozen', False):
    DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "THUNAI_Data")
    os.makedirs(DATA_DIR, exist_ok=True)
    STATE_FILE = os.path.join(DATA_DIR, "thunai_data.json")
    bundle_state = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "thunai_data.json")
    if not os.path.exists(STATE_FILE) and os.path.exists(bundle_state):
        try:
            shutil.copyfile(bundle_state, STATE_FILE)
        except Exception:
            pass
else:
    STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thunai_data.json")

DEFAULT_STATE = {
    "profile": {
        "full_name": "கல்யாணி ராமநாதன் (Kalyani Ramanathan)",
        "preferred_name": "கல்யாணி அம்மா (Kalyani Amma)",
        "dob": "1948-04-15",
        "age": 76,
        "sex": "Female",
        "blood_group": "B+",
        "preferred_language": "tanglish",  # 'ta', 'en', 'tanglish'
        "communication_preferences": "Short, gentle sentences. Large typography. Speaks in Tamil and Tanglish.",
        "living_arrangement": "Living at home in Adyar, Chennai with spouse; daughter lives 15 mins away.",
        "primary_caregiver": {
            "name": "ப்ரியா (Priya Ramanathan)",
            "relationship": "மகள் (Daughter)",
            "phone": "+91 98401 23456",
            "is_emergency_contact": True
        },
        "secondary_caregiver": {
            "name": "சுரேஷ் (Suresh - Son)",
            "relationship": "மகன் (Son - Bangalore)",
            "phone": "+91 98402 34567",
            "is_emergency_contact": True
        },
        "primary_physician": {
            "name": "டாக்டர் வாசுதேவன் (Dr. K. Vasudevan)",
            "specialty": "Senior Geriatric Physician",
            "hospital": "அப்பல்லோ மருத்துவமனை (Apollo Clinic, Adyar)",
            "phone": "+91 98400 11223"
        },
        "advance_care_info": "Prefers home-based care for minor concerns; consult Dr. Vasudevan for all major changes."
    },
    
    "wellness_check": {
        "last_check_date": "Today, 08:30 AM",
        "physical": {
            "feeling": "Mild knee stiffness, otherwise peaceful",
            "energy": "Moderate (6/10)",
            "sleep_quality": "Slept 6.5 hours peacefully",
            "appetite": "Normal",
            "hydration_glasses": 5,
            "dizziness": "None",
            "shortness_of_breath": "None"
        },
        "emotional": {
            "mood": "Content and calm (நலமாக)",
            "loneliness": "Low - Spoke with daughter Priya yesterday",
            "anxiety": "None reported",
            "feeling_safe": "Yes, completely safe at home"
        },
        "daily_functioning": {
            "eating": "Independent",
            "walking": "Independent with wooden walking stick",
            "bathing": "Needs minor supervision for bathroom grip",
            "taking_meds": "Independent with THUNAI voice reminders"
        }
    },

    "medications": [
        {
            "id": "med-1",
            "name": "Telma 40",
            "generic": "Telmisartan Tablets IP 40mg",
            "dose": "1 tablet",
            "frequency": "Once daily (Morning after breakfast)",
            "route": "Oral with full glass of water",
            "purpose": "Blood Pressure control (ரத்த அழுத்தம்)",
            "prescribed_by": "Dr. K. Vasudevan",
            "status": "Current",
            "time": "08:00 AM",
            "taken_today": True,
            "taken_at": "08:15 AM",
            "notes": "Do not skip. Take with room-temperature water.",
            "allergies_warning": "None"
        },
        {
            "id": "med-2",
            "name": "Metformin 500mg",
            "generic": "Metformin Hydrochloride IP 500mg",
            "dose": "1 tablet",
            "frequency": "Twice daily (After breakfast & dinner)",
            "route": "Oral",
            "purpose": "Blood Sugar control (சர்க்கரை நோய்)",
            "prescribed_by": "Dr. K. Vasudevan",
            "status": "Current",
            "time": "01:30 PM",
            "taken_today": False,
            "taken_at": None,
            "notes": "Always take after meals to avoid stomach upset.",
            "allergies_warning": "None"
        },
        {
            "id": "med-3",
            "name": "Shelcal 500",
            "generic": "Calcium 500mg + Vitamin D3 250 IU",
            "dose": "1 tablet",
            "frequency": "Once daily (After lunch)",
            "route": "Oral",
            "purpose": "Bone density & joint support (எலும்பு வலிமை)",
            "prescribed_by": "Dr. K. Vasudevan",
            "status": "Current",
            "time": "02:00 PM",
            "taken_today": False,
            "taken_at": None,
            "notes": "Take after afternoon meal.",
            "allergies_warning": "None"
        },
        {
            "id": "med-4",
            "name": "Ecosprin 75mg",
            "generic": "Aspirin gastro-resistant 75mg",
            "dose": "1 tablet",
            "frequency": "Once daily (Night after dinner)",
            "route": "Oral",
            "purpose": "Cardiovascular prevention (இதய பாதுகாப்பு)",
            "prescribed_by": "Dr. K. Vasudevan",
            "status": "Current",
            "time": "08:30 PM",
            "taken_today": False,
            "taken_at": None,
            "notes": "Take after dinner. Never double up if forgotten.",
            "allergies_warning": "None"
        }
    ],

    "medical_history": {
        "chief_concern": {
            "reason": "Mild bilateral knee stiffness on waking; blood pressure monitoring",
            "onset": "6 months ago, gradual",
            "severity": "Mild to Moderate (3/10)",
            "relieving_factors": "Warm water compress and 10-minute slow walking"
        },
        "current_symptoms": [
            {
                "symptom": "Morning knee stiffness (முழங்கால் வலி)",
                "location": "Both knees",
                "severity": "Mild (3/10)",
                "pattern": "First 20 mins after waking",
                "source": "Older adult reported",
                "confidence": "Reported"
            },
            {
                "symptom": "Occasional mild post-prandial gas (அசிடிட்டி)",
                "location": "Upper abdomen",
                "severity": "Very Mild",
                "pattern": "After spicy evening snacks",
                "source": "Older adult reported",
                "confidence": "Reported"
            }
        ],
        "past_medical_history": [
            {
                "condition": "Essential Hypertension (ரத்த கொதிப்பு)",
                "diagnosed_year": "2015",
                "status": "Controlled on Telma 40",
                "source": "Clinician documented (Apollo Clinic)",
                "confidence": "Confirmed/documented"
            },
            {
                "condition": "Type 2 Diabetes Mellitus (சர்க்கரை நோய்)",
                "diagnosed_year": "2018",
                "status": "Controlled on Metformin 500mg, HbA1c 6.8%",
                "source": "Clinician documented",
                "confidence": "Confirmed/documented"
            },
            {
                "condition": "Bilateral Knee Osteoarthritis (Grade 2)",
                "diagnosed_year": "2021",
                "status": "Under conservative management & physiotherapy",
                "source": "Clinician documented",
                "confidence": "Confirmed/documented"
            }
        ],
        "surgical_hospitalization": [
            {
                "procedure": "Cataract Surgery (Left Eye with IOL)",
                "date": "2023-02-14",
                "hospital": "Sankara Nethralaya, Chennai",
                "outcome": "Successful, vision clear with reading glasses",
                "source": "Medical document"
            }
        ],
        "allergies": [
            {
                "allergen": "Penicillin (பென்சிலின்)",
                "reaction": "Skin rash and itching",
                "severity": "Moderate",
                "source": "Clinician documented",
                "confidence": "Confirmed/documented"
            },
            {
                "allergen": "Sulfa drugs",
                "reaction": "Unknown / Not tested",
                "source": "Not provided",
                "confidence": "Unknown"
            }
        ],
        "immunizations": [
            {"vaccine": "COVID-19 (Covishield)", "doses": "2 Doses + 1 Booster (2022)", "status": "Completed"},
            {"vaccine": "Influenza (Flu Quadrivalent)", "doses": "Annual dose (October 2025)", "status": "Up to date"},
            {"vaccine": "Pneumococcal Conjugate (PCV13)", "doses": "1 Dose (2023)", "status": "Completed"}
        ],
        "recent_investigations": [
            {"test": "Fasting Blood Sugar", "value": "118", "unit": "mg/dL", "date": "2026-09-15", "source": "Apollo Diagnostics", "confidence": "Confirmed"},
            {"test": "HbA1c", "value": "6.8", "unit": "%", "date": "2026-09-15", "source": "Apollo Diagnostics", "confidence": "Confirmed"},
            {"test": "Serum Creatinine", "value": "0.9", "unit": "mg/dL", "date": "2026-09-15", "source": "Apollo Diagnostics", "confidence": "Confirmed"},
            {"test": "Lipid Profile (LDL)", "value": "98", "unit": "mg/dL", "date": "2026-09-15", "source": "Apollo Diagnostics", "confidence": "Confirmed"}
        ],
        "diagnoses_distinction": {
            "confirmed_documented": ["Essential Hypertension", "Type 2 Diabetes Mellitus", "Bilateral Knee Osteoarthritis", "Penicillin Allergy"],
            "patient_reported": ["Mild morning stiffness", "Mild occasional acidity"],
            "suspected": ["None currently"],
            "conflicting_or_unknown": "None documented. All records align with Apollo Clinic records."
        }
    },

    "measurements": [
        {"id": "m-1", "type": "Blood Pressure", "value": "124/82", "unit": "mmHg", "date": "Today, 08:30 AM", "context": "Morning resting, before tea", "source": "Omron Digital Monitor (Self)", "status": "Normal"},
        {"id": "m-2", "type": "Heart Rate", "value": "72", "unit": "bpm", "date": "Today, 08:30 AM", "context": "Resting pulse", "source": "Digital Monitor", "status": "Normal"},
        {"id": "m-3", "type": "Fasting Blood Glucose", "value": "114", "unit": "mg/dL", "date": "Yesterday, 07:45 AM", "context": "Fasting 10 hrs", "source": "Accu-Chek Instant", "status": "Controlled"},
        {"id": "m-4", "type": "Oxygen Saturation (SpO2)", "value": "98", "unit": "%", "date": "Today, 08:30 AM", "context": "Room air resting", "source": "Pulse Oximeter", "status": "Optimal"},
        {"id": "m-5", "type": "Temperature", "value": "98.4", "unit": "°F", "date": "Today, 08:30 AM", "context": "Morning routine", "source": "Digital Thermometer", "status": "Normal"},
        {"id": "m-6", "type": "Weight", "value": "63.5", "unit": "kg", "date": "2026-09-20", "context": "Morning before breakfast", "source": "Bathroom Scale", "status": "Stable"}
    ],

    "appointments": [
        {
            "id": "apt-1",
            "doctor": "டாக்டர் வாசுதேவன் (Dr. K. Vasudevan)",
            "specialty": "Geriatric Review & Routine Blood Work",
            "date": "2026-10-05",
            "time": "04:30 PM",
            "location": "அப்பல்லோ கிளினிக் (Apollo Clinic, Adyar)",
            "reason": "Quarterly diabetic & BP prescription renewal",
            "preparation": "Bring 1-week home BP & blood sugar log, morning medicine strips",
            "questions_to_ask": [
                "Is knee morning stiffness suitable for light yoga?",
                "Do we need to adjust Metformin dose based on last HbA1c 6.8%?"
            ],
            "confirmed": True
        }
    ],

    "reminders": [
        {
            "id": "rem-1",
            "title": "Dr. K. Vasudevan - Apollo Clinic Checkup",
            "date": "2026-10-25",
            "time": "04:30 PM",
            "description": "Bring 1-week home BP & blood sugar log notebook and morning medicine strips."
        }
    ],

    "mobility_and_falls": {
        "walking_ability": "Walks independently on level surfaces; uses single-point cane outdoors",
        "walking_aids": "Wooden walking stick (கைத்தடி) with anti-skid rubber tip",
        "balance_concerns": "Mild balance hesitation when standing up quickly from deep chairs",
        "fall_history": "No falls in the past 12 months. 1 near-slip in wet bathroom 6 months ago (grab bar installed since).",
        "home_safety_adaptations": [
            "Anti-slip mats installed in bathroom",
            "Sturdy grab bar beside toilet and shower",
            "Night lamps kept on in hallway leading to bathroom",
            "Removed loose throw rugs from living room"
        ]
    },

    "nutrition_and_hydration": {
        "diet_type": "South Indian Vegetarian (இட்லி, தோசை, சாம்பார், காய்கறிகள்)",
        "appetite": "Healthy & regular",
        "fluid_intake_target": "6-7 glasses of warm boiled water / jeera water per day",
        "chewing_swallowing": "Normal, no choking reported",
        "food_restrictions": "Low sodium (உப்பு குறைவு), low refined sugar (சர்க்கரை குறைவு)"
    },

    "sleep_log": {
        "usual_bedtime": "10:00 PM",
        "usual_wake_time": "05:30 AM",
        "average_duration": "7 hours",
        "night_waking": "1-2 times for washroom, falls back asleep easily",
        "daytime_nap": "30-45 minutes around 02:30 PM after lunch"
    },

    "adls_functioning": [
        {"activity": "Bathing & Showering", "status": "Independent (with bathroom grab bar)", "category": "ADL"},
        {"activity": "Dressing & Grooming", "status": "Independent", "category": "ADL"},
        {"activity": "Toileting", "status": "Independent", "category": "ADL"},
        {"activity": "Eating & Drinking", "status": "Independent", "category": "ADL"},
        {"activity": "Walking & Transfers", "status": "Independent with cane", "category": "ADL"},
        {"activity": "Medication Management", "status": "Needs reminders (THUNAI voice alerts)", "category": "IADL"},
        {"activity": "Light Meal Preparation", "status": "Independent (makes morning filter coffee)", "category": "IADL"},
        {"activity": "Phone & Video Calls", "status": "Independent (calls daughter Priya)", "category": "IADL"}
    ],

    "care_timeline": [
        {
            "id": "tl-1",
            "datetime": "2026-09-28 08:15 AM",
            "event": "Medication Event",
            "observation": "Took morning Telma 40 with warm water after idli & sambar.",
            "action": "Marked taken in THUNAI reminder system.",
            "person_reporting": "Kalyani Amma (Older adult)",
            "follow_up": "BP checked at 08:30 AM: 124/82 mmHg (Normal)."
        },
        {
            "id": "tl-2",
            "datetime": "2026-09-27 06:00 PM",
            "event": "Mobility & Social",
            "observation": "Completed 15-minute gentle garden walk with daughter Priya.",
            "action": "Reported pleasant mood, no shortness of breath.",
            "person_reporting": "Priya (Caregiver)",
            "follow_up": "Encouraged daily evening garden stroll."
        },
        {
            "id": "tl-3",
            "datetime": "2026-09-25 10:00 AM",
            "event": "Clinical Investigation",
            "observation": "Quarterly blood tests collected by Apollo home lab phlebotomist.",
            "action": "Fasting glucose: 114 mg/dL, HbA1c: 6.8%, Creatinine: 0.9 mg/dL.",
            "person_reporting": "Apollo Diagnostics Report",
            "follow_up": "Logged to THUNAI Medical History for Dr. Vasudevan review."
        },
        {
            "id": "tl-4",
            "datetime": "2026-09-20 07:30 PM",
            "event": "Wellness Check",
            "observation": "Reported mild gas after eating vada in evening.",
            "action": "THUNAI recommended sipping warm jeera water and walking for 10 mins.",
            "person_reporting": "Kalyani Amma (Voice consultation)",
            "follow_up": "Symptom resolved in 30 minutes, slept peacefully."
        }
    ],

    "daily_care_plan": [
        {"time": "05:45 AM", "activity": "Wake up & Warm Water (காலை விழிப்பு & வெந்நீர்)", "icon": "🌅", "completed": True},
        {"time": "06:30 AM", "activity": "Morning Relaxation Flute & Deep Breathing (காலை அமைதி இசை & மூச்சுப் பயிற்சி)", "icon": "🪈", "completed": True},
        {"time": "07:30 AM", "activity": "Filter Coffee & Light Idli Breakfast (சிற்றுண்டி)", "icon": "☕", "completed": True},
        {"time": "08:15 AM", "activity": "Morning Blood Pressure Medicine: Telma 40 (காலை மாத்திரை)", "icon": "💊", "completed": True},
        {"time": "11:00 AM", "activity": "Hydration: Tender Coconut Water or Buttermilk (மோர் / நீர்)", "icon": "🥥", "completed": False},
        {"time": "01:00 PM", "activity": "Nutritious Lunch (மதிய உணவு - சாம்பார் சாதம் & கீரை)", "icon": "🍲", "completed": False},
        {"time": "01:45 PM", "activity": "Afternoon Medicines: Metformin & Shelcal 500 (மதிய மாத்திரை)", "icon": "💊", "completed": False},
        {"time": "02:30 PM", "activity": "Rest & Gentle Nap (மதிய ஓய்வு)", "icon": "🛌", "completed": False},
        {"time": "05:00 PM", "activity": "Mild Tea & 15-Minute Garden Walk (மாலை நடைப்பயிற்சி)", "icon": "🚶‍♀️", "completed": False},
        {"time": "06:30 PM", "activity": "Evening Calming Music & Relaxation (மாலை அமைதி இசை & ஓய்வு)", "icon": "🎵", "completed": False},
        {"time": "08:00 PM", "activity": "Light Dinner: Idiyappam / Dosa (இரவு உணவு)", "icon": "🍽️", "completed": False},
        {"time": "08:30 PM", "activity": "Night Medicine: Ecosprin 75mg with water (இரவு மாத்திரை)", "icon": "💊", "completed": False},
        {"time": "10:00 PM", "activity": "Delta Wave Sleep Music & Peaceful Sleep (இரவு உறக்கம்)", "icon": "🌙", "completed": False}
    ],

    "relaxation_music_library": {
        "selected_track_id": "rel-1",
        "categories": [
            {"id": "nature", "name_ta": "இயற்கையின் தாலாட்டு", "name_en": "Nature & Earth", "icon": "🌿"},
            {"id": "flute_veena", "name_ta": "புல்லாங்குழல் & வீணை", "name_en": "Meditative Flute & Veena", "icon": "🪈"},
            {"id": "sleep", "name_ta": "ஆழ்ந்த உறக்கம்", "name_en": "Deep Sleep & Rest", "icon": "🌙"},
            {"id": "mindfulness", "name_ta": "மூச்சுப் பயிற்சி & அமைதி", "name_en": "Mindfulness & Breath", "icon": "🧘‍♀️"},
            {"id": "heritage", "name_ta": "பாரம்பரிய மெல்லிசை", "name_en": "Gentle Heritage Strings", "icon": "🌸"}
        ],
        "tracks": [
            # 1. Nature & Earth
            {"id": "rel-1", "category": "nature", "category_name_ta": "இயற்கையின் தாலாட்டு", "category_name_en": "Nature & Earth", "title_ta": "காலை பறவைகள் & தென்றல் காற்று", "title_en": "Morning Birds & Gentle Breeze", "instrument": "Breeze & Birds", "audio_preset": "morning_birds", "duration": "15 Mins", "tempo": "52 BPM", "description_ta": "அமைதியான காலைப் பொழுதில் சோலையில் கேட்கும் பறவைகளின் இனிய ஒலியும் மென் தென்றலும்.", "description_en": "Peaceful early morning birdsong with a gentle garden breeze to uplift spirits."},
            {"id": "rel-2", "category": "nature", "category_name_ta": "இயற்கையின் தாலாட்டு", "category_name_en": "Nature & Earth", "title_ta": "இலைகளில் விழும் தூறல் மழை", "title_en": "Gentle Rain on Green Leaves", "instrument": "Soft Rain & Droplets", "audio_preset": "rain", "duration": "20 Mins", "tempo": "Rain Cadence", "description_ta": "மர இலைகளில் சொட்டும் மெல்லிய தூறல் மழை ஓசை மன அழுத்தத்தை நீக்கும்.", "description_en": "Hypnotic sound of soft rain falling upon green garden leaves to dissolve stress."},
            {"id": "rel-3", "category": "nature", "category_name_ta": "இயற்கையின் தாலாட்டு", "category_name_en": "Nature & Earth", "title_ta": "அமைதியான கடற்கரை அலைகள்", "title_en": "Sunset Ocean Waves", "instrument": "Rolling Ocean Tides", "audio_preset": "ocean_waves", "duration": "25 Mins", "tempo": "Breathing Waves", "description_ta": "மெதுவாக கரையைத் தொட்டுச் செல்லும் மாலை நேர மெல்லிய கடல் அலைகளின் ஓசை.", "description_en": "Gentle rhythmic ocean tides synchronized with relaxed breathing cadence."},
            {"id": "rel-4", "category": "nature", "category_name_ta": "இயற்கையின் தாலாட்டு", "category_name_en": "Nature & Earth", "title_ta": "மூங்கில் காட்டின் மென் காற்று", "title_en": "Bamboo Forest Whisper", "instrument": "Bamboo Wind", "audio_preset": "bamboo_breeze", "duration": "20 Mins", "tempo": "Ambient Flow", "description_ta": "பசுமையான மூங்கில் மரங்களுக்கிடையே தவழ்ந்து வரும் சுகமான இயற்கை காற்று.", "description_en": "Serene wind murmuring through tall bamboo groves for deep physical relaxation."},
            {"id": "rel-5", "category": "nature", "category_name_ta": "இயற்கையின் தாலாட்டு", "category_name_en": "Nature & Earth", "title_ta": "மலை அருவியின் சலசலப்பு", "title_en": "Crystal Mountain Stream", "instrument": "Flowing Water", "audio_preset": "mountain_stream", "duration": "30 Mins", "tempo": "Continuous Serenity", "description_ta": "குளிர்ந்த கற்பாறைகளில் தவழும் தெளிந்த நீரோடையின் சலசலக்கும் சத்தம்.", "description_en": "Calming trickling of fresh mountain spring water over smooth pebbles."},

            # 2. Meditative Flute & Veena
            {"id": "rel-6", "category": "flute_veena", "category_name_ta": "புல்லாங்குழல் & வீணை", "category_name_en": "Meditative Flute & Veena", "title_ta": "பூபாள ராக விடியல் புல்லாங்குழல்", "title_en": "Bhoopalam Dawn Flute", "instrument": "Bamboo Flute & Tanpura", "audio_preset": "dawn_flute", "duration": "18 Mins", "tempo": "54 BPM", "description_ta": "விடியற்காலையில் உள்ளத்திற்கு புதிய உற்சாகமும் அமைதியும் தரும் பூபாள ராக மெல்லிசை.", "description_en": "Awakening morning raga played on traditional bamboo flute with soft tanpura drone."},
            {"id": "rel-7", "category": "flute_veena", "category_name_ta": "புல்லாங்குழல் & வீணை", "category_name_en": "Meditative Flute & Veena", "title_ta": "கல்யாணி ராக மாலை வீணை நாதம்", "title_en": "Kalyani Raga Evening Veena", "instrument": "Saraswati Veena", "audio_preset": "evening_veena", "duration": "22 Mins", "tempo": "Graceful Strings", "description_ta": "அன்னை கல்யாணி அம்மாவுக்காக மீட்கப்படும் சுகமான வீணையின் கம்பீர நாதம்.", "description_en": "Rich acoustic resonance of the classical veena playing comforting Kalyani raga."},
            {"id": "rel-8", "category": "flute_veena", "category_name_ta": "புல்லாங்குழல் & வீணை", "category_name_en": "Meditative Flute & Veena", "title_ta": "மோகன ராக அமைதி இசை", "title_en": "Mohanam Melodic Healing", "instrument": "Warm Bansuri Flute", "audio_preset": "mohanam_flute", "duration": "20 Mins", "tempo": "Harmonic Flow", "description_ta": "உடலின் நரம்புகளை சாந்தப்படுத்தும் உலகப் புகழ்பெற்ற மோகன ராக புல்லாங்குழல்.", "description_en": "Pentatonic Mohanam melodies scientifically known to reduce heart rate and blood pressure."},
            {"id": "rel-9", "category": "flute_veena", "category_name_ta": "புல்லாங்குழல் & வீணை", "category_name_en": "Meditative Flute & Veena", "title_ta": "சரஸ்வதி வீணை சாந்த தாளம்", "title_en": "Saraswati Veena Serenity", "instrument": "Deep Veena Plucks", "audio_preset": "saraswati_veena", "duration": "25 Mins", "tempo": "Peaceful Acoustic", "description_ta": "மனதின் சஞ்சலங்களை போக்கி ஆழ்ந்த அமைதியை உண்டாக்கும் வீணை நரம்புகள்.", "description_en": "Slow plucks and rich harmonics creating an envelope of quiet contentment."},
            {"id": "rel-10", "category": "flute_veena", "category_name_ta": "புல்லாங்குழல் & வீணை", "category_name_en": "Meditative Flute & Veena", "title_ta": "பள்ளத்தாக்கு புல்லாங்குழல் மெல்லிசை", "title_en": "Valley Bamboo Flute Serenade", "instrument": "Echo Flute & Birds", "audio_preset": "valley_flute", "duration": "16 Mins", "tempo": "Serene Wind", "description_ta": "மலைப் பள்ளத்தாக்கில் எதிரொலிக்கும் மெல்லிய புல்லாங்குழலின் இனிய சங்கீதம்.", "description_en": "Reverberant acoustic flute echoes across peaceful misty hills."},

            # 3. Deep Sleep & Rest
            {"id": "rel-11", "category": "sleep", "category_name_ta": "ஆழ்ந்த உறக்கம்", "category_name_en": "Deep Sleep & Rest", "title_ta": "ஆழ்ந்த உறக்க டெல்டா தாலாட்டு", "title_en": "Warm Night Delta Wave Lullaby", "instrument": "Ambient Pads & Delta", "audio_preset": "delta_lullaby", "duration": "45 Mins", "tempo": "Delta Wave", "description_ta": "தூக்கமின்மை உள்ள முதியவர்கள் அமைதியாக உறங்க உதவும் மென்மையான தாலாட்டு அலைகள்.", "description_en": "Delta sleep frequencies designed to gently lull senior minds into restful slumber."},
            {"id": "rel-12", "category": "sleep", "category_name_ta": "ஆழ்ந்த உறக்கம்", "category_name_en": "Deep Sleep & Rest", "title_ta": "அமைதியான நள்ளிரவு பியானோ", "title_en": "Soothing Midnight Piano", "instrument": "Felted Piano", "audio_preset": "midnight_piano", "duration": "30 Mins", "tempo": "48 BPM Adagio", "description_ta": "இரவில் கேட்கும் மிதமான, இதமான மெதுவான பியானோ இசை.", "description_en": "Warm, mellow piano chords echoing softly like a gentle lullaby."},
            {"id": "rel-13", "category": "sleep", "category_name_ta": "ஆழ்ந்த உறக்கம்", "category_name_en": "Deep Sleep & Rest", "title_ta": "மனதை அமைதிப்படுத்தும் மென் இசை", "title_en": "Warm Blanket Acoustic Harmony", "instrument": "Acoustic & Soft Strings", "audio_preset": "warm_strings", "duration": "25 Mins", "tempo": "Comforting", "description_ta": "குளிர்கால கம்பளியைப் போல மனதை பாதுகாப்பாக அரவணைக்கும் மென் நாதம்.", "description_en": "Enveloping harmonic acoustic tones giving a reassuring sense of warmth."},
            {"id": "rel-14", "category": "sleep", "category_name_ta": "ஆழ்ந்த உறக்கம்", "category_name_en": "Deep Sleep & Rest", "title_ta": "விண்மீன் இரவு சாந்த இசை", "title_en": "Starlit Sky Ambient Strings", "instrument": "Celestial Chimes & Cello", "audio_preset": "starlit_ambient", "duration": "35 Mins", "tempo": "Floating Ambient", "description_ta": "அமைதியான நட்சத்திர இரவு வானத்தைப் போன்ற சாந்தமான ஒலியமைப்பு.", "description_en": "Dreamy, weightless ambient textures easing muscular tension."},
            {"id": "rel-15", "category": "sleep", "category_name_ta": "ஆழ்ந்த உறக்கம்", "category_name_en": "Deep Sleep & Rest", "title_ta": "முதியோருக்கான அமைதித் தொட்டில்", "title_en": "Cradle of Peace (ஆழ்ந்த நிம்மதி)", "instrument": "Music Box & Flute Drone", "audio_preset": "cradle_peace", "duration": "40 Mins", "tempo": "Slowing Rhythm", "description_ta": "குழந்தை போல் எந்த கவலையும் இல்லாமல் ஆழ்ந்து தூங்க உதவும் சுகமான தாலாட்டு.", "description_en": "Gentle rocking lullaby notes bringing serene emotional security before sleep."},

            # 4. Mindfulness & Breath
            {"id": "rel-16", "category": "mindfulness", "category_name_ta": "மூச்சுப் பயிற்சி & அமைதி", "category_name_en": "Mindfulness & Breath", "title_ta": "ஆழ்ந்த மூச்சுப் பயிற்சி மணிகள்", "title_en": "Deep Breathing 4-7-8 Chimes", "instrument": "Guided Breathing Chime", "audio_preset": "breathing_478", "duration": "15 Mins", "tempo": "4s Inhale - 7s Hold - 8s Exhale", "description_ta": "மூச்சு உள்ளிழுக்கவும், வைத்திருக்கவும், வெளியிடவும் வழிகாட்டும் அமைதி மணிகள்.", "description_en": "Harmonic chimes pulsing to guide seniors through therapeutic 4-7-8 breathing."},
            {"id": "rel-17", "category": "mindfulness", "category_name_ta": "மூச்சுப் பயிற்சி & அமைதி", "category_name_en": "Mindfulness & Breath", "title_ta": "திபெத்திய சாந்த கிண்ண நாதம்", "title_en": "Singing Bowls of Serenity", "instrument": "Tibetan Singing Bowls", "audio_preset": "singing_bowls", "duration": "20 Mins", "tempo": "432 Hz Resonance", "description_ta": "432 ஹெர்ட்ஸ் அதிர்வெண்ணில் ஒலிக்கும் சாந்த கிண்ணங்களின் மெல்லிய கம்பனம்.", "description_en": "Long-sustaining resonant bowls tuning mental vibrations to pure calm."},
            {"id": "rel-18", "category": "mindfulness", "category_name_ta": "மூச்சுப் பயிற்சி & அமைதி", "category_name_en": "Mindfulness & Breath", "title_ta": "பூந்தோட்ட மணி ஓசையும் நீரோடையும்", "title_en": "Temple Garden Chimes & Water", "instrument": "Wind Chimes & Stream", "audio_preset": "garden_chimes", "duration": "18 Mins", "tempo": "Natural Wind Flow", "description_ta": "பூங்காற்றில் அசையும் அமைதி மணிகளும் மெல்லிய நீர் ஓட்டமும்.", "description_en": "Aromatic garden chimes swaying in a slow afternoon breeze."},
            {"id": "rel-19", "category": "mindfulness", "category_name_ta": "மூச்சுப் பயிற்சி & அமைதி", "category_name_en": "Mindfulness & Breath", "title_ta": "காலை பிராணாயாம தம்புரா நாதம்", "title_en": "Morning Sun Pranayama Drone", "instrument": "Tanpura in C#", "audio_preset": "tanpura_drone", "duration": "25 Mins", "tempo": "Continuous Grounding", "description_ta": "மூச்சுப் பயிற்சி மற்றும் தியானத்தின் போது மனதை ஒருமுகப்படுத்தும் தம்புரா நாதம்.", "description_en": "A pure four-string tanpura drone grounding awareness in the present moment."},
            {"id": "rel-20", "category": "mindfulness", "category_name_ta": "மூச்சுப் பயிற்சி & அமைதி", "category_name_en": "Mindfulness & Breath", "title_ta": "இதய துடிப்பை சீராக்கும் மென் தாளம்", "title_en": "Calming Heartbeat Rhythm", "instrument": "Soft Pulse & Low Strings", "audio_preset": "heartbeat_rhythm", "duration": "20 Mins", "tempo": "60 BPM Calming Pulse", "description_ta": "பதற்றத்தை தணித்து ரத்த அழுத்தத்தை சீராக்க உதவும் மெதுவான 60 BPM தாளம்.", "description_en": "Steady 60 BPM acoustic pulse helping naturally regulate blood pressure and pulse."},

            # 5. Gentle Heritage Strings
            {"id": "rel-21", "category": "heritage", "category_name_ta": "பாரம்பரிய மெல்லிசை", "category_name_en": "Gentle Heritage Strings", "title_ta": "பாட்டியின் அன்பு தாலாட்டு மெட்டு", "title_en": "Grandmother's Sweet Lullaby Melodies", "instrument": "Flute & Warm Harmonics", "audio_preset": "grandmother_lullaby", "duration": "20 Mins", "tempo": "Nostalgic Lullaby", "description_ta": "பழைய நினைவுகளையும் குழந்தை பருவத்து நிம்மதியையும் மீட்டுத் தரும் இனிமையான தாலாட்டு மெட்டு.", "description_en": "Traditional South Indian lullaby motif evoking childhood memories of warmth and safety."},
            {"id": "rel-22", "category": "heritage", "category_name_ta": "பாரம்பரிய மெல்லிசை", "category_name_en": "Gentle Heritage Strings", "title_ta": "கிராமத்து விடியல் தம்புரா & குயில்", "title_en": "Village Dawn Tanpura & Cuckoo", "instrument": "Tanpura & Forest Cuckoo", "audio_preset": "village_tanpura", "duration": "22 Mins", "tempo": "Rural Morning Calm", "description_ta": "கிராமத்து விடியலின் அமைதியும் குயிலின் குரலும் தம்புராவின் சுகமான ஒலியும்.", "description_en": "Nostalgic rural morning ambiance with distant cuckoo calls over rich string drones."},
            {"id": "rel-23", "category": "heritage", "category_name_ta": "பாரம்பரிய மெல்லிசை", "category_name_en": "Gentle Heritage Strings", "title_ta": "சந்தூர் மெல்லிசை அருவி", "title_en": "Santoor Cascades of Kashmir", "instrument": "Santoor Acoustic Strings", "audio_preset": "santoor_cascade", "duration": "18 Mins", "tempo": "Sparkling Drops", "description_ta": "நூறு கம்பிகள் கொண்ட சந்தூர் வாத்தியத்தில் துளிர்க்கும் நீர்வீழ்ச்சி போன்ற மெல்லிசை.", "description_en": "Delicate wooden hammers striking acoustic strings like sparkling water droplets."},
            {"id": "rel-24", "category": "heritage", "category_name_ta": "பாரம்பரிய மெல்லிசை", "category_name_en": "Gentle Heritage Strings", "title_ta": "அந்திப் பொழுது ஹார்மோனியம்", "title_en": "Peaceful Harmonium Twilight", "instrument": "Soft Reed Harmonium", "audio_preset": "harmonium_twilight", "duration": "25 Mins", "tempo": "Sunset Serenade", "description_ta": "மாலையில் மனதிற்கு அமைதியையும் ஆசுவாசத்தையும் தரும் மெதுவான ஹார்மோனியம்.", "description_en": "Gently pumped warm reed organ melodies playing twilight serenity ragas."},
            {"id": "rel-25", "category": "heritage", "category_name_ta": "பாரம்பரிய மெல்லிசை", "category_name_en": "Gentle Heritage Strings", "title_ta": "சாந்தி அமைதி நாதம்", "title_en": "Shanti Universal Peace Resonance", "instrument": "Acoustic Choirs & Bells", "audio_preset": "shanti_om", "duration": "30 Mins", "tempo": "Universal Serenity", "description_ta": "மனதிற்குள் சாந்தியும் உலகில் அமைதியும் நிலவச் செய்யும் அமைதி இசை நாதம்.", "description_en": "Deep, all-embracing ambient harmony filling the living space with peace."}
        ]
    },

    "approved_memories": [
        {"id": "mem-1", "category": "Preference", "content": "Likes to be addressed respectfully as 'கல்யாணி அம்மா' (Kalyani Amma).", "date_added": "2026-09-01", "approved": True},
        {"id": "mem-2", "category": "Routine", "content": "Enjoys warm filter coffee at 7:30 AM before morning medications.", "date_added": "2026-09-05", "approved": True},
        {"id": "mem-3", "category": "Family", "content": "Daughter Priya visits every Tuesday and Saturday evening.", "date_added": "2026-09-10", "approved": True},
        {"id": "mem-4", "category": "Relaxation", "content": "Fond of listening to soothing morning flute and sunset ocean waves for calming the mind.", "date_added": "2026-09-12", "approved": True},
        {"id": "mem-5", "category": "Health", "content": "Has penicillin allergy; Dr. Vasudevan is primary physician at Apollo Adyar.", "date_added": "2026-09-15", "approved": True}
    ],

    "memory_enabled": True,

    # MeTTa / Reasoning Knowledge Graph schema
    "metta_knowledge_base": {
        "facts": [
            "(is-a user elder)",
            "(has-name user \"Kalyani Ramanathan\")",
            "(preferred-title user \"Kalyani Amma\")",
            "(has-age user 76)",
            "(has-language-mode user \"tanglish\")",
            "(primary-caregiver user \"Priya\" \"+919840123456\")",
            "(primary-doctor user \"Dr. Vasudevan\" \"Apollo Adyar\")",
            "(has-condition user \"Hypertension\")",
            "(has-condition user \"Type 2 Diabetes\")",
            "(has-condition user \"Knee Osteoarthritis\")",
            "(has-allergy user \"Penicillin\")",
            "(takes-medication user \"Telma 40\" \"08:00 AM\")",
            "(takes-medication user \"Metformin 500mg\" \"01:30 PM\")",
            "(takes-medication user \"Shelcal 500\" \"02:00 PM\")",
            "(takes-medication user \"Ecosprin 75mg\" \"08:30 PM\")",
            "(last-bp user \"124/82\" \"Normal\")",
            "(mobility-status user \"Independent with cane\")"
        ],
        "rules": [
            "(rule (detected-symptom chest-pain) -> (trigger-action emergency-alert-112))",
            "(rule (detected-symptom breathlessness) -> (trigger-action emergency-alert-112))",
            "(rule (detected-symptom fall-head-injury) -> (trigger-action emergency-alert-108))",
            "(rule (detected-intent call-family) -> (require-confirmation \"Would you like me to call Priya?\"))",
            "(rule (missed-dose ?medication) -> (advise-action \"Take when remembered, never double up\"))",
            "(rule (query-language-is tanglish) -> (respond-in-mode tanglish-gentle))",
            "(rule (query-language-is tamil) -> (respond-in-mode tamil-pure-gentle))"
        ],
        "goals": [
            "(goal safe-elder-care)",
            "(goal dignity-and-compassion)",
            "(goal zero-unauthorized-clinical-diagnosis)",
            "(goal seamless-family-connection)"
        ]
    },

    # Adaptive "Grows Up" Engine (வளர்ச்சி நிலை)
    "growth": {
        "level": 3,
        "stage_title": "மலர் (Blossoming Guardian)",
        "interaction_count": 48,
        "bonding_percentage": 91,
        "last_learned": "Enjoys warm filter coffee at 7:30 AM before morning medications",
        "learned_preferences": [
            "காலை 7:30 மணிக்கு மிதமான காபி குடித்த பிறகு மாத்திரை",
            "மெதுவான, கனிவான குரலில் பேச வேண்டும்",
            "மாலையில் கந்த சஷ்டி கவசம் & பக்திப் பாடல்கள் பிடிக்கும்",
            "மகள் ப்ரியா செவ்வாய் மற்றும் சனிக்கிழமை சந்திப்பார்"
        ]
    }
}


def load_state():
    """Load state from local JSON file or return defaults."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                # Merge saved into default to ensure new schema fields exist
                merged = {**DEFAULT_STATE, **saved}
                return merged
        except Exception as e:
            print(f"[THUNAI State] Error reading state file: {e}. Using defaults.")
    return DEFAULT_STATE.copy()


def save_state(state):
    """Save state to local JSON file safely."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[THUNAI State] Error saving state file: {e}")
        return False


def record_interaction_growth(query="", intent=""):
    """
    Adaptive Growth Engine:
    Levels up THUNAI with every conversation, tracks bonding, and dynamically learns preferences.
    """
    state = load_state()
    growth = state.setdefault("growth", {
        "level": 3,
        "stage_title": "மலர் (Blossoming Guardian)",
        "interaction_count": 48,
        "bonding_percentage": 91,
        "last_learned": "Enjoys warm filter coffee at 7:30 AM before morning medications",
        "learned_preferences": [
            "காலை 7:30 மணிக்கு மிதமான காபி குடித்த பிறகு மாத்திரை",
            "மெதுவான, கனிவான குரலில் பேச வேண்டும்",
            "மாலையில் 25 அமைதி புல்லாங்குழல் & இயற்கை தாலாட்டு இசை பிடிக்கும்",
            "மகள் ப்ரியா செவ்வாய் மற்றும் சனிக்கிழமை சந்திப்பார்"
        ]
    })

    growth["interaction_count"] = growth.get("interaction_count", 48) + 1
    count = growth["interaction_count"]
    growth["bonding_percentage"] = min(99, 82 + (count // 4))

    # Dynamic Growth Stage Evolution
    if count < 15:
        growth["level"] = 1
        growth["stage_title"] = "விதை (Seedling Companion)"
    elif count < 35:
        growth["level"] = 2
        growth["stage_title"] = "தளிர் (Sprout / Attentive Friend)"
    elif count < 65:
        growth["level"] = 3
        growth["stage_title"] = "மலர் (Blossoming Guardian)"
    elif count < 100:
        growth["level"] = 4
        growth["stage_title"] = "கனி (Nurturing Companion)"
    else:
        growth["level"] = 5
        growth["stage_title"] = "நிழல் மரம் (Devoted Lifelong Guardian)"

    # Automatically detect habits or preferences from user statements
    q_lower = query.lower()
    learned_item = None
    if any(k in q_lower for k in ["like", "love", "favorite", "pidikkum", "பிடிக்கும்"]):
        learned_item = f"Personal preference: \"{query}\""
    elif any(k in q_lower for k in ["routine", "always", "every day", "eppovum", "தினமும்"]):
        learned_item = f"Daily routine preference: \"{query}\""
    elif any(k in q_lower for k in ["dislike", "hate", "pidikkadhu", "பிடிக்காது"]):
        learned_item = f"Personal aversion: \"{query}\""

    if learned_item and learned_item not in growth["learned_preferences"]:
        growth["learned_preferences"].insert(0, learned_item)
        growth["last_learned"] = learned_item

    save_state(state)
    return growth
