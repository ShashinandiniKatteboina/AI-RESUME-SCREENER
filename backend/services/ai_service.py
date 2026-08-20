import os
import json

from google import genai


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ============================================================
# AI ANALYSIS
# ============================================================

def generate_ai_analysis(
    resume,
    job,
    match_score,
    matched_skills,
    missing_skills
):

    # --------------------------------------------------------
    # Get basic information
    # --------------------------------------------------------

    job_title = job.get(
        "title",
        "Software Engineer"
    )

    job_description = job.get(
        "description",
        ""
    )

    # --------------------------------------------------------
    # Get resume information
    # --------------------------------------------------------

    parsed_resume = resume.get(
        "parsed_resume",
        {}
    )

    if not isinstance(
        parsed_resume,
        dict
    ):
        parsed_resume = {}

    name = parsed_resume.get(
        "name",
        ""
    )

    education = parsed_resume.get(
        "education",
        []
    )

    projects = parsed_resume.get(
        "projects",
        []
    )

    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI resume screening assistant.

Analyze the candidate's resume against the job.

JOB TITLE:
{job_title}

JOB DESCRIPTION:
{job_description}

MATCH SCORE:
{match_score}%

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}

CANDIDATE NAME:
{name}

EDUCATION:
{education}

PROJECTS:
{projects}

Return a concise professional analysis.

Return JSON with exactly these fields:

{{
    "overall_assessment": "...",
    "strengths": [],
    "skill_gaps": [],
    "resume_suggestions": [],
    "learning_recommendations": [],
    "job_fit": "..."
}}
"""

    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text

        # ----------------------------------------------------
        # Remove markdown code fences if Gemini adds them
        # ----------------------------------------------------

        response_text = response_text.strip()

        if response_text.startswith("```json"):

            response_text = response_text[
                7:
            ]

        elif response_text.startswith("```"):

            response_text = response_text[
                3:
            ]

        if response_text.endswith("```"):

            response_text = response_text[
                :-3
            ]

        response_text = response_text.strip()

        # ----------------------------------------------------
        # Convert JSON response
        # ----------------------------------------------------

        ai_result = json.loads(
            response_text
        )

        return ai_result

    # ========================================================
    # GEMINI ERROR
    # ========================================================

    except Exception as e:

        print(
            "⚠️ Gemini AI unavailable:",
            str(e)
        )

        # ----------------------------------------------------
        # Fallback response
        # ----------------------------------------------------

        return {

            "overall_assessment":
                f"The candidate has a {match_score}% skill match for the {job_title} position.",

            "strengths":
                matched_skills,

            "skill_gaps":
                missing_skills,

            "resume_suggestions": [
                "Quantify project achievements with measurable results.",
                "Keep the resume formatting consistent and concise."
            ],

            "learning_recommendations":
                missing_skills,

            "job_fit":
                f"{match_score}% skill match"
        }