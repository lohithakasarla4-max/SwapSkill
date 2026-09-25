import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add your Gemini API key to the .env file."
    )


client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# AI SKILL MATCHING
# =========================================================

def find_skill_matches(
    my_skills,
    wanted_skills,
    students
):

    # -----------------------------------------------------
    # CREATE STUDENT INFORMATION
    # -----------------------------------------------------

    student_text = ""

    for student in students:

        student_text += f"""
Name: {student['name']}
Skills they know: {", ".join(student['know'])}
Skills they want to learn: {", ".join(student['want'])}

"""


    # -----------------------------------------------------
    # GEMINI PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are the AI matching assistant for SkillSwap.

SkillSwap is a peer-to-peer platform where students
exchange skills instead of paying for expensive courses.

The current student has:

Skills they already know:
{", ".join(my_skills)}

Skills they want to learn:
{", ".join(wanted_skills)}


OTHER STUDENTS
==============

{student_text}


YOUR TASK
=========

Find the best skill-exchange partners for the current
student.

A strong match happens when:

1. Another student knows something that the current
   student wants to learn.

AND

2. The current student knows something that the other
   student wants to learn.


FOR EACH MATCH, PROVIDE
=======================

### 👤 Match
Give the student's name.

### 🔄 Skill Exchange
Clearly explain:

- What the current student can teach.
- What the matched student can teach.

### ⭐ Why This Is a Good Match
Give a short and simple explanation.

### 📊 Match Score
Give a percentage from 0% to 100%.


IMPORTANT RULES
===============

- Only recommend realistic matches.
- Do not invent skills.
- Use only the skills provided.
- Prefer students with two-way skill exchanges.
- If there is no good match, clearly say that.
- Keep the response simple.
- Keep it student-friendly.
- Do not give unrelated information.
"""


    # -----------------------------------------------------
    # SEND REQUEST TO GEMINI
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )


        # -------------------------------------------------
        # CHECK RESPONSE
        # -------------------------------------------------

        if response.text:

            return response.text.strip()

        else:

            return (
                "ERROR: Gemini returned an empty response."
            )


    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        return f"ERROR: {str(e)}"