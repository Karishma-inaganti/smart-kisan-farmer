
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

app.secret_key = "smart-kisan-secret-key"

bookings = {}
token_counter = 100
booked_slot = None
FARMERS_FILE = "farmers.json"


# =========================================================
# FARMER DATA
# =========================================================

def load_farmers():

    if os.path.exists(FARMERS_FILE):

        try:
            with open(FARMERS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except:
            return {}

    return {}


farmers = load_farmers()


def save_farmers():

    with open(FARMERS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            farmers,
            file,
            indent=4,
            ensure_ascii=False
        )

# =========================================================
# TRANSLATIONS
# =========================================================

translations = {

    # =====================================================
    # ENGLISH
    # =====================================================

    "en": {

        "title": "Smart Kisan",
        "welcome": "Welcome to Smart Kisan",

        "farmer": "Farmer",
        "officer": "Officer",

        "login": "Login",
        "register": "Register",
        "back": "Back",
        "home": "Home",
        "logout": "Logout",

        # Farmer Login
        "farmer_login": "Farmer Login",
        "farmer_id": "Farmer ID",
        "farmer_id_placeholder": "Enter Farmer ID",
        "farmer_login_help":
            "Enter SKF followed by the last 4 digits of your registered mobile number.",
        "login_button": "LOGIN",
        "invalid_farmer_id":
            "Invalid Farmer ID. Please enter a valid Farmer ID.",

        # Registration
        "farmer_registration": "Farmer Registration",
        "farmer_name": "Farmer Name",
        "mobile": "Mobile Number",
        "village": "Village",
        "crop_name": "Crop",
        "quantity": "Quantity",
        "quantity_placeholder": "Example: 50 kg",
        "submit": "REGISTER",

        "registration_success": "Registration Successful",
        "your_farmer_id": "Your Farmer ID",

        "invalid_mobile":
            "Please enter a valid 10-digit mobile number.",

        "required_fields":
            "Please fill all the required fields.",

        "already_registered":
            "This mobile number is already registered. Please login using your Farmer ID.",

        # Dashboard
        "farmer_dashboard": "Farmer Dashboard",
        "welcome_farmer": "Welcome, Farmer!",

        "my_details": "My Details",
        "my_token": "My Token",
        "token_number": "Token Number",

        "book_slot": "Book Slot",
        "book_your_slot": "Book Your Procurement Slot",
        "available_slots": "Available Slots",
        "select_date": "Select Date",
        "select_time": "Select Time",
        "book_now": "Book Now",

        "booking_success": "Booking Successful",
        "your_token": "Your Token Number",
        "booking_date": "Booking Date",
        "booking_time": "Booking Time",

        "slot_booked":
            "Your procurement slot has been booked successfully.",

        "no_slot":
            "Please select a date and time.",

        "slot_unavailable":
            "Sorry, this slot is no longer available.",

        # Queue
        "queue_status": "Queue Status",
        "current_position": "Current Position",
        "estimated_time": "Estimated Time",
        "no_token": "No token booked yet.",

        # Procurement
        "procurement_status": "Procurement Status",
        "crop": "Crop",
        "status": "Status",
        "pending": "Pending",
        "completed": "Completed",

        # Centre
        "nearby_centre": "Nearby Procurement Centre",
        "centre_name": "Centre Name",
        "distance": "Distance",

        # Notifications
        "notifications": "Notifications",
        "new_notification": "New Notification",

        # Schedule
        "schedule": "Schedule",
        "scheduled_date": "Scheduled Date",
        "scheduled_time": "Scheduled Time",

        # Officer
        "officer_login": "Officer Login",
        "employee": "Employee Login",
        "username": "Username",
        "password": "Password",
        "invalid": "Invalid username or password",

        "officer_dashboard": "Officer Dashboard",
        "total_farmers": "Total Farmers",
        "pending_procurement": "Pending Procurement",
        "completed_procurement": "Completed Procurement",
        "today_queue": "Today's Queue",

        "officer_notifications": "Officer Notifications",
        "officer_notifications_desc":
            "View notifications related to farmers and procurement.",

        "procurement_update": "Procurement Update",
        "centre_update": "Centre Update",
        "farmer_activity": "Farmer Activity",

        "procurement_waiting":
            "Farmers are waiting for procurement today.",

        "centre_operating":
            "Procurement Centre is operating normally.",

        "farmers_registered":
            "Farmers are registered for today's procurement.",

        "farmer_name_label": "Farmer Name",
        "crop_label": "Crop",
        "quantity_label": "Quantity",
        "centre_label": "Centre"
    },


    # =====================================================
    # HINDI
    # =====================================================

    "hi": {

        "title": "स्मार्ट किसान",
        "welcome": "स्मार्ट किसान में आपका स्वागत है",

        "farmer": "किसान",
        "officer": "अधिकारी",

        "login": "लॉगिन",
        "register": "पंजीकरण",
        "back": "वापस",
        "home": "होम",
        "logout": "लॉगआउट",

        "farmer_login": "किसान लॉगिन",
        "farmer_id": "किसान आईडी",
        "farmer_id_placeholder": "किसान आईडी दर्ज करें",

        "farmer_login_help":
            "अपने पंजीकृत मोबाइल नंबर के अंतिम 4 अंकों के आगे SKF लिखें।",

        "login_button": "लॉगिन",

        "invalid_farmer_id":
            "अमान्य किसान आईडी। कृपया सही किसान आईडी दर्ज करें।",

        "farmer_registration": "किसान पंजीकरण",
        "farmer_name": "किसान का नाम",
        "mobile": "मोबाइल नंबर",
        "village": "गांव",
        "crop_name": "फसल",
        "quantity": "मात्रा",
        "quantity_placeholder": "उदाहरण: 50 किलो",
        "submit": "पंजीकरण करें",

        "registration_success": "पंजीकरण सफल",
        "your_farmer_id": "आपकी किसान आईडी",

        "invalid_mobile":
            "कृपया सही 10 अंकों का मोबाइल नंबर दर्ज करें।",

        "required_fields":
            "कृपया सभी आवश्यक जानकारी भरें।",

        "already_registered":
            "यह मोबाइल नंबर पहले से पंजीकृत है। कृपया अपनी किसान आईडी से लॉगिन करें।",

        "farmer_dashboard": "किसान डैशबोर्ड",
        "welcome_farmer": "स्वागत है, किसान!",

        "my_details": "मेरी जानकारी",
        "my_token": "मेरा टोकन",
        "token_number": "टोकन नंबर",

        "book_slot": "स्लॉट बुक करें",
        "book_your_slot": "अपना खरीद स्लॉट बुक करें",
        "available_slots": "उपलब्ध स्लॉट",
        "select_date": "तारीख चुनें",
        "select_time": "समय चुनें",
        "book_now": "अभी बुक करें",

        "booking_success": "बुकिंग सफल",
        "your_token": "आपका टोकन नंबर",
        "booking_date": "बुकिंग तारीख",
        "booking_time": "बुकिंग समय",

        "slot_booked":
            "आपका खरीद स्लॉट सफलतापूर्वक बुक हो गया है।",

        "no_slot":
            "कृपया तारीख और समय चुनें।",

        "slot_unavailable":
            "यह स्लॉट अब उपलब्ध नहीं है।",

        "queue_status": "कतार स्थिति",
        "current_position": "वर्तमान स्थिति",
        "estimated_time": "अनुमानित समय",
        "no_token": "अभी तक कोई टोकन बुक नहीं हुआ है।",

        "procurement_status": "खरीद स्थिति",
        "crop": "फसल",
        "status": "स्थिति",
        "pending": "लंबित",
        "completed": "पूर्ण",

        "nearby_centre": "नजदीकी खरीद केंद्र",
        "centre_name": "केंद्र का नाम",
        "distance": "दूरी",

        "notifications": "सूचनाएं",
        "new_notification": "नई सूचना",

        "schedule": "समय-सारणी",
        "scheduled_date": "निर्धारित तारीख",
        "scheduled_time": "निर्धारित समय",

        "officer_login": "अधिकारी लॉगिन",
        "employee": "कर्मचारी लॉगिन",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "invalid": "यूज़रनेम या पासवर्ड गलत है",

        "officer_dashboard": "अधिकारी डैशबोर्ड",
        "total_farmers": "कुल किसान",
        "pending_procurement": "लंबित खरीद",
        "completed_procurement": "पूर्ण खरीद",
        "today_queue": "आज की कतार",

        "officer_notifications": "अधिकारी सूचनाएं",
        "officer_notifications_desc":
            "किसानों और खरीद से संबंधित सूचनाएं देखें।",

        "procurement_update": "खरीद अपडेट",
        "centre_update": "केंद्र अपडेट",
        "farmer_activity": "किसान गतिविधि",

        "procurement_waiting":
            "आज किसान खरीद के लिए प्रतीक्षा कर रहे हैं।",

        "centre_operating":
            "खरीद केंद्र सामान्य रूप से कार्य कर रहा है।",

        "farmers_registered":
            "आज की खरीद के लिए किसान पंजीकृत हैं।",

        "farmer_name_label": "किसान का नाम",
        "crop_label": "फसल",
        "quantity_label": "मात्रा",
        "centre_label": "केंद्र"
    },


    # =====================================================
    # TELUGU
    # =====================================================

    "te": {

        "title": "స్మార్ట్ కిసాన్",
        "welcome": "స్మార్ట్ కిసాన్‌కు స్వాగతం",

        "farmer": "రైతు",
        "officer": "అధికారి",

        "login": "లాగిన్",
        "register": "నమోదు",
        "back": "వెనక్కి",
        "home": "హోమ్",
        "logout": "లాగౌట్",

        "farmer_login": "రైతు లాగిన్",
        "farmer_id": "రైతు ID",

        "farmer_id_placeholder":
            "రైతు ID నమోదు చేయండి",

        "farmer_login_help":
            "మీ రిజిస్టర్డ్ మొబైల్ నంబర్ చివరి 4 అంకెల ముందు SKF నమోదు చేయండి.",

        "login_button": "లాగిన్",

        "invalid_farmer_id":
            "చెల్లని రైతు ID. సరైన రైతు ID నమోదు చేయండి.",

        "farmer_registration": "రైతు నమోదు",
        "farmer_name": "రైతు పేరు",
        "mobile": "మొబైల్ నంబర్",
        "village": "గ్రామం",
        "crop_name": "పంట",
        "quantity": "పరిమాణం",

        "quantity_placeholder":
            "ఉదాహరణ: 50 kg",

        "submit": "నమోదు చేయండి",

        "registration_success":
            "నమోదు విజయవంతమైంది",

        "your_farmer_id":
            "మీ రైతు ID",

        "invalid_mobile":
            "దయచేసి సరైన 10 అంకెల మొబైల్ నంబర్ నమోదు చేయండి.",

        "required_fields":
            "దయచేసి అన్ని వివరాలను నమోదు చేయండి.",

        "already_registered":
            "ఈ మొబైల్ నంబర్ ఇప్పటికే నమోదు చేయబడింది. మీ రైతు IDతో లాగిన్ చేయండి.",

        "farmer_dashboard":
            "రైతు డ్యాష్‌బోర్డ్",

        "welcome_farmer":
            "స్వాగతం, రైతు!",

        "my_details":
            "నా వివరాలు",

        "my_token":
            "నా టోకెన్",

        "token_number":
            "టోకెన్ నంబర్",

        "book_slot":
            "స్లాట్ బుక్ చేయండి",

        "book_your_slot":
            "మీ కొనుగోలు స్లాట్‌ను బుక్ చేయండి",

        "available_slots":
            "అందుబాటులో ఉన్న స్లాట్లు",

        "select_date":
            "తేదీని ఎంచుకోండి",

        "select_time":
            "సమయాన్ని ఎంచుకోండి",

        "book_now":
            "ఇప్పుడే బుక్ చేయండి",

        "booking_success":
            "బుకింగ్ విజయవంతమైంది",

        "your_token":
            "మీ టోకెన్ నంబర్",

        "booking_date":
            "బుకింగ్ తేదీ",

        "booking_time":
            "బుకింగ్ సమయం",

        "slot_booked":
            "మీ కొనుగోలు స్లాట్ విజయవంతంగా బుక్ చేయబడింది.",

        "no_slot":
            "దయచేసి తేదీ మరియు సమయాన్ని ఎంచుకోండి.",

        "slot_unavailable":
            "ఈ స్లాట్ ప్రస్తుతం అందుబాటులో లేదు.",

        "queue_status":
            "క్యూ స్థితి",

        "current_position":
            "ప్రస్తుత స్థానం",

        "estimated_time":
            "అంచనా సమయం",

        "no_token":
            "ఇంకా టోకెన్ బుక్ చేయలేదు.",

        "procurement_status":
            "కొనుగోలు స్థితి",

        "crop":
            "పంట",

        "status":
            "స్థితి",

        "pending":
            "పెండింగ్",

        "completed":
            "పూర్తయింది",

        "nearby_centre":
            "సమీప కొనుగోలు కేంద్రం",

        "centre_name":
            "కేంద్రం పేరు",

        "distance":
            "దూరం",

        "notifications":
            "నోటిఫికేషన్లు",

        "new_notification":
            "కొత్త నోటిఫికేషన్",

        "schedule":
            "షెడ్యూల్",

        "scheduled_date":
            "షెడ్యూల్ తేదీ",

        "scheduled_time":
            "షెడ్యూల్ సమయం",

        "officer_login":
            "అధికారి లాగిన్",

        "employee":
            "ఉద్యోగి లాగిన్",

        "username":
            "యూజర్‌నేమ్",

        "password":
            "పాస్‌వర్డ్",

        "invalid":
            "యూజర్‌నేమ్ లేదా పాస్‌వర్డ్ తప్పు",

        "officer_dashboard":
            "అధికారి డ్యాష్‌బోర్డ్",

        "total_farmers":
            "మొత్తం రైతులు",

        "pending_procurement":
            "పెండింగ్ కొనుగోలు",

        "completed_procurement":
            "పూర్తయిన కొనుగోలు",

        "today_queue":
            "ఈరోజు క్యూ",

        "officer_notifications":
            "అధికారి నోటిఫికేషన్లు",

        "officer_notifications_desc":
            "రైతులు మరియు కొనుగోలుకు సంబంధించిన నోటిఫికేషన్లను చూడండి.",

        "procurement_update":
            "కొనుగోలు అప్‌డేట్",

        "centre_update":
            "కేంద్రం అప్‌డేట్",

        "farmer_activity":
            "రైతుల కార్యకలాపాలు",

        "procurement_waiting":
            "ఈరోజు రైతులు కొనుగోలు కోసం వేచి ఉన్నారు.",

        "centre_operating":
            "కొనుగోలు కేంద్రం సాధారణంగా పనిచేస్తోంది.",

        "farmers_registered":
            "ఈరోజు కొనుగోలు కోసం రైతులు నమోదు చేసుకున్నారు.",

        "farmer_name_label":
            "రైతు పేరు",

        "crop_label":
            "పంట",

        "quantity_label":
            "పరిమాణం",

        "centre_label":
            "కేంద్రం"
    }
}


# =========================================================
# HELPER
# =========================================================

def get_language():

    lang = request.args.get("lang", "en")

    if lang not in translations:
        lang = "en"

    return lang


# =========================================================
# 7 DAYS
# =========================================================

def get_dates():

    dates = []

    today = datetime.now().date()

    for i in range(7):

        date = today + timedelta(days=i)

        dates.append({
            "value": date.strftime("%Y-%m-%d"),
            "display": date.strftime("%d-%m-%Y"),
            "day": date.strftime("%A")
        })

    return dates


# =========================================================
# TIME SLOTS
# =========================================================

def get_time_slots():

    return [
        "09:00 AM",
        "09:30 AM",
        "10:00 AM",
        "10:30 AM",
        "11:00 AM",
        "11:30 AM",
        "12:00 PM",
        "02:00 PM",
        "02:30 PM",
        "03:00 PM",
        "03:30 PM",
        "04:00 PM"
    ]


# =========================================================
# NEAREST PROCUREMENT CENTRE
# =========================================================

# You can add your actual villages and centres here.
# This avoids showing a random centre.

village_centres = {

    "dhone": {
        "name": "Dhone Procurement Centre",
        "distance": "2 km"
    },

    "kurnool": {
        "name": "Kurnool Procurement Centre",
        "distance": "3 km"
    },

    "nandyal": {
        "name": "Nandyal Procurement Centre",
        "distance": "4 km"
    },

    "adoni": {
        "name": "Adoni Procurement Centre",
        "distance": "3 km"
    },

    "banaganapalle": {
        "name": "Banaganapalle Procurement Centre",
        "distance": "2.5 km"
    },

    "allagadda": {
        "name": "Allagadda Procurement Centre",
        "distance": "3 km"
    }
}


def get_nearest_centre(village):

    village_key = village.strip().lower()

    if village_key in village_centres:
        return village_centres[village_key]

    # If village is not in our centre database,
    # do NOT randomly show another village.
    return {
        "name": "Centre information unavailable",
        "distance": "Please contact officer"
    }


# =========================================================
# FIND QUEUE POSITION
# =========================================================

def get_queue_details(token):

    if not token or token not in bookings:
        return None

    booking = bookings[token]

    selected_date = booking["date"]
    selected_time = booking["time"]

    same_slot_bookings = []

    for t, data in bookings.items():

        if (
            data["date"] == selected_date
            and data["time"] == selected_time
            and data["status"] == "Booked"
        ):
            same_slot_bookings.append(t)

    # Sort according to booking order
    same_slot_bookings.sort(
        key=lambda x: bookings[x]["booked_at"]
    )

    try:
        position = same_slot_bookings.index(token) + 1
    except ValueError:
        position = 1

    # Assume 20 minutes for each farmer
    estimated_minutes = position * 20

    return {
        "position": position,
        "estimated_time": estimated_minutes
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def language():

    return render_template("language.html")


@app.route("/home")
def home():

    lang = get_language()

    return render_template(
        "index.html",
        lang=lang,
        t=translations[lang]
    )


# =========================================================
# FARMER CHOICE
# =========================================================

@app.route("/farmer-choice")
def farmer_choice():

    lang = get_language()

    return render_template(
        "farmer_choice.html",
        lang=lang,
        t=translations[lang]
    )


# =========================================================
# FARMER REGISTRATION
# =========================================================

# =========================================================
# FARMER REGISTER
# =========================================================

@app.route("/farmer-register", methods=["GET", "POST"])
def farmer_register():

    lang = request.args.get("lang", "en")
    t = translations.get(lang, translations["en"])

    error = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        village = request.form.get("village", "").strip()
        crop = request.form.get("crop", "").strip()
        quantity = request.form.get("quantity", "").strip()
        mobile = request.form.get("mobile", "").strip()

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not name:
            error = "Please enter Farmer Name"

        elif not village:
            error = "Please enter Village"

        elif not crop:
            error = "Please enter Crop"

        elif not quantity:
            error = "Please enter Quantity"

        elif not mobile.isdigit() or len(mobile) != 10:
            error = "Please enter valid 10 digit mobile number"

        if error:

            return render_template(
                "farmer_register.html",
                lang=lang,
                t=t,
                error=error
            )

        # -----------------------------------------
        # CREATE FARMER ID
        # -----------------------------------------

        farmer_id = "SKF" + mobile[-4:]

        # -----------------------------------------
        # SAVE FARMER
        # -----------------------------------------

        farmers[farmer_id] = {

            "name": name,

            "village": village,

            "crop": crop,

            "quantity": quantity,

            "mobile": mobile,

            "status": "Pending"

        }

        # Save permanently
        save_farmers()

        # -----------------------------------------
        # SAVE IN SESSION
        # -----------------------------------------

        session["farmer_id"] = farmer_id

        session["farmer_name"] = name

        # -----------------------------------------
        # SHOW REGISTRATION SUCCESS
        # -----------------------------------------

        return render_template(
            "registration_success.html",

            lang=lang,

            t=t,

            farmer_id=farmer_id,

            farmer_name=name,

            village=village,

            crop=crop,

            quantity=quantity
        )

    return render_template(
        "farmer_register.html",

        lang=lang,

        t=t,

        error=error
    )



# =========================================================
# FARMER LOGIN
# =========================================================
# =========================================================
# FARMER LOGIN
# =========================================================

@app.route("/farmer-login", methods=["GET", "POST"])
def farmer_login():

    lang = request.args.get("lang", "en")

    t = translations.get(lang, translations["en"])

    error = None

    registered_id = request.args.get("registered")

    if request.method == "POST":

        farmer_id = request.form.get(
            "farmer_id",
            ""
        ).strip().upper()

        # -----------------------------------------
        # CHECK FARMER ID
        # -----------------------------------------

        if farmer_id in farmers:

            session["farmer_id"] = farmer_id

            session["farmer_name"] = farmers[farmer_id]["name"]

            return redirect(
                url_for(
                    "farmer",
                    lang=lang
                )
            )

        else:

            error = (
                "Invalid Farmer ID. "
                "Please register first or enter the correct Farmer ID."
            )

    return render_template(
        "farmer_login.html",

        lang=lang,

        t=t,

        error=error,

        registered_id=registered_id
    )
# =========================================================
# FARMER DASHBOARD
# =========================================================
# =========================================================
# FARMER DASHBOARD
# =========================================================

@app.route("/farmer")
def farmer():

    lang = get_language()
    t = translations[lang]

    farmer_id = session.get("farmer_id")

    if not farmer_id or farmer_id not in farmers:
        return redirect(
            url_for(
                "farmer_login",
                lang=lang
            )
        )

    farmer_data = farmers[farmer_id]

    farmer_token = session.get("farmer_token")

    return render_template(
        "farmer.html",
        lang=lang,
        t=t,
        farmer_id=farmer_id,
        farmer=farmer_data,
        farmer_token=farmer_token
    )
# =========================================================
# DATE FUNCTIONS
# =========================================================

def get_dates():

    dates = []

    today = datetime.now()

    for i in range(7):

        date = today + timedelta(days=i)

        dates.append({
            "value": date.strftime("%Y-%m-%d"),
            "display": date.strftime("%d-%m-%Y"),
            "day": date.strftime("%A")
        })

    return dates


# =========================================================
# TIME SLOTS
# =========================================================

def get_time_slots():

    return [
        "09:00 AM - 10:00 AM",
        "10:00 AM - 11:00 AM",
        "11:00 AM - 12:00 PM",
        "12:00 PM - 01:00 PM",
        "02:00 PM - 03:00 PM",
        "03:00 PM - 04:00 PM",
        "04:00 PM - 05:00 PM"
    ]


# =========================================================
# QUEUE
# =========================================================

def get_queue_details(token):

    if not token:

        return None

    if token not in bookings:

        return None

    booking = bookings[token]

    return {
        "position": 1,
        "estimated_time": "10 minutes",
        "status": booking.get("status", "Booked")
    }

# =========================================================
# BOOK SLOT PAGE
# =========================================================

@app.route("/book-slot", methods=["GET", "POST"])
def book_slot():

    lang = get_language()
    t = translations[lang]

    farmer_id = session.get("farmer_id")

    # Farmer login check
    if not farmer_id or farmer_id not in farmers:
        return redirect(
            url_for(
                "farmer_login",
                lang=lang
            )
        )

    farmer_data = farmers[farmer_id]

    # -----------------------------
    # GET - Show booking page
    # -----------------------------
    if request.method == "GET":

        return render_template(
            "book_slot.html",

            lang=lang,
            t=t,

            farmer_id=farmer_id,
            farmer=farmer_data,

            dates=get_dates(),
            time_slots=get_time_slots()
        )

    # -----------------------------
    # POST - Book selected slot
    # -----------------------------

    booked_date = request.form.get("date")
    booked_time = request.form.get("time")

    # Check date
    if not booked_date:
        return render_template(
            "book_slot.html",
            lang=lang,
            t=t,
            farmer_id=farmer_id,
            farmer=farmer_data,
            dates=get_dates(),
            time_slots=get_time_slots(),
            error="Please select a date."
        )

    # Check time
    if not booked_time:
        return render_template(
            "book_slot.html",
            lang=lang,
            t=t,
            farmer_id=farmer_id,
            farmer=farmer_data,
            dates=get_dates(),
            time_slots=get_time_slots(),
            error="Please select a time slot."
        )

    # Save booking
    farmer_data["booking_status"] = "Booked"
    farmer_data["booked_date"] = booked_date
    farmer_data["booked_time"] = booked_time

    # Save farmer data
    farmers[farmer_id] = farmer_data

    # -----------------------------
    # SUCCESS PAGE
    # -----------------------------

    return render_template(
        "booking_success.html",

        lang=lang,
        t=t,

        farmer=farmer_data,
        farmer_id=farmer_id,

        booked_date=booked_date,
        booked_time=booked_time
    )

    # =====================================================
    # CHECK SLOT AVAILABILITY
    # Maximum 5 farmers per time slot
    # =====================================================

    slot_count = 0

    for data in bookings.values():

        if (
            data["date"] == selected_date
            and data["time"] == selected_time
            and data["status"] == "Booked"
        ):
            slot_count += 1

    if slot_count >= 5:

        return render_template(
            "book_slot.html",

            lang=lang,
            t=translations[lang],

            dates=get_dates(),
            time_slots=get_time_slots(),

            error=translations[lang]["slot_unavailable"]
        )

    # =====================================================
    # PREVENT SAME FARMER BOOKING MULTIPLE TIMES
    # =====================================================
    for token, data in bookings.items():

        if (
            data.get("farmer_id") == farmer_id
            and data["status"] == "Booked"
        ):

            session["farmer_token"] = token

            return redirect(
                url_for(
                    "farmer",
                    lang=lang
                )
            )

    # =====================================================
    # GENERATE TOKEN
    # =====================================================

    token_counter += 1

    token = "A-" + str(token_counter)

    # =====================================================
    # STORE BOOKING
    # =====================================================

    bookings[token] = {

        "farmer_id": farmer_id,

        "date": selected_date,

        "time": selected_time,

        "status": "Booked",

        "booked_at": datetime.now()
    }

    # Save token
    session["farmer_token"] = token

    # =====================================================
    # SUCCESS
    # =====================================================

    return redirect(
        url_for(
            "booking_success",
            lang=lang,
            token=token,
            date=selected_date,
            time=selected_time
        )
    )


# =========================================================
# BOOKING SUCCESS
# =========================================================

@app.route("/booking-success")
def booking_success():

    lang = get_language()

    token = request.args.get("token")

    date = request.args.get("date")

    time = request.args.get("time")

    queue = get_queue_details(token)

    return render_template(

        "booking_success.html",

        lang=lang,

        t=translations[lang],

        token=token,

        date=date,

        time=time,

        queue=queue
    )

# =========================================================
# FARMER PROCUREMENT STATUS
# =========================================================
@app.route("/procurement-status")
def procurement_status():

    return render_template(
        "procurement_status.html",
        booked_slot=booked_slot,
        status="Slot Booked" if booked_slot else "Not Booked",
        message="Your procurement slot has been successfully booked."
        if booked_slot
        else "Please book a procurement slot first."
    )
# =========================================================
# MY TOKEN
# =========================================================

@app.route("/my-token")
def my_token():

    lang = get_language()

    token = session.get("farmer_token")

    queue = get_queue_details(token)

    return render_template(

        "my_token.html",

        lang=lang,

        t=translations[lang],

        token=token,

        queue=queue
    )


# =========================================================
# NEARBY CENTRE
# =========================================================
# =========================================================
# NEARBY PROCUREMENT CENTRE
# =========================================================

CENTRES = {
    "Kurnool": {
        "name": "Kurnool Procurement Centre",
        "location": "Kurnool, Andhra Pradesh",
        "distance": "3.5 km",
        "timing": "9:00 AM - 5:00 PM",
        "phone": "9876543210"
    },

    "Adoni": {
        "name": "Adoni Procurement Centre",
        "location": "Adoni, Andhra Pradesh",
        "distance": "4.2 km",
        "timing": "9:00 AM - 5:00 PM",
        "phone": "9876543211"
    },

    "Nandyal": {
        "name": "Nandyal Procurement Centre",
        "location": "Nandyal, Andhra Pradesh",
        "distance": "5.1 km",
        "timing": "9:00 AM - 5:00 PM",
        "phone": "9876543212"
    },

    "Dhone": {
        "name": "Dhone Procurement Centre",
        "location": "Dhone, Andhra Pradesh",
        "distance": "4.8 km",
        "timing": "9:00 AM - 5:00 PM",
        "phone": "9876543213"
    },

    "Yemmiganur": {
        "name": "Yemmiganur Procurement Centre",
        "location": "Yemmiganur, Andhra Pradesh",
        "distance": "3.9 km",
        "timing": "9:00 AM - 5:00 PM",
        "phone": "9876543214"
    }
}


@app.route("/nearby-centre")
def nearby_centre():

    lang = request.args.get("lang", "en")

    if lang not in translations:
        lang = "en"

    # Get logged-in farmer
    farmer_id = session.get("farmer_id")

    farmer = farmers.get(farmer_id)

    if not farmer:

        return render_template(
            "nearby_centre.html",
            centre=None,
            lang=lang,
            t=translations[lang]
        )

    village = farmer.get("village", "").strip()

    # Match village with nearest centre
    village_lower = village.lower()

    if village_lower in ["kurnool", "orvakal", "nandyal road"]:
        centre = CENTRES["Kurnool"]

    elif village_lower in ["adoni", "mantralayam", "kosigi"]:
        centre = CENTRES["Adoni"]

    elif village_lower in ["nandyal", "banaganapalle", "atmakur"]:
        centre = CENTRES["Nandyal"]

    elif village_lower in ["dhone", "pattikonda", "peapully"]:
        centre = CENTRES["Dhone"]

    elif village_lower in ["yemmiganur", "kodumuru", "guntakal"]:
        centre = CENTRES["Yemmiganur"]

    else:
        # If village is not in our demo mapping,
        # don't randomly show a centre.
        centre = None

    return render_template(
        "nearby_centre.html",
        centre=centre,
        village=village,
        lang=lang,
        t=translations[lang]
    )


# =========================================================
# QUEUE STATUS
# =========================================================

@app.route("/queue-status")
def queue_status():

    lang = get_language()

    token = session.get("farmer_token")

    queue = get_queue_details(token)

    return render_template(

        "queue_status.html",

        lang=lang,

        t=translations[lang],

        token=token,

        queue=queue
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@app.route("/notifications")
def notifications():

    lang = get_language()

    return render_template(

        "notifications.html",

        lang=lang,

        t=translations[lang]
    )


# =========================================================
# SCHEDULE
# =========================================================
@app.route("/schedule")
def schedule():

    lang = request.args.get("lang", "en")

    if lang not in translations:
        lang = "en"

    t = translations[lang]

    slots = []

    today = datetime.now().date()

    # Next 7 days
    for i in range(7):

        current_date = today + timedelta(days=i)

        date_display = current_date.strftime("%d %B %Y")
        date_value = current_date.strftime("%Y-%m-%d")

        # Morning slot
        slots.append({
            "date": date_display,
            "date_value": date_value,
            "time": "9:00 AM - 11:00 AM",
            "available": 12
        })

        # Afternoon slot
        slots.append({
            "date": date_display,
            "date_value": date_value,
            "time": "11:00 AM - 1:00 PM",
            "available": 8
        })

        # Evening slot
        slots.append({
            "date": date_display,
            "date_value": date_value,
            "time": "2:00 PM - 4:00 PM",
            "available": 6
        })

    return render_template(
        "schedule.html",
        slots=slots,
        lang=lang,
        t=t
    )

# =========================================================
# OFFICER LOGIN
# =========================================================

@app.route("/officer-login", methods=["GET"])
def officer_login():
    lang = request.args.get("lang", "en")

    t = {
        "title": "Employee Login - Smart Kisan",
        "login": "Employee Login",
        "username": "Username",
        "password": "Password",
        "login_button": "LOGIN",
        "back": "Back to Home",
        "invalid": "Invalid username or password"
    }

    return render_template(
        "officer_login.html",
        lang=lang,
        t=t
    )
@app.route("/officer-login", methods=["POST"])
def officer_login_post():

    username = request.form.get("username")
    password = request.form.get("password")
    lang = request.args.get("lang", "en")

    if username == "officer" and password == "1234":
        return redirect("/officer?lang=" + lang)

    t = {
        "title": "Employee Login - Smart Kisan",
        "login": "Employee Login",
        "username": "Username",
        "password": "Password",
        "login_button": "LOGIN",
        "back": "Back to Home",
        "invalid": "Invalid username or password"
    }

    return render_template(
        "officer_login.html",
        lang=lang,
        t=t,
        error=t["invalid"]
    )
# =========================================================
# OFFICER DASHBOARD
# =========================================================
@app.route("/officer")
def officer():

    lang = request.args.get("lang", "en")

    try:
        with open("farmers.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Handle different farmers.json structures
    if isinstance(data, list):
        farmers = data

    elif isinstance(data, dict):
        # If JSON is {"farmers": [...]}
        if isinstance(data.get("farmers"), list):
            farmers = data["farmers"]

        # If JSON contains farmer records as values
        else:
            farmers = [
                value for value in data.values()
                if isinstance(value, dict)
            ]

    else:
        farmers = []

    total_farmers = len(farmers)

    pending_procurement = 0
    completed_procurement = 0

    for farmer in farmers:

        if not isinstance(farmer, dict):
            continue

        status = str(farmer.get("status", "")).lower()

        if status == "pending":
            pending_procurement += 1

        elif status == "completed":
            completed_procurement += 1

    return render_template(
        "officer.html",
        lang=lang,
        t=translations.get(lang, translations["en"]),
        total_farmers=total_farmers,
        pending_procurement=pending_procurement,
        completed_procurement=completed_procurement
    )
# =========================================================
# OFFICER PROCUREMENT STATUS
# =========================================================

@app.route("/officer-procurement-status")
def officer_procurement_status():

    lang = get_language()

    farmer_list = []

    for farmer_id, farmer_data in farmers.items():

        farmer_list.append({

            "farmer_id": farmer_id,

            "name": farmer_data["name"],

            "crop": farmer_data["crop"],

            "quantity": farmer_data["quantity"],

            "village": farmer_data["village"],

            "centre": farmer_data.get("centre", {}).get("name", "Not Assigned"),

            "status": "Pending"
        })

    return render_template(

        "officer_procurement_status.html",

        lang=lang,

        t=translations[lang],

        farmers=farmer_list
    )


# =========================================================
# OFFICER NOTIFICATIONS
# =========================================================

@app.route("/officer-notifications")
def officer_notifications():

    lang = get_language()

    # Dynamic notifications

    notifications_list = []

    if len(farmers) > 0:

        notifications_list.append(
            translations[lang]["farmers_registered"]
        )

    pending_count = sum(
        1
        for b in bookings.values()
        if b["status"] == "Booked"
    )

    if pending_count > 0:

        notifications_list.append(
            f"{pending_count} "
            + translations[lang]["procurement_waiting"]
        )

    notifications_list.append(
        translations[lang]["centre_operating"]
    )

    return render_template(

        "officer_notifications.html",

        lang=lang,

        t=translations[lang],

        notifications=notifications_list
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("language")
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )