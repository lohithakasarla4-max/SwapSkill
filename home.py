import streamlit as st

from database import get_user


# =========================================================
# HOME PAGE
# =========================================================

def show_home(user_id):

    # -----------------------------------------------------
    # GET CURRENT USER
    # -----------------------------------------------------

    user = get_user(user_id)

    if not user:
        st.error("User not found.")
        return

    user_name = user[2]

    know = user[3]
    want = user[4]

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="home-header">

            <h1>👋 Welcome, {user_name}!</h1>

            <p>
                Welcome to <b>SkillSwap</b> —
                Your skills are your currency.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # QUICK INTRO
    # -----------------------------------------------------

    st.markdown("## 🔄 Learn. Teach. Grow.")

    st.write(
        "Exchange your skills with other students "
        "and learn something new without expensive courses."
    )

    # -----------------------------------------------------
    # SKILLS SECTION
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💡 Skills You Know")

        if know:

            st.info(know)

        else:

            st.warning(
                "You haven't added your skills yet."
            )

    with col2:

        st.markdown("### 🎯 Skills You Want to Learn")

        if want:

            st.success(want)

        else:

            st.warning(
                "You haven't added skills you want to learn."
            )

    st.divider()

    # -----------------------------------------------------
    # ACTION CARDS
    # -----------------------------------------------------

    st.markdown("## 🚀 What do you want to do?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 🤝

            **Find Matches**

            Discover students who have
            skills you want to learn.
            """
        )

        if st.button(
            "Find Skill Matches",
            use_container_width=True
        ):

            st.session_state.page = "matches"
            st.rerun()

    with col2:

        st.markdown(
            """
            ### 💬

            **Connections**

            View your requests and
            accepted skill partners.
            """
        )

        if st.button(
            "View Connections",
            use_container_width=True
        ):

            st.session_state.page = "connections"
            st.rerun()

    with col3:

        st.markdown(
            """
            ### 👤

            **My Profile**

            View and update your
            SkillSwap profile.
            """
        )

        if st.button(
            "View Profile",
            use_container_width=True
        ):

            st.session_state.page = "profile"
            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SKILLSWAP MESSAGE
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="home-message">

            <h3>🌱 Everyone has something to teach.</h3>

            <p>
                You don't need to buy an expensive course.
                Your skills can help someone else,
                and their skills can help you.
            </p>

            <p>
                <b>Teach what you know → Learn what you want → Grow together.</b>
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )