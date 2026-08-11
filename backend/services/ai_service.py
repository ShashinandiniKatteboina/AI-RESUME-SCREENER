import os
import json

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GET GEMINI API KEY
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# GENERATE AI ANALYSIS
# ============================================================

def generate_ai_analysis(
    resume,
    job_description,
    match_score,
    matched_skills,
    missing_skills
):

    prompt = f"""
You are an AI career assistant.

Your task is to analyze a candidate's resume against
a given job description.

============================================================
CANDIDATE RESUME
============================================================

{resume}


============================================================
JOB DESCRIPTION
============================================================

{job_description}


============================================================
MATCHING INFORMATION
============================================================

MATCH SCORE:
{match_score}%

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}


============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT use:
```json

Do NOT add any explanation outside the JSON.

Use exactly this structure:

{{
    "overall_assessment": "Short professional assessment",

    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],

    "skill_gaps": [
        "missing skill 1",
        "missing skill 2"
    ],

    "learning_recommendations": [
        "recommendation 1",
        "recommendation 2",
        "recommendation 3"
    ],

    "resume_suggestions": [
        "suggestion 1",
        "suggestion 2"
    ],

    "job_fit": "Short explanation of how well the candidate fits the job"
}}


============================================================
IMPORTANT RULES
============================================================

1. Do not invent skills or experience.

2. Base the analysis ONLY on the provided resume,
   job description and matching information.

3. Mention only relevant skill gaps.

4. Keep recommendations practical for a
   software engineering candidate.

5. Prioritize missing skills based on their importance
   to the job.

6. For learning_recommendations:
   - Give 3 to 5 actionable recommendations.
   - Start with the most important missing skill.
   - Briefly explain what the candidate should learn
     or practice.
   - Do not recommend skills that are already present
     in the resume.

7. For resume_suggestions:
   - Suggest improvements based only on the provided resume.
   - Do not invent experience.
   - Do not tell the candidate to falsely add skills
     they do not have.

8. For strengths:
   - Mention only skills, projects, education,
     certifications or experience actually present
     in the resume.

9. For skill_gaps:
   - Include relevant missing skills from the
     job requirements.

10. Keep the overall assessment concise and professional.

11. Keep the job fit explanation concise.

12. Return valid JSON only.
"""


    # ========================================================
    # SEND REQUEST TO GEMINI
    # ========================================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )


    # ========================================================
    # GET RESPONSE TEXT
    # ========================================================

    response_text = response.text.strip()


    # ========================================================
    # REMOVE MARKDOWN CODE FENCES
    # ========================================================

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]


    if response_text.endswith("```"):
        response_text = response_text[:-3]


    response_text = response_text.strip()


    # ========================================================
    # CONVERT JSON STRING TO PYTHON DICTIONARY
    # ========================================================

    try:

        ai_result = json.loads(response_text)

    except json.JSONDecodeError:

        print("⚠️ Gemini returned invalid JSON")

        print("===== RAW GEMINI RESPONSE =====")
        print(response_text)

        # Safe fallback
        ai_result = {
            "overall_assessment": response_text,

            "strengths": [],

            "skill_gaps": missing_skills,

            "learning_recommendations": [],

            "resume_suggestions": [],

            "job_fit": ""
        }


    # ========================================================
    # ENSURE REQUIRED FIELDS EXIST
    # ========================================================

    ai_result.setdefault(
        "overall_assessment",
        ""
    )

    ai_result.setdefault(
        "strengths",
        []
    )

    ai_result.setdefault(
        "skill_gaps",
        missing_skills
    )

    ai_result.setdefault(
        "learning_recommendations",
        []
    )

    ai_result.setdefault(
        "resume_suggestions",
        []
    )

    ai_result.setdefault(
        "job_fit",
        ""
    )


    # ========================================================
    # RETURN STRUCTURED RESULT
    # ========================================================

    return ai_result