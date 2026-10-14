import json
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ============================================================
# FLASK APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.secret_key = "fitbuddy_secret_key_2026"

DATABASE = "fitbuddy.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_db()


    # ========================================================
    # USERS TABLE
    # ========================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'user',

            created_at TEXT NOT NULL

        )
    """)


    # ========================================================
    # FITNESS PROFILES TABLE
    # ========================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS fitness_profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            age INTEGER NOT NULL,

            gender TEXT NOT NULL,

            height REAL NOT NULL,

            weight REAL NOT NULL,

            goal TEXT NOT NULL,

            level TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id)

        )
    """)


    # ========================================================
    # PLANS TABLE
    # ========================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS plans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            profile_id INTEGER NOT NULL,

            workout_plan TEXT NOT NULL,

            nutrition_tips TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id),

            FOREIGN KEY (profile_id)
            REFERENCES fitness_profiles(id)

        )
    """)


    # ========================================================
    # CREATE DEFAULT ADMIN ACCOUNT
    # ========================================================

    admin_email = "admin@fitbuddy.com"

    admin_password = "admin123"


    existing_admin = conn.execute(
        """
        SELECT id

        FROM users

        WHERE email = ?

        AND role = 'admin'
        """,

        (admin_email,)
    ).fetchone()


    if not existing_admin:

        hashed_admin_password = generate_password_hash(
            admin_password
        )


        conn.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password,
                role,
                created_at
            )

            VALUES (?, ?, ?, ?, ?)
            """,

            (
                "FitBuddy Admin",

                admin_email,

                hashed_admin_password,

                "admin",

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )


    # ========================================================
    # SAVE DATABASE
    # ========================================================

    conn.commit()

    conn.close()


# ============================================================
# WORKOUT DATA
# ============================================================

WORKOUT_DATA = {


    # ========================================================
    # WEIGHT LOSS
    # ========================================================

    "weight_loss": {

        "title": "Weight Loss",

        "days": [

            {
                "day": "Monday",

                "focus": "Full Body + Cardio",

                "icon": "🏃",

                "exercises": [

                    ("Bodyweight Squats", "3 × 12"),

                    ("Jumping Jacks", "3 × 20"),

                    ("Push-ups", "3 × 10"),

                    ("Mountain Climbers", "3 × 20"),

                    ("Plank", "3 × 30 sec")
                ]
            },


            {
                "day": "Tuesday",

                "focus": "Cardio",

                "icon": "❤️",

                "exercises": [

                    ("Brisk Walking", "30 min"),

                    ("High Knees", "3 × 20"),

                    ("Step-ups", "3 × 12"),

                    ("Jumping Jacks", "3 × 20")
                ]
            },


            {
                "day": "Wednesday",

                "focus": "Lower Body",

                "icon": "🦵",

                "exercises": [

                    ("Squats", "3 × 12"),

                    ("Reverse Lunges", "3 × 10"),

                    ("Glute Bridges", "3 × 15"),

                    ("Calf Raises", "3 × 15"),

                    ("Wall Sit", "3 × 30 sec")
                ]
            },


            {
                "day": "Thursday",

                "focus": "Active Recovery",

                "icon": "🧘",

                "exercises": [

                    ("Easy Walking", "20–30 min"),

                    ("Full Body Stretch", "10 min"),

                    ("Light Yoga", "15 min"),

                    ("Deep Breathing", "5 min")
                ]
            },


            {
                "day": "Friday",

                "focus": "Full Body",

                "icon": "⚡",

                "exercises": [

                    ("Squats", "3 × 15"),

                    ("Push-ups", "3 × 10"),

                    ("Mountain Climbers", "3 × 20"),

                    ("Lunges", "3 × 10"),

                    ("Plank", "3 × 40 sec")
                ]
            },


            {
                "day": "Saturday",

                "focus": "Cardio + Core",

                "icon": "🔥",

                "exercises": [

                    ("Brisk Walking", "30 min"),

                    ("Bicycle Crunches", "3 × 15"),

                    ("Leg Raises", "3 × 10"),

                    ("Plank", "3 × 30 sec")
                ]
            },


            {
                "day": "Sunday",

                "focus": "Rest & Recovery",

                "icon": "🌿",

                "exercises": [

                    ("Relaxed Walking", "15–20 min"),

                    ("Gentle Stretching", "10 min"),

                    ("Deep Breathing", "5 min")
                ]
            }

        ]
    },


    # ========================================================
    # MUSCLE GAIN
    # ========================================================

    "muscle_gain": {

        "title": "Muscle Gain",

        "days": [

            {
                "day": "Monday",

                "focus": "Chest + Triceps",

                "icon": "💪",

                "exercises": [

                    ("Push-ups", "3 × 10"),

                    ("Incline Push-ups", "3 × 10"),

                    ("Diamond Push-ups", "3 × 8"),

                    ("Triceps Dips", "3 × 10"),

                    ("Plank", "3 × 30 sec")
                ]
            },


            {
                "day": "Tuesday",

                "focus": "Back + Biceps",

                "icon": "🏋️",

                "exercises": [

                    ("Superman", "3 × 12"),

                    ("Reverse Snow Angels", "3 × 10"),

                    ("Back Extensions", "3 × 12"),

                    ("Biceps Curl", "3 × 12")
                ]
            },


            {
                "day": "Wednesday",

                "focus": "Legs",

                "icon": "🦵",

                "exercises": [

                    ("Squats", "4 × 12"),

                    ("Lunges", "3 × 10"),

                    ("Glute Bridges", "3 × 15"),

                    ("Calf Raises", "4 × 15"),

                    ("Wall Sit", "3 × 40 sec")
                ]
            },


            {
                "day": "Thursday",

                "focus": "Recovery",

                "icon": "🧘",

                "exercises": [

                    ("Easy Walking", "20 min"),

                    ("Leg Stretch", "10 min"),

                    ("Shoulder Stretch", "10 min"),

                    ("Deep Breathing", "5 min")
                ]
            },


            {
                "day": "Friday",

                "focus": "Upper Body",

                "icon": "🔥",

                "exercises": [

                    ("Push-ups", "4 × 10"),

                    ("Pike Push-ups", "3 × 8"),

                    ("Triceps Dips", "3 × 10"),

                    ("Superman", "3 × 12")
                ]
            },


            {
                "day": "Saturday",

                "focus": "Lower Body + Core",

                "icon": "⚡",

                "exercises": [

                    ("Squats", "4 × 12"),

                    ("Reverse Lunges", "3 × 10"),

                    ("Glute Bridges", "3 × 15"),

                    ("Plank", "3 × 40 sec"),

                    ("Leg Raises", "3 × 10")
                ]
            },


            {
                "day": "Sunday",

                "focus": "Complete Recovery",

                "icon": "🌿",

                "exercises": [

                    ("Relaxed Walking", "15–20 min"),

                    ("Full Body Stretch", "15 min"),

                    ("Breathing Exercise", "5 min")
                ]
            }

        ]
    },


    # ========================================================
    # GENERAL FITNESS
    # ========================================================

    "general_fitness": {

        "title": "General Fitness",

        "days": [

            {
                "day": "Monday",

                "focus": "Full Body",

                "icon": "🏋️",

                "exercises": [

                    ("Squats", "3 × 12"),

                    ("Push-ups", "3 × 10"),

                    ("Lunges", "3 × 10"),

                    ("Plank", "3 × 30 sec")
                ]
            },


            {
                "day": "Tuesday",

                "focus": "Cardio",

                "icon": "❤️",

                "exercises": [

                    ("Brisk Walking", "30 min"),

                    ("Jumping Jacks", "3 × 20"),

                    ("High Knees", "3 × 20")
                ]
            },


            {
                "day": "Wednesday",

                "focus": "Core",

                "icon": "🔥",

                "exercises": [

                    ("Plank", "3 × 30 sec"),

                    ("Bicycle Crunches", "3 × 15"),

                    ("Leg Raises", "3 × 10"),

                    ("Bird Dog", "3 × 10")
                ]
            },


            {
                "day": "Thursday",

                "focus": "Flexibility",

                "icon": "🧘",

                "exercises": [

                    ("Full Body Stretch", "15 min"),

                    ("Cat-Cow Stretch", "3 × 10"),

                    ("Child's Pose", "3 × 30 sec"),

                    ("Deep Breathing", "5 min")
                ]
            },


            {
                "day": "Friday",

                "focus": "Full Body",

                "icon": "⚡",

                "exercises": [

                    ("Squats", "3 × 15"),

                    ("Push-ups", "3 × 10"),

                    ("Glute Bridges", "3 × 15"),

                    ("Mountain Climbers", "3 × 15")
                ]
            },


            {
                "day": "Saturday",

                "focus": "Cardio + Core",

                "icon": "🏃",

                "exercises": [

                    ("Walking", "30 min"),

                    ("Plank", "3 × 30 sec"),

                    ("Bicycle Crunches", "3 × 15"),

                    ("Jumping Jacks", "3 × 20")
                ]
            },


            {
                "day": "Sunday",

                "focus": "Rest & Recovery",

                "icon": "🌿",

                "exercises": [

                    ("Easy Walking", "15–20 min"),

                    ("Gentle Stretching", "10 min"),

                    ("Deep Breathing", "5 min")
                ]
            }

        ]
    },


    # ========================================================
    # FLEXIBILITY
    # ========================================================

    "flexibility": {

        "title": "Flexibility",

        "days": [

            {
                "day": "Monday",

                "focus": "Full Body Mobility",

                "icon": "🧘",

                "exercises": [

                    ("Neck Stretch", "3 × 20 sec"),

                    ("Shoulder Rolls", "3 × 10"),

                    ("Cat-Cow", "3 × 10"),

                    ("Child's Pose", "3 × 30 sec")
                ]
            },


            {
                "day": "Tuesday",

                "focus": "Lower Body Flexibility",

                "icon": "🦵",

                "exercises": [

                    ("Hamstring Stretch", "3 × 30 sec"),

                    ("Quad Stretch", "3 × 30 sec"),

                    ("Hip Flexor Stretch", "3 × 30 sec"),

                    ("Calf Stretch", "3 × 30 sec")
                ]
            },


            {
                "day": "Wednesday",

                "focus": "Yoga & Mobility",

                "icon": "🌿",

                "exercises": [

                    ("Cat-Cow", "3 × 10"),

                    ("Child's Pose", "3 × 30 sec"),

                    ("Cobra Stretch", "3 × 20 sec"),

                    ("Seated Twist", "3 × 20 sec")
                ]
            },


            {
                "day": "Thursday",

                "focus": "Upper Body Mobility",

                "icon": "💪",

                "exercises": [

                    ("Shoulder Stretch", "3 × 30 sec"),

                    ("Arm Circles", "3 × 15"),

                    ("Chest Stretch", "3 × 30 sec"),

                    ("Neck Stretch", "3 × 20 sec")
                ]
            },


            {
                "day": "Friday",

                "focus": "Full Body Stretch",

                "icon": "✨",

                "exercises": [

                    ("Standing Forward Fold", "3 × 30 sec"),

                    ("Quad Stretch", "3 × 30 sec"),

                    ("Shoulder Stretch", "3 × 30 sec"),

                    ("Child's Pose", "3 × 30 sec")
                ]
            },


            {
                "day": "Saturday",

                "focus": "Yoga Flow",

                "icon": "🧘",

                "exercises": [

                    ("Sun Salutation", "5 rounds"),

                    ("Cat-Cow", "3 × 10"),

                    ("Cobra", "3 × 20 sec"),

                    ("Child's Pose", "3 × 30 sec")
                ]
            },


            {
                "day": "Sunday",

                "focus": "Relaxation",

                "icon": "🌿",

                "exercises": [

                    ("Gentle Stretching", "15 min"),

                    ("Deep Breathing", "5 min"),

                    ("Relaxed Walking", "15 min")
                ]
            }

        ]
    }

}


# ============================================================
# NUTRITION TIPS
# ============================================================

NUTRITION_TIPS = {


    "weight_loss": [

        "Drink enough water throughout the day.",

        "Include vegetables and fruits in your meals.",

        "Choose balanced portions instead of skipping meals.",

        "Include protein sources such as eggs, fish, beans or curd.",

        "Prefer whole foods and limit highly processed snacks."

    ],


    "muscle_gain": [

        "Include a good protein source in your meals.",

        "Combine protein with carbohydrates for workout energy.",

        "Stay hydrated before and after exercise.",

        "Include nutrient-rich foods such as eggs, fish, beans and dairy.",

        "Allow enough rest and recovery between workouts."

    ],


    "general_fitness": [

        "Maintain a balanced diet with vegetables, fruits and protein.",

        "Drink water regularly throughout the day.",

        "Avoid relying heavily on sugary drinks.",

        "Include different food groups in your daily meals.",

        "Try to maintain consistent meal and sleep routines."

    ],


    "flexibility": [

        "Stay hydrated throughout the day.",

        "Include fruits and vegetables regularly.",

        "Eat balanced meals to support daily activity.",

        "Include protein sources in your meals.",

        "Good sleep and recovery are important for mobility."

    ]

}


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if "user_id" in session:

        if session.get("role") == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# USER REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if "user_id" in session:

        if session.get("role") == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()


        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        password = request.form.get(
            "password",
            ""
        )


        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not name or not email or not password:

            flash(
                "Please fill all the fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        conn = get_db()


        existing_user = conn.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,

            (email,)
        ).fetchone()


        if existing_user:

            conn.close()

            flash(
                "Email already registered. Please login.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # ----------------------------------------------------
        # HASH PASSWORD
        # ----------------------------------------------------

        hashed_password = generate_password_hash(
            password
        )


        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        conn.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password,
                role,
                created_at
            )

            VALUES (?, ?, ?, ?, ?)
            """,

            (
                name,

                email,

                hashed_password,

                "user",

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )


        conn.commit()

        conn.close()


        flash(
            "Registration successful! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# ============================================================
# USER LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if "user_id" in session:

        if session.get("role") == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        password = request.form.get(
            "password",
            ""
        )


        if not email or not password:

            flash(
                "Please enter email and password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        conn = get_db()


        # Only USER accounts can use this login

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            AND role = 'user'
            """,

            (email,)
        ).fetchone()


        conn.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            session["role"] = "user"


            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid user email or password.",
            "error"
        )


    return render_template(
        "login.html"
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if "user_id" in session:

        if session.get("role") == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        password = request.form.get(
            "password",
            ""
        )


        if not email or not password:

            flash(
                "Please enter admin email and password.",
                "error"
            )

            return redirect(
                url_for("admin_login")
            )


        conn = get_db()


        admin = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            AND role = 'admin'
            """,

            (email,)
        ).fetchone()


        conn.close()


        if admin and check_password_hash(
            admin["password"],
            password
        ):

            session["user_id"] = admin["id"]

            session["user_name"] = admin["name"]

            session["user_email"] = admin["email"]

            session["role"] = "admin"


            return redirect(
                url_for("admin")
            )


        flash(
            "Invalid admin email or password.",
            "error"
        )


    return render_template(
        "admin_login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out successfully.",
        "success"
    )


    return redirect(
        url_for("login")
    )


# ============================================================
# USER DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin")
        )


    return render_template(
        "index.html",

        user_name=session.get(
            "user_name"
        )
    )


# ============================================================
# GENERATE 7-DAY FITNESS PLAN
# ============================================================

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin")
        )


    user_id = session["user_id"]


    # --------------------------------------------------------
    # GET FORM DATA
    # --------------------------------------------------------

    name = request.form.get(
        "name",
        ""
    ).strip()


    age = request.form.get(
        "age",
        ""
    )


    gender = request.form.get(
        "gender",
        ""
    )


    height = request.form.get(
        "height",
        ""
    )


    weight = request.form.get(
        "weight",
        ""
    )


    goal = request.form.get(
        "goal",
        ""
    )


    level = request.form.get(
        "level",
        ""
    )


    # --------------------------------------------------------
    # REQUIRED FIELD CHECK
    # --------------------------------------------------------

    if not all([
        name,
        age,
        gender,
        height,
        weight,
        goal,
        level
    ]):

        flash(
            "Please fill all the fitness details.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    # --------------------------------------------------------
    # NUMBER CONVERSION
    # --------------------------------------------------------

    try:

        age = int(age)

        height = float(height)

        weight = float(weight)

    except ValueError:

        flash(
            "Please enter valid numbers.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if age < 13 or age > 100:

        flash(
            "Please enter a valid age between 13 and 100.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    if height < 80 or height > 250:

        flash(
            "Please enter a valid height.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    if weight < 20 or weight > 300:

        flash(
            "Please enter a valid weight.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    # --------------------------------------------------------
    # SELECT WORKOUT
    # --------------------------------------------------------

    selected_plan = WORKOUT_DATA.get(
        goal
    )


    if not selected_plan:

        flash(
            "Please select a valid fitness goal.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    workout_plan = selected_plan["days"]


    nutrition_tips = NUTRITION_TIPS.get(
        goal,
        []
    )


    conn = get_db()


    # --------------------------------------------------------
    # SAVE FITNESS PROFILE
    # --------------------------------------------------------

    cursor = conn.execute(
        """
        INSERT INTO fitness_profiles
        (
            user_id,
            age,
            gender,
            height,
            weight,
            goal,
            level,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            user_id,

            age,

            gender,

            height,

            weight,

            goal,

            level,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    profile_id = cursor.lastrowid


    # --------------------------------------------------------
    # SAVE FITNESS PLAN
    # --------------------------------------------------------

    cursor = conn.execute(
        """
        INSERT INTO plans
        (
            user_id,
            profile_id,
            workout_plan,
            nutrition_tips,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            user_id,

            profile_id,

            json.dumps(
                workout_plan
            ),

            json.dumps(
                nutrition_tips
            ),

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    plan_id = cursor.lastrowid


    conn.commit()

    conn.close()


    return redirect(
        url_for(
            "result",
            plan_id=plan_id
        )
    )


# ============================================================
# RESULT PAGE
# ============================================================

@app.route(
    "/result/<int:plan_id>"
)
def result(plan_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin")
        )


    user_id = session["user_id"]


    conn = get_db()


    data = conn.execute(
        """
        SELECT

            plans.id AS plan_id,

            plans.workout_plan,

            plans.nutrition_tips,

            plans.created_at,

            fitness_profiles.age,

            fitness_profiles.gender,

            fitness_profiles.height,

            fitness_profiles.weight,

            fitness_profiles.goal,

            fitness_profiles.level

        FROM plans

        JOIN fitness_profiles

        ON plans.profile_id =
           fitness_profiles.id

        WHERE plans.id = ?

        AND plans.user_id = ?
        """,

        (
            plan_id,

            user_id
        )
    ).fetchone()


    conn.close()


    if not data:

        return "Plan not found", 404


    workout_plan = json.loads(
        data["workout_plan"]
    )


    nutrition_tips = json.loads(
        data["nutrition_tips"]
    )


    # --------------------------------------------------------
    # BMI CALCULATION
    # --------------------------------------------------------

    height_m = data["height"] / 100


    bmi = round(
        data["weight"] /
        (height_m * height_m),
        1
    )


    return render_template(
        "result.html",

        user=data,

        workout_plan=workout_plan,

        nutrition_tips=nutrition_tips,

        bmi=bmi
    )


# ============================================================
# USER HISTORY
# ============================================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if session.get("role") != "user":

        return redirect(
            url_for("admin")
        )


    user_id = session["user_id"]


    conn = get_db()


    plans = conn.execute(
        """
        SELECT

            plans.id AS plan_id,

            users.name,

            plans.created_at,

            fitness_profiles.age,

            fitness_profiles.weight,

            fitness_profiles.goal,

            fitness_profiles.level

        FROM plans

        JOIN fitness_profiles

        ON plans.profile_id =
           fitness_profiles.id

        JOIN users

        ON plans.user_id = users.id

        WHERE plans.user_id = ?

        ORDER BY plans.id DESC
        """,

        (user_id,)
    ).fetchall()


    conn.close()


    return render_template(
        "history.html",

        plans=plans
    )

# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
def admin():

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("admin_login")
        )


    # --------------------------------------------------------
    # ADMIN ROLE CHECK
    # --------------------------------------------------------

    if session.get("role") != "admin":

        flash(
            "Admin access required.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    conn = get_db()


    # --------------------------------------------------------
    # TOTAL USERS
    # --------------------------------------------------------

    total_users = conn.execute(
        """
        SELECT COUNT(*) AS count

        FROM users

        WHERE role = 'user'
        """
    ).fetchone()["count"]


    # --------------------------------------------------------
    # TOTAL PLANS
    # --------------------------------------------------------

    total_plans = conn.execute(
        """
        SELECT COUNT(*) AS count

        FROM plans
        """
    ).fetchone()["count"]


    # --------------------------------------------------------
    # TOTAL PROFILES
    # --------------------------------------------------------

    total_profiles = conn.execute(
        """
        SELECT COUNT(*) AS count

        FROM fitness_profiles
        """
    ).fetchone()["count"]


    # --------------------------------------------------------
    # USER LIST
    # --------------------------------------------------------

    users = conn.execute(
        """
        SELECT

            users.id,

            users.name,

            users.email,

            users.created_at,

            COUNT(plans.id)
            AS plan_count

        FROM users

        LEFT JOIN plans

        ON users.id = plans.user_id

        WHERE users.role = 'user'

        GROUP BY users.id

        ORDER BY users.id DESC
        """
    ).fetchall()


    conn.close()


    return render_template(
        "admin.html",

        users=users,

        total_users=total_users,

        total_plans=total_plans,

        total_profiles=total_profiles
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    # Create database and tables

    init_db()


    # Start Flask server

    app.run(
        debug=True
    )