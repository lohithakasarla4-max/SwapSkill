import os
import streamlit as st

from database import init_database
from login import show_login
from register import show_register
from home import show_home
from matches import show_matches
from connections import show_connections
from profile import show_profile


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SkillSwap",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSS_PATH = os.path.join(BASE_DIR, "style.css")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

init_database()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

if os.path.exists(CSS_PATH):

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# SPLASH SCREEN
# --------------------------------------------------

if not st.session_state.splash_shown:

    if os.path.exists(LOGO_PATH):

        with st.container(key="skillswap_splash"):

            st.image(
                LOGO_PATH,
                width=600
            )

    else:

        st.error(
            f"❌ logo.png was not found.\n\n"
            f"Expected location:\n{LOGO_PATH}"
        )

    # Important:
    # Do NOT use time.sleep()
    # Do NOT use st.rerun() here.

    st.session_state.splash_shown = True


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

if st.session_state.user_id:

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-title">
                🔄 SkillSwap
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"Welcome, **{st.session_state.username}** 👋"
        )

        st.divider()

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.session_state.page = "home"
            st.rerun()

        if st.button(
            "🤝 Matches",
            use_container_width=True
        ):

            st.session_state.page = "matches"
            st.rerun()

        if st.button(
            "💬 Connections",
            use_container_width=True
        ):

            st.session_state.page = "connections"
            st.rerun()

        if st.button(
            "👤 Profile",
            use_container_width=True
        ):

            st.session_state.page = "profile"
            st.rerun()

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.page = "login"
            st.session_state.splash_shown = False

            st.rerun()


# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------

if st.session_state.page == "login":

    show_login()


elif st.session_state.page == "register":

    show_register()


elif st.session_state.page == "home":

    if st.session_state.user_id:

        show_home(
            st.session_state.user_id
        )

    else:

        st.session_state.page = "login"
        st.rerun()


elif st.session_state.page == "matches":

    if st.session_state.user_id:

        show_matches(
            st.session_state.user_id
        )

    else:

        st.session_state.page = "login"
        st.rerun()


elif st.session_state.page == "connections":

    if st.session_state.user_id:

        show_connections(
            st.session_state.user_id
        )

    else:

        st.session_state.page = "login"
        st.rerun()


elif st.session_state.page == "profile":

    if st.session_state.user_id:

        show_profile(
            st.session_state.user_id
        )

    else:

        st.session_state.page = "login"
        st.rerun()


else:

    st.session_state.page = "login"
    st.rerun()