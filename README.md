# 🤝 SwapSkill

> **A Peer-to-Peer Skill-Exchange Platform built with Python and Streamlit**

**SwapSkill** is an interactive web platform designed to democratize learning through peer-to-peer knowledge sharing. Instead of paying for expensive online courses, users can offer their own expertise in exchange for learning new skills from community members.

---

## ✨ Features

* **User Authentication:** Secure registration and login workflow.
* **Profile Management:** Manage skill offerings, learning interests, and user bios.
* **Smart Skill Matching:** Dynamic match generation based on complementary user skill sets.
* **Exchange Connections:** Send, accept, and manage active skill-swap connection requests.
* **Streamlit UI:** Clean, multi-page web dashboard powered by custom styling.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** Streamlit
* **Database:** SQLite (`skillswap.db`)
* **Styling:** CSS3 (`style.css`)

---

## 📂 Project Structure

```text
SwapSkill/
├── app.py              # Main Streamlit application entry point
├── home.py             # Home page layout
├── login.py            # User authentication (Login)
├── register.py         # User account creation
├── profile.py          # User profile management
├── matches.py          # Peer-to-peer skill matching engine
├── connections.py      # Skill-swap connection requests
├── database.py         # Database connection and helper functions
├── agent.py            # AI assistant and recommendation module
├── style.css           # Custom UI styling
└── logo.png            # Application logo
