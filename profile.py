import streamlit as st

from database import get_user, update_skills


# =========================================================
# PROFILE PAGE
# =========================================================

def show_profile(user_id):

    # -----------------------------------------------------
    # GET USER
    # -----------------------------------------------------

    user = get_user(user_id)

    if not user:
        st.error("User not found.")
        return

    user_name = user[2]
    current_know = user[3] or ""
    current_want = user[4] or ""

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="profile-header">

            <h1>👤 My Profile</h1>

            <p>
                Manage your SkillSwap profile and skills.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    st.markdown("## 🧑‍🎓 Profile Information")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Name")

        st.info(user_name)

    with col2:

        st.markdown("### Username")

        st.info(user[1])

    st.divider()

    # -----------------------------------------------------
    # SKILL UPDATE
    # -----------------------------------------------------

    st.markdown("## 🛠️ My Skills")

    st.write(
        "Update the skills you know and the skills "
        "you want to learn."
    )

    with st.form("profile_form"):

        skills_known = st.text_input(
            "💡 Skills I Know",
            value=current_know,
            placeholder="Example: Python, SQL, Canva"
        )

        skills_wanted = st.text_input(
            "🎯 Skills I Want to Learn",
            value=current_want,
            placeholder="Example: Java, Figma, AI"
        )

        save_button = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True
        )

    # -----------------------------------------------------
    # SAVE CHANGES
    # -----------------------------------------------------

    if save_button:

        if not skills_known.strip():

            st.warning(
                "Please enter at least one skill you know."
            )

        elif not skills_wanted.strip():

            st.warning(
                "Please enter at least one skill you want to learn."
            )

        else:

            update_skills(
                user_id,
                skills_known.strip(),
                skills_wanted.strip()
            )

            st.success(
                "✅ Your profile has been updated!"
            )

            st.rerun()

    # -----------------------------------------------------
    # PROFILE PREVIEW
    # -----------------------------------------------------

    st.divider()

    st.markdown("## 👀 Profile Preview")

    st.markdown(
        f"""
        <div class="profile-card">

            <h2>👤 {user_name}</h2>

            <p><b>💡 Skills I Know</b></p>

            <p>{current_know if current_know else "No skills added yet."}</p>

            <p><b>🎯 Skills I Want to Learn</b></p>

            <p>{current_want if current_want else "No skills added yet."}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # BACK TO HOME
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "⬅️ Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()