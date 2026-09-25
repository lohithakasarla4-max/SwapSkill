import sqlite3
import json
import hashlib


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = "skillswap.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            name TEXT NOT NULL,

            know TEXT DEFAULT '[]',

            want TEXT DEFAULT '[]'

        )
        """
    )

    # ---------------- CONNECTIONS TABLE ----------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS connections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            sender_id INTEGER NOT NULL,

            receiver_id INTEGER NOT NULL,

            status TEXT DEFAULT 'pending',

            UNIQUE(sender_id, receiver_id),

            FOREIGN KEY(sender_id)
            REFERENCES users(id),

            FOREIGN KEY(receiver_id)
            REFERENCES users(id)

        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# REGISTER USER
# =========================================================

def register_user(
    username,
    password,
    name,
    know,
    want
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                name,
                know,
                want
            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                name,
                json.dumps(know),
                json.dumps(want)
            )
        )

        conn.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    finally:

        conn.close()


# =========================================================
# LOGIN USER
# =========================================================

def login_user(
    username,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            name
        FROM users

        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# GET USER BY ID
# =========================================================

def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            name,
            know,
            want

        FROM users

        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# GET ALL OTHER USERS
# =========================================================

def get_other_users(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            name,
            know,
            want

        FROM users

        WHERE id != ?
        """,
        (user_id,)
    )

    users = cursor.fetchall()

    conn.close()

    return users


# =========================================================
# CONVERT DATABASE USER TO DICTIONARY
# =========================================================

def user_to_dict(user):

    return {
        "id": user[0],
        "username": user[1],
        "name": user[2],
        "know": json.loads(user[3] or "[]"),
        "want": json.loads(user[4] or "[]")
    }


# =========================================================
# GET USERS FOR GEMINI
# =========================================================

def get_students_for_matching(user_id):

    users = get_other_users(user_id)

    students = []

    for user in users:

        students.append(
            {
                "id": user[0],

                "name": user[2],

                "know": json.loads(
                    user[3] or "[]"
                ),

                "want": json.loads(
                    user[4] or "[]"
                )
            }
        )

    return students


# =========================================================
# UPDATE USER SKILLS
# =========================================================

def update_skills(
    user_id,
    know,
    want
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET
            know = ?,
            want = ?

        WHERE id = ?
        """,
        (
            json.dumps(know),
            json.dumps(want),
            user_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# INITIALIZE DATABASE WHEN FILE IS LOADED
# =========================================================

init_database()