import streamlit as st

from database import register_user


# =========================================================
# REGISTER PAGE
# =========================================================

def show_register():

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="register-header">

            <h1>🔄 SkillSwap</h1>

            <p>
                Your skills are your currency.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 📝 Create Your Account")

    st.write(
        "Join SkillSwap and start exchanging skills with other students."
    )

    # -----------------------------------------------------
    # REGISTRATION FORM
    # -----------------------------------------------------

    with st.form("register_form"):

        name = st.text_input(
            "👤 Full Name",
            placeholder="Enter your name"
        )

        username = st.text_input(
            "🔑 Username",
            placeholder="Choose a username"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            placeholder="Enter your password again"
        )

        skills_known = st.text_input(
            "💡 Skills You Know",
            placeholder="Example: Python, SQL, Canva"
        )

        skills_wanted = st.text_input(
            "🎯 Skills You Want to Learn",
            placeholder="Example: Java, Figma, AI"
        )

        register_button = st.form_submit_button(
            "🚀 Create Account",
            use_container_width=True
        )

    # -----------------------------------------------------
    # REGISTER BUTTON
    # -----------------------------------------------------

    if register_button:

        # Check empty fields
        if not name.strip():
            st.warning("Please enter your name.")

        elif not username.strip():
            st.warning("Please enter a username.")

        elif not password:
            st.warning("Please create a password.")

        elif not confirm_password:
            st.warning("Please confirm your password.")

        elif password != confirm_password:
            st.error("❌ Passwords do not match.")

        elif not skills_known.strip():
            st.warning(
                "Please enter at least one skill you know."
            )

        elif not skills_wanted.strip():
            st.warning(
                "Please enter at least one skill you want to learn."
            )

        else:

            # -------------------------------------------------
            # CREATE ACCOUNT
            # -------------------------------------------------

            result = register_user(
                username.strip(),
                password,
                name.strip(),
                skills_known.strip(),
                skills_wanted.strip()
            )

            if result:

                st.success(
                    "🎉 Account created successfully!"
                )

                st.info(
                    "You can now login using your username and password."
                )

                # Go to login
                if st.button(
                    "🔐 Go to Login",
                    use_container_width=True
                ):

                    st.session_state.page = "login"
                    st.rerun()

            else:

                st.error(
                    "❌ Username already exists. "
                    "Please choose another username."
                )

    # -----------------------------------------------------
    # LOGIN OPTION
    # -----------------------------------------------------

    st.write("")

    st.markdown(
        "Already have an account?"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        st.session_state.page = "login"
        st.rerun()