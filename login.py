import streamlit as st

from database import login_user


# =========================================================
# LOGIN PAGE
# =========================================================

def show_login():

    # -----------------------------------------------------
    # SKILLSWAP HEADER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="login-container">
            <h1>🔄 SkillSwap</h1>
            <p>Your skills are your currency.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🔐 Login")

    st.write("Login to continue exchanging skills.")

    # -----------------------------------------------------
    # LOGIN FORM
    # -----------------------------------------------------

    with st.form("login_form"):

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    # -----------------------------------------------------
    # LOGIN PROCESS
    # -----------------------------------------------------

    if login_button:

        username = username.strip()

        # Check username
        if not username:

            st.warning(
                "⚠️ Please enter your username."
            )

        # Check password
        elif not password:

            st.warning(
                "⚠️ Please enter your password."
            )

        else:

            # Check database
            user = login_user(
                username,
                password
            )

            if user:

                # -----------------------------------------
                # SAVE USER INFORMATION
                # -----------------------------------------

                st.session_state.user_id = user[0]

                st.session_state.username = user[1]

                st.session_state.page = "home"

                st.success(
                    "🎉 Login successful!"
                )

                # Go to Home
                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    # -----------------------------------------------------
    # REGISTER OPTION
    # -----------------------------------------------------

    st.write("")

    st.markdown(
        """
        <div style="text-align:center;">
            <p>Don't have an account?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "📝 Create a New Account",
        use_container_width=True
    ):

        st.session_state.page = "register"

        st.rerun()