import streamlit as st

from database import get_user, get_students_for_matching
from agent import find_skill_matches


# =========================================================
# MATCHES PAGE
# =========================================================

def show_matches(user_id):

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
        <div class="matches-header">

            <h1>🤝 Find Your Skill Matches</h1>

            <p>
                Hi <b>{user_name}</b>! Let's find students
                who can teach you what you want to learn.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # CURRENT SKILLS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💡 You Can Teach")

        if know:
            st.info(know)
        else:
            st.warning("Add some skills you know first.")

    with col2:

        st.markdown("### 🎯 You Want to Learn")

        if want:
            st.success(want)
        else:
            st.warning("Add skills you want to learn first.")

    st.divider()

    # -----------------------------------------------------
    # FIND MATCHES
    # -----------------------------------------------------

    st.markdown("## 🔍 AI-Powered Matching")

    st.write(
        "Gemini will compare your skills with other "
        "students and find possible skill exchanges."
    )

    if st.button(
        "✨ Find My Matches",
        use_container_width=True
    ):

        # Get other students
        students = get_students_for_matching(user_id)

        if not students:

            st.warning(
                "There are no other students registered yet."
            )

            st.info(
                "Ask your friends to create SkillSwap "
                "accounts so you can find matches."
            )

        else:

            with st.spinner(
                "🤖 Gemini is finding your best matches..."
            ):

                result = find_skill_matches(
                    know,
                    want,
                    students
                )

            # -------------------------------------------------
            # SHOW RESULT
            # -------------------------------------------------

            if result.startswith("ERROR:"):

                st.error(result)

            else:

                st.markdown("## ⭐ Your Best Matches")

                st.markdown(result)

    # -----------------------------------------------------
    # BACK BUTTON
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "⬅️ Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()