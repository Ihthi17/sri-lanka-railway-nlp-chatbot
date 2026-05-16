"""
Sri Lanka Railway Chatbot - Fixed Complete Version
Handles user queries with proper database integration and error handling
"""

import re
import json
import difflib
import numpy as np
from datetime import datetime
from database import SessionLocal, DB_CONNECTED, engine
from sqlalchemy import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


# ============================================
# LOAD INTENTS
# ============================================

def load_intents():
    """Load intents from intent.json"""
    try:
        with open("intents.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("intent.json not found. Using basic intents.")
        return {"intents": []}
    except json.JSONDecodeError:
        print("intent.json is malformed. Using basic intents.")
        return {"intents": []}



intents_data = load_intents()

patterns = []
tags = []

for intent in intents_data.get("intents", []):
    for pattern in intent.get("patterns", []):
        patterns.append(pattern.lower())
        tags.append(intent.get("intent", "unknown"))

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(lowercase=True, analyzer='char', ngram_range=(2, 3))
X = vectorizer.fit_transform(patterns) if patterns else None

def contains_word(msg, word):
    return re.search(rf"\b{re.escape(word)}\b", msg) is not None

    
# ============================================
# INTENT DETECTION
# ============================================

def predict_intent(message):
    """
    Improved Intent Detection
    Priority-based keyword matching + TF-IDF fallback
    """

    msg = message.lower().strip()



    # ============================================
    # HIGH PRIORITY INTENTS
    # ============================================

    # GREETING
    greeting_keywords = [
        "hi", "hello", "hey", "good morning", "good afternoon",
        "good evening", "greetings"
    ]
    if any(contains_word(msg, word) for word in greeting_keywords):
     return "greeting"

    # GOODBYE
    goodbye_keywords = [
        "bye", "goodbye", "see you", "exit", "quit", "see you later",
        "farewell", "catch you", "take care", "cheers", "gotta go",
        "bye bye", "later", "have a nice day"
    ]
    if any(word in msg for word in goodbye_keywords):
        return "goodbye"

    # CANCEL / REFUND
    cancel_keywords = [
        "cancel", "cancellation", "refund", "refund information",
        "cancel ticket", "cancel booking", "cancel reservation",
        "cancel train", "refund ticket", "refund booking","refund info"
    ]
    if any(word in msg for word in cancel_keywords):
        return "cancel_ticket"

    # CONTACT DETAILS
    contact_keywords = [
        "contact", "phone", "department", "help line", "hotline",
        "customer care", "railway department", "contact number",
        "contact details", "contact info"
    ]
    if any(word in msg for word in contact_keywords):
        return "railway_contact"

    # LUGGAGE/CHARGES
    luggage_keywords = [
         "baggage", "bag", "luggage charge", "luggage rule",
        "luggage policy", "additional charge", "extra charge"
    ]
    if any(word in msg for word in luggage_keywords):
        return "additional_charges"

    # BOOKING
    booking_keywords = [
        "book", "booking", "reserve", 
        "book train", "buy ticket", "purchase ticket"
    ]
    if any(word in msg for word in booking_keywords):
        return "booking"

    # FARE QUERY
    fare_keywords = [
        "fare", "price", "ticket price", "cost", "charges",
        "ticket cost", "ticket charges", "how much","all ticket prices",
        
    ]
    if any(word in msg for word in fare_keywords):
        return "fare_query"

    # ALL TRAIN SCHEDULE REQUEST (HIGHEST PRIORITY)
    all_schedule_keywords = [
        "all schedule", "all schedules", "full schedule",
        "today all trains", "all train schedule",
        "train list today", "today schedule", "daily schedule",
        "show all trains", "all trains today",
        "give me today all train schedules",
        "give me the today train schedule"
    ]

    if any(word in msg for word in all_schedule_keywords):
        return "all_schedule"

    # SCHEDULE QUERY
    schedule_keywords = [
        "schedule", "timetable", "departure", "arrival", "time",
        "today", "tomorrow", "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]
    if any(word in msg for word in schedule_keywords):
        return "schedule_query"


    # TRAIN SEARCH
    train_keywords = [
        "available trains", "what trains", "train available",
        "all trains", "list trains", "show trains"
    ]
    if any(word in msg for word in train_keywords):
        return "train_search"

    # TERMS & POLICIES
    policy_keywords = [
        "terms", "policy", "rules", "conditions", "refund policy",
        "cancellation policy", "baggage rules", "pet policy",
        "terms and conditions", "terms & conditions","child policy",
        "ticket validity", "payment methods", "Maximum Reservation",
        "nic requirement","ticket usage","what is the child policy","Luggage",
        "luggage information", "what can i carry", "are pets allowed",
        "what can i bring", "can i bring", "dangerous goods","child","child info",
        "Ticket Usage", "ticket usage policy", "ticket usage rules",
        "Governing Law", "governing law", "applicable law", "jurisdiction",
        "how to pay"



    ]
    if any(word in msg for word in policy_keywords):
        return "terms_policy"
    
    

    # STATION INFO
    station_keywords = [
        "station", "distance", "location", "how far",
        "how far is", "how far from colombo", "distance from colombo"
    ]
    if any(word in msg for word in station_keywords):
        return "station_info"
    

  


    # ============================================
    # ROUTE DETECTION
    # ============================================
    if " to " in msg:
        return "route_query"

    # ============================================
    # SINGLE STATION NAME CHECK
    # ============================================
    station = normalize_station(msg)
    if station:
        return "station_name"
    
    

    # ============================================
    # TF-IDF FALLBACK
    # ============================================
    if X is None or len(patterns) == 0:
        return "unknown"

    try:
        v = vectorizer.transform([msg])
        similarities = cosine_similarity(v, X)[0]
        max_idx = np.argmax(similarities)

        if similarities[max_idx] > 0.40:
            return tags[max_idx]
    except Exception as e:
        print(f"Intent prediction error: {e}")

    return "unknown"


# ============================================
# STATION MANAGEMENT
# ============================================

def load_stations():
    """Load all stations from database"""
    if not DB_CONNECTED or SessionLocal is None:
        return {}

    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT station_id, station_name, distance_from_colombo FROM stations")
        ).fetchall()
        return {r[1].lower(): {"name": r[1], "id": r[0], "distance": r[2]} for r in rows}
    except Exception as e:
        print(f"Error loading stations: {e}")
        return {}
    finally:
        db.close()


def get_stations():
    """Dynamically get stations or return cached version"""
    global STATIONS
    if not STATIONS:
        STATIONS = load_stations()
    return STATIONS

STATIONS = load_stations()

def normalize_station(station_name):
    if not station_name:
        return None

    station_lower = station_name.lower().strip()
    stations_data = get_stations()

    # direct match
    for key, value in stations_data.items():
        if station_lower == key:
            return value["name"]

    # partial match (Only for longer words to avoid false positives)
    if len(station_lower) > 3:
        for key, value in stations_data.items():
            if station_lower == key or key == station_lower:
                return value["name"]

    # Colombo special handling
    if "colombo" in station_lower:
        return "Colombo Fort"

    # fuzzy match fallback
    matches = difflib.get_close_matches(station_lower, stations_data.keys(), n=1, cutoff=0.7)
    if matches:
        return stations_data[matches[0]]["name"]

    return None



# ============================================
# DAY DETECTION
# ============================================

def extract_day(message):
    msg = message.lower()

    # Detect direct day names
    days = {
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        "daily": "Daily"
    }

    for key, value in days.items():
        if key in msg:
            return value

    # TODAY
    if "today" in msg:
        return datetime.now().strftime("%A")

    # TOMORROW
    if "tomorrow" in msg:
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.strftime("%A")

    return None



def normalize_station(station_name):
    if not station_name:
        return None

    station_lower = station_name.lower().strip()

    # direct match
    for key, value in STATIONS.items():
        if station_lower == key:
            return value["name"]

    # partial match (IMPORTANT FIX)
    for key, value in STATIONS.items():
        if station_lower in key or key in station_lower:
            return value["name"]

    # Colombo special handling
    if "colombo" in station_lower:
        return "Colombo Fort"

    # fuzzy match fallback
    matches = difflib.get_close_matches(station_lower, STATIONS.keys(), n=1, cutoff=0.5)
    if matches:
        return STATIONS[matches[0]]["name"]

    return None


def extract_single_station(message):
    msg = message.lower()

    # from station
    match = re.search(r"(from|in)\s+([\w\s]+)", msg)

    if match:
        station_raw = match.group(2).strip()
        station = normalize_station(station_raw)

        if station:
            return station

    return None


def extract_route(message):
    msg = message.lower().strip()

    # DO NOT destroy station names
    msg = re.sub(r"[^\w\s]", " ", msg)
    msg = re.sub(r"\s+", " ", msg)

    patterns = [
        r"(?:from\s+)?([\w\s]+?)\s+to\s+([\w\s]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, msg)
        if match:
            source_raw = match.group(1).strip()
            dest_raw = match.group(2).strip()

            source = normalize_station(source_raw)
            destination = normalize_station(dest_raw)

            return source, destination

    return None, None


# ============================================
# SESSION MANAGEMENT
# ============================================

SESSION = {}


def init_session(user_id):
    """Initialize or get user session"""
    if user_id not in SESSION:
        SESSION[user_id] = {
            "from_station": "Colombo Fort",
            "to_station": None,
            "current_intent": None,
            "last_updated": datetime.now()
        }
    return SESSION[user_id]


# ============================================
# DATABASE QUERY FUNCTIONS
# ============================================

def get_fares(from_station, to_station):
    """
    Get ticket fares for given route.
    Returns dict with fare information or None if not found.
    """
    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "🔧 Database connection unavailable. Please contact the Railway Department for fare information."
        }

    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                f.first_class_price,
                f.second_class_price,
                f.third_class_price
            FROM fares f
            JOIN stations s1 ON f.from_station_id = s1.station_id
            JOIN stations s2 ON f.to_station_id = s2.station_id
            WHERE s1.station_name = :from_station 
            AND s2.station_name = :to_station
            LIMIT 1
        """)

        result = db.execute(
            query,
            {"from_station": from_station, "to_station": to_station}
        ).fetchone()

        if result:
            return {
                "status": "success",
                "from": from_station,
                "to": to_station,
                "first_class": float(result[0]) if result[0] else None,
                "second_class": float(result[1]) if result[1] else None,
                "third_class": float(result[2]) if result[2] else None
            }
        else:
            return {
                "status": "not_found",
                "message": f"❌ No fare data found for {from_station} → {to_station}.\n📞 Please contact the Railway Department for current fares."
            }

    except Exception as e:
        print(f"Database error in get_fares: {e}")
        return {
            "status": "error",
            "message": "🔧 Error retrieving fare information. Please contact the Railway Department: +94-11-2325-800"
        }
    finally:
        db.close()


        


def get_train_schedule(from_station, to_station):
    """
    Get available trains between two stations.
    Returns list of trains with timings or error message.
    """
    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "🔧 Database connection unavailable. Please contact the Railway Department for schedule information."
        }

    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                DISTINCT t.train_name,
                ts1.departure_time,
                ts2.arrival_time,
                ts1.running_days
            FROM trains t
            JOIN train_schedules ts1 ON t.train_id = ts1.train_id
            JOIN train_schedules ts2 ON t.train_id = ts2.train_id
            JOIN stations s1 ON ts1.station_id = s1.station_id
            JOIN stations s2 ON ts2.station_id = s2.station_id
            WHERE s1.station_name = :from_station 
            AND s2.station_name = :to_station
            AND ts1.departure_time IS NOT NULL
            AND ts2.arrival_time IS NOT NULL
            ORDER BY ts1.departure_time
        """)

        results = db.execute(
            query,
            {"from_station": from_station, "to_station": to_station}
        ).fetchall()

        if results:
            return {
                "status": "success",
                "from": from_station,
                "to": to_station,
                "trains": [
                    {
                        "name": r[0],
                        "departure": str(r[1]),
                        "arrival": str(r[2]),
                        "days": r[3]
                    }
                    for r in results
                ]
            }
        else:
            return {
                "status": "not_found",
                "message": f"❌ No trains found between {from_station} and {to_station}.\n📞 Please contact the Railway Department for more information. +94-11-2325-800"
            }

    except Exception as e:
        print(f"Database error in get_train_schedule: {e}")
        return {
            "status": "error",
            "message": "🔧 Error retrieving schedule. Please contact the Railway Department: +94-11-2325-800"
        }
    finally:
        db.close()


def get_all_trains():
    """Get all available trains"""
    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "🔧 Database connection unavailable."
        }

    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                t.train_name,
                r.route_name,
                t.train_type,
                COUNT(DISTINCT ts.station_id) as stops
            FROM trains t
            JOIN routes r ON t.route_id = r.route_id
            LEFT JOIN train_schedules ts ON t.train_id = ts.train_id
            GROUP BY t.train_id, t.train_name, r.route_name, t.train_type
            ORDER BY t.train_name
            LIMIT 50
        """)

        results = db.execute(query).fetchall()

        if results:
            return {
                "status": "success",
                "trains": [
                    {
                        "name": r[0],
                        "route": r[1],
                        "type": r[2],
                        "stops": r[3]
                    }
                    for r in results
                ]
            }
        else:
            return {"status": "not_found", "message": "No trains found."}

    except Exception as e:
        print(f"Database error in get_all_trains: {e}")
        return {
            "status": "error",
            "message": "Error retrieving train information."
        }
    finally:
        db.close()


def get_station_info(station_name):
    """Get information about a specific station"""
    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "🔧 Database connection unavailable."
        }

    db = SessionLocal()
    try:
        query = text("""
            SELECT station_name, distance_from_colombo, Telephone_no
            FROM stations
            WHERE station_name = :station_name
            LIMIT 1
        """)

        result = db.execute(
            query,
            {"station_name": station_name}
        ).fetchone()

        if result:
                    return {
            "status": "success",
            "station": result[0],
            "distance": float(result[1]) if result[1] else "N/A",
            "Telephone_no": result[2] if result[2] else "Not Available"
        }
        else:
            return {
                "status": "not_found",
                "message": f"Station '{station_name}' not found in our database."
            }

    except Exception as e:
        print(f"Database error in get_station_info: {e}")
        return {"status": "error", "message": "Error retrieving station information."}
    finally:
        db.close()


def get_terms_conditions(category=None):
    """Get terms and conditions"""
    if not DB_CONNECTED or SessionLocal is None:
        return {"status": "error", "message": "🔧 Database connection unavailable."}

    db = SessionLocal()
    try:
        if category:
            query = text("""
                SELECT section_no, title, description
                FROM terms_conditions
                WHERE category = :category
                ORDER BY section_no
            """)
            results = db.execute(query, {"category": category}).fetchall()
        else:
            query = text("""
                SELECT section_no, title, description
                FROM terms_conditions
                ORDER BY section_no
                LIMIT 10
            """)
            results = db.execute(query).fetchall()

        if results:
            return {
                "status": "success",
                "terms": [{"section": r[0], "title": r[1], "description": r[2]} for r in results]
            }
        return {"status": "not_found", "message": "❌ Terms and conditions not found."}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Error retrieving terms."}
    finally:
        db.close()

def get_policy_by_keyword(search_query):
    """
    Search for a specific policy by its title (e.g., 'Child') 
    or its section number (e.g., '05').
    """
    if not DB_CONNECTED or SessionLocal is None:
        return {"status": "error", "message": "🔧 Database connection unavailable."}

    db = SessionLocal()
    try:
        # Search by exact section number OR partial title match
        query = text("""
            SELECT section_no, title, description, category
            FROM terms_conditions
            WHERE section_no = :query
               OR title LIKE :like_query
            LIMIT 1
        """)
        
        result = db.execute(query, {
            "query": search_query,
            "like_query": f"%{search_query}%"
        }).fetchone()

        if result:
            return {
                "status": "success",
                "data": {
                    "section": result[0],
                    "title": result[1],
                    "description": result[2],
                    "category": result[3]
                }
            }
        return {"status": "not_found"}
    except Exception as e:
        print(f"Database error: {e}")
        return {"status": "error"}
    finally:
        db.close()

       
        


def get_additional_charges():
    """Get additional charges information"""
    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "🔧 Database connection unavailable."
        }

    db = SessionLocal()
    try:
        query = text("""
            SELECT charge_type, description, amount
            FROM additional_charges
            ORDER BY charge_id
        """)
        results = db.execute(query).fetchall()

        if results:
            return {
                "status": "success",
                "charges": [
                    {
                        "type": r[0],
                        "description": r[1],
                        "amount": float(r[2]) if r[2] else None
                    }
                    for r in results
                ]
            }
        else:
            return {
                "status": "not_found",
                "message": "❌ No additional charges information available."
            }

    except Exception as e:
        print(f"Database error in get_additional_charges: {e}")
        return {
            "status": "error",
            "message": "Error retrieving additional charges."
        }
    finally:
        db.close()


# ============================================
# RESPONSE FORMATTING
# ============================================

def format_fare_response(fare_data):
    """Format fare data into readable response"""
    if fare_data["status"] == "error" or fare_data["status"] == "not_found":
        return fare_data["message"]

    response = f"""💰 **Ticket Fares: {fare_data['from']} → {fare_data['to']}**

"""
    if fare_data["first_class"]:
        response += f"🛋️  **First Class (AC Premium):** Rs. {fare_data['first_class']:.2f}\n"
    if fare_data["second_class"]:
        response += f"🪑 **Second Class (Reserved):** Rs. {fare_data['second_class']:.2f}\n"
    if fare_data["third_class"]:
        response += f"👥 **Third Class (Economy):** Rs. {fare_data['third_class']:.2f}\n"

    response += "\n📚 *Luggage charges and taxes may apply separately.*"
    return response


def format_schedule_response(schedule_data):

    """Format schedule data into readable response"""
    if schedule_data["status"] == "error" or schedule_data["status"] == "not_found":
        return schedule_data["message"]

    response = f"""🚆 **Train Schedule: {schedule_data['from']} → {schedule_data['to']}**

"""
    for train in schedule_data["trains"]:
        response += f"""
**{train['name']}**
⏰ Departs: {train['departure']} | Arrives: {train['arrival']}
📅 Days: {train['days']}
"""

    return response.strip()

def format_dynamic_train_response(data, day=None, station=None):

    if data["status"] != "success":
        return data["message"]

    title = "🚆 Train Schedule"

    if day:
        title += f" - {day}"

    if station:
        title += f" - {station}"

    response = f"{title}\n\n"

    for train in data["trains"]:

        response += (
            f"🚉 {train['train_name']}\n"
            f"📍 Station: {train['station']}\n"
            f"⏰ Departure: {train['departure']}\n"
            f"📅 Running: {train['days']}\n\n"
        )

    return response

def format_additional_charges(data):
    """Format additional charges into readable response"""
    if data["status"] != "success":
        return data.get("message", "❌ No additional charge data available.")

    response = "💰 **Additional Charges**\n\n"

    for item in data["charges"]:
        response += f"📌 **{item['type'].replace('_', ' ').title()}**\n"
        response += f"• {item['description']}\n"

        if item["amount"]:
            response += f"• Amount: Rs. {item['amount']:.2f}\n"
        else:
            response += "• Amount: Variable\n"

        response += "\n"

    response += "📞 For more details: +94-11-2325-800"
    return response


def format_terms_response(data):
    """Format terms and conditions into readable response"""
    if data["status"] != "success":
        return data.get("message", "❌ Terms and conditions not available.")

    response = "📋 **Terms & Conditions**\n\n"

    for term in data["terms"]:
        response += f"**{term['section']}. {term['title']}**\n"
        response += f"{term['description']}\n\n"

    response += "📞 For complete terms: +94-11-2325-800"
    return response


def format_station_info(data):
    """Format station information into readable response"""
    if data["status"] != "success":
        return data.get("message", "❌ Station information not available.")

    response = f"""📍 **Station Information**

**Station:** {data['station']}
**Distance from Colombo Fort:** {data['distance']} km
** Phone Number :**{data['Telephone_no']}

📞 For more details: +94-11-2325-800"""
    return response


def format_all_trains(data):
    """Format all trains list into readable response"""
    if data["status"] != "success":
        return data.get("message", "❌ Train information not available.")

    response = "🚆 **Available Trains**\n\n"

    for train in data["trains"]:
        response += f"**{train['name']}** ({train['type']})\n"
        response += f"Route: {train['route']} | Stops: {train['stops']}\n\n"

    return response.strip()

def search_trains(day=None, from_station=None):
    """
    Dynamic train search:
    - today trains
    - saturday trains
    - trains from Colombo
    """

    if not DB_CONNECTED or SessionLocal is None:
        return {
            "status": "error",
            "message": "Database unavailable"
        }

    db = SessionLocal()

    try:

        base_query = """
            SELECT DISTINCT
                t.train_name,
                s.station_name,
                ts.departure_time,
                ts.running_days
            FROM trains t
            JOIN train_schedules ts
                ON t.train_id = ts.train_id
            JOIN stations s
                ON ts.station_id = s.station_id
            WHERE 1=1
        """

        params = {}

        # ============================================
        # FILTER BY DAY
        # ============================================

        if day:

             # Convert full weekday -> DB format
            day_map = {
                    "Monday": "Mon",
                    "Tuesday": "Tue",
                    "Wednesday": "Wed",
                    "Thursday": "Thu",
                    "Friday": "Fri",
                    "Saturday": "Sat",
                    "Sunday": "Sun"
                }


            # Daily trains
            if day.lower() == "daily":

                base_query += """
                    AND ts.running_days LIKE :day
                """

                params["day"] = "%Daily%"

            else:

                db_day = day_map.get(day, day)


                # Include selected day + daily trains
                base_query += """
                    AND (
                        ts.running_days LIKE :day
                        OR ts.running_days LIKE '%Daily%'
                    )
                """

                params["day"] = f"%{db_day}%"

        # ============================================
        # FILTER BY STATION
        # ============================================

        if from_station:

            base_query += """
                AND s.station_name = :station
            """

            params["station"] = from_station

        # ============================================
        # ORDER RESULTS
        # ============================================

        base_query += """
            ORDER BY ts.departure_time
        """

        results = db.execute(
            text(base_query),
            params
        ).fetchall()

        # ============================================
        # RESULTS FOUND
        # ============================================

        if results:

            return {
                "status": "success",
                "trains": [
                    {
                        "train_name": r[0],
                        "station": r[1],
                        "departure": str(r[2]),
                        "days": r[3]
                    }
                    for r in results
                ]
            }

        # ============================================
        # NO RESULTS
        # ============================================

        return {
            "status": "not_found",
            "message": "No trains found"
        }

    except Exception as e:

        print("Train search error:", e)

        return {
            "status": "error",
            "message": "Database query error"
        }

    finally:

        db.close()


# ============================================
# MAIN CHATBOT LOGIC
# ============================================

def get_response(message, user_id="user_001"):
    """
    Generate chatbot response based on user message and intent.
    Implements proper database queries with error handling.
    """
    if not message or not message.strip():
        return "👋 Please type your question. Try: book train, schedule, fare, refund policy, or station info."

    msg = message.lower().strip()
    session = init_session(user_id)

    # Predict intent
    intent = predict_intent(msg)
    session["current_intent"] = intent

    # Extract route if present
    from_station, to_station = extract_route(msg)
    if to_station:
        session["from_station"] = from_station or "Colombo Fort"
        session["to_station"] = to_station

    # ============================================
    # INTENT HANDLERS
    # ============================================

    # GREETING
    if intent == "greeting":
        return """👋 **Welcome to Sri Lanka Railway Chatbot 🚆**

I can help you with:
✅ **Book train tickets** - Say: "Book train to Kandy"
✅ **Check fares** - Say: "Price from Colombo to Galle"
✅ **Train schedules** - Say: "Schedule to Matara"
✅ **Station info** - Say: "Distance to Ella"
✅ **Policies** - Say: "Refund policy" or "Luggage rules"

What can I help you with today?"""

    # GOODBYE
    if intent == "goodbye":
        return "👋 Thank you for using Sri Lanka Railway Chatbot! Have a safe journey 🚆"

    # ALL SCHEDULE
    if intent == "all_schedule":
        day = datetime.now().strftime("%A")
        dynamic_data = search_trains(day=day)
        if dynamic_data["status"] == "success":
            return format_dynamic_train_response(dynamic_data, day=day)
        return "❌ No trains found for today. Please check the official website for full timetable."


    # RAILWAY CONTACT
    if intent == "railway_contact":
        return """📞 **Sri Lanka Railway Department Contact**

🏢 **Headquarters:** Colombo Fort Railway Station
📱 **Hotline:** +94 11 4 600 111
📧 **Email:** info@railway.gov.lk
🌐 **Website:** www.railway.gov.lk

⏰ **Operating Hours:** 24/7 Customer Support

For emergencies, dial 1971."""

    # CANCEL TICKET / REFUND
    if intent == "cancel_ticket":
        terms = get_terms_conditions("General Reservation")
        
        response = """🔄 **Cancellation & Refund Policy**

"""
        
        if terms["status"] == "success":
            for term in terms["terms"]:
                if "cancel" in term["title"].lower() or "refund" in term["title"].lower():
                    response += f"• {term['description']}\n"
        else:
            response += """• 75% refund if cancelled before 7 days
• 50% refund if cancelled before 48 hours
• No refund for cancellations within 48 hours

"""
        
        response += "\n📞 To cancel: Contact +94 11 4 600 111 or visit www.railway.gov.lk"
        return response

    # ADDITIONAL CHARGES (LUGGAGE)
    if intent == "additional_charges":
        charges_data = get_additional_charges()
        return format_additional_charges(charges_data)

    # TERMS & POLICY
   # TERMS & POLICY
    if intent == "terms_policy":
        # Define common policy-related words to strip away
        stop_words = ["policy", "rules", "terms", "conditions", "rule", "what", "is", "the"]
        
        # Extract the potential keyword (e.g., "child" from "child policy")
        keyword = msg
        for word in stop_words:
            keyword = keyword.replace(word, "")
        keyword = keyword.strip()

        # If there is a specific keyword, try to find a single matching policy first
        if keyword:
            specific_policy = get_policy_by_keyword(keyword)
            if specific_policy["status"] == "success":
                p = specific_policy["data"]
                return f"📋 **{p['title']} (Section {p['section']})**\n\n{p['description']}\n\n📂 Category: {p['category']}"

        # Default fallback: Show the general top 10 terms
        terms_data = get_terms_conditions()
        return format_terms_response(terms_data)

    # BOOKING
    if intent == "booking":
        if not session["to_station"]:
            return "🚆 **Train Booking**\n\nPlease tell me your destination station.\n\nExample: 'Book train to Kandy' or 'Colombo to Matara'"

        return f"""✅ **Booking Request Received**

📍 **From:** {session['from_station']}
📍 **To:** {session['to_station']}

Next steps:
1️⃣ Check **fares** - Say: "ticket price"
2️⃣ Check **schedule** - Say: "train schedule"
3️⃣ **Complete booking** at www.railway.gov.lk

📞 Need help? Call: +94 11 4 600 111"""

    # FARE QUERY
    if intent == "fare_query":
        if not session["to_station"]:
            return "💰 **Check Ticket Fares**\n\nPlease provide your destination.\n\nExample: 'What is the fare to Kandy?' or 'Price Colombo to Galle'"

        fare_data = get_fares(session["from_station"], session["to_station"])
        return format_fare_response(fare_data)

    # SCHEDULE QUERY
    # SCHEDULE QUERY
    if intent == "schedule_query":

        # detect day
        day = extract_day(msg)

        # detect station
        station = extract_single_station(msg)

        # detect full route
        from_station, to_station = extract_route(msg)

        # ============================================
        # FULL ROUTE SEARCH
        # Example: Colombo to Kandy
        # ============================================

        if from_station and to_station:

            # save session
            session["from_station"] = from_station
            session["to_station"] = to_station

            schedule_data = get_train_schedule(
                from_station,
                to_station
            )

            if schedule_data["status"] == "success":

                response = (
                    "✅ Yes, trains are available.\n\n"
                    + format_schedule_response(schedule_data)
                )

                response += "\n\n💡 Say 'ticket price' to check fares."

                return response

            return schedule_data["message"]

        # ============================================
        # DAY / STATION SEARCH
        # Example:
        # today trains
        # saturday trains
        # trains from colombo
        # ============================================

        dynamic_data = search_trains(
            day=day,
            from_station=station
        )

        if dynamic_data["status"] == "success":

            return format_dynamic_train_response(
                dynamic_data,
                day=day,
                station=station
            )

        return """❌ No trains found.

Try:
• today trains
• saturday trains
• trains from Colombo
• Colombo to Kandy
"""

    # ROUTE QUERY (Generic from-to)
    if intent == "route_query":
        if not session["to_station"]:
            return "📅 Please tell me full route like Colombo to Matara"

        # Get both schedule and fare
        schedule_data = get_train_schedule(session["from_station"], session["to_station"])
        
        if schedule_data["status"] == "success":
            response = "✅ Yes, trains are available.\n\n" + format_schedule_response(schedule_data)
            response += "\n\n💡 Say 'ticket price' to check fares."
            return response
        else:
            return schedule_data.get("message", "❌ No trains found for this route.")

    # TRAIN SEARCH (All trains)
    if intent == "train_search":
        trains_data = get_all_trains()
        return format_all_trains(trains_data)

    # STATION INFO
    if intent == "station_info":
        # Try to extract station name from message
        station = normalize_station(msg)
        
        if not station:
            return "📍 **Station Information**\n\nPlease specify a station name.\n\nExample: 'Distance to Kandy' or 'Information about Ella'"
        
        station_data = get_station_info(station)
        return format_station_info(station_data)

    # STATION NAME (Single station mentioned)
    if intent == "station_name":
        station = normalize_station(msg)
        if station:
            station_data = get_station_info(station)
            return format_station_info(station_data)

    # UNKNOWN INTENT
    return """❓ I'm not sure I understood that.

I can help you with:
• 🚆 **Train schedules** - "Colombo to Kandy"
• 💰 **Ticket prices** - "Fare to Galle"
• 📋 **Policies** - "Refund policy" or "Luggage rules"
• 📍 **Station info** - "Distance to Ella"
• 📞 **Contact** - "Railway department contact"

What would you like to know?"""


# ============================================
# TESTING / MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("Sri Lanka Railway Chatbot Started")
    print("=" * 50)
    
    if not DB_CONNECTED:
        print("WARNING: Database not connected!")
        print("Some features may not work properly.\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using Sri Lanka Railway Chatbot!")
            break
        
        response = get_response(user_input)
        print(f"\nBot: {response}")