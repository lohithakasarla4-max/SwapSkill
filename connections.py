import sqlite3
import json
import streamlit as st


# =========================================================
# DATABASE CONNECTION
# =========================================================

DB_PATH = "skillswap.db"


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


# =========================================================
# SEND CONNECTION REQUEST
# =========================================================

def send_request(sender_id, receiver_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO connections
            (
                sender_id,
                receiver_id,
                status
            )
            VALUES (?, ?, 'pending')
            """,
            (
                sender_id,
                receiver_id
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================================================
# UPDATE REQUEST
# =========================================================

def update_request(connection_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE connections
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            connection_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# GET PENDING REQUESTS
# =========================================================

def get_requests(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            connections.id,
            users.id,
            users.name,
            users.know,
            users.want

        FROM connections

        JOIN users
        ON connections.sender_id = users.id

        WHERE connections.receiver_id = ?
        AND connections.status = 'pending'
        """,
        (user_id,)
    )

    requests = cursor.fetchall()

    conn.close()

    return requests


# =========================================================
# GET ACCEPTED CONNECTIONS
# =========================================================

def get_connections(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            connections.id,
            users.id,
            users.name,
            users.know,
            users.want

        FROM connections

        JOIN users

        ON
        (
            CASE

                WHEN connections.sender_id = ?
                THEN connections.receiver_id

                ELSE connections.sender_id

            END
        ) = users.id

        WHERE
        (
            connections.sender_id = ?
            OR connections.receiver_id = ?
        )

        AND connections.status = 'accepted'
        """,
        (
            user_id,
            user_id,
            user_id
        )
    )

    connections = cursor.fetchall()

    conn.close()

    return connections


# =========================================================
# CONNECTIONS PAGE
# =========================================================

def show_connections(user_id):

    st.title("🤝 Connections")

    # -----------------------------------------------------
    # CONNECTION REQUESTS
    # -----------------------------------------------------

    st.subheader("📩 Connection Requests")

    requests = get_requests(user_id)

    if not requests:

        st.info(
            "You don't have any pending requests."
        )

    else:

        for request in requests:

            connection_id = request[0]

            other_user_id = request[1]

            name = request[2]

            know = json.loads(
                request[3] or "[]"
            )

            want = json.loads(
                request[4] or "[]"
            )


            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:15px;
                    margin-bottom:10px;
                    border:1px solid #E7DDF2;
                ">

                    <h3>👤 {name}</h3>

                    <p>
                    <b>Skills they know:</b>
                    {", ".join(know)}
                    </p>

                    <p>
                    <b>Skills they want to learn:</b>
                    {", ".join(want)}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✅ Accept",
                    key=f"accept_{connection_id}",
                    use_container_width=True
                ):

                    update_request(
                        connection_id,
                        "accepted"
                    )

                    st.success(
                        f"You are now connected with {name}! 🎉"
                    )

                    st.rerun()


            with col2:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{connection_id}",
                    use_container_width=True
                ):

                    update_request(
                        connection_id,
                        "rejected"
                    )

                    st.info(
                        "Connection request rejected."
                    )

                    st.rerun()


    # -----------------------------------------------------
    # ACCEPTED CONNECTIONS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader("🌟 My Connections")

    connections = get_connections(user_id)

    if not connections:

        st.info(
            "You don't have any connections yet."
        )

    else:

        for connection in connections:

            connection_id = connection[0]

            other_user_id = connection[1]

            name = connection[2]

            know = json.loads(
                connection[3] or "[]"
            )

            want = json.loads(
                connection[4] or "[]"
            )


            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:15px;
                    margin-bottom:15px;
                    border:1px solid #E7DDF2;
                ">

                    <h3>
                        🤝 {name}
                    </h3>

                    <p>
                        <b>Can teach:</b>
                        {", ".join(know)}
                    </p>

                    <p>
                        <b>Wants to learn:</b>
                        {", ".join(want)}
                    </p>

                    <p style="color:#4CAF50;">
                        🟢 Connected
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )