from database.analysis_repository import get_analysis


# ============================================================
# GET ANALYSIS ID
# ============================================================

analysis_id = input("Enter Analysis ID: ").strip()


# ============================================================
# GET ANALYSIS FROM MONGODB
# ============================================================

analysis = get_analysis(analysis_id)


# ============================================================
# CHECK RESULT
# ============================================================

if not analysis:

    print("❌ Analysis not found")

else:

    print("✅ Analysis retrieved")

    # --------------------------------------------------------
    # BASIC ANALYSIS INFORMATION
    # --------------------------------------------------------

    print("\n===== ANALYSIS =====")

    print("Analysis ID:")
    print(analysis["_id"])

    print("\nResume ID:")
    print(analysis.get("resume_id"))

    print("\nJob ID:")
    print(analysis.get("job_id"))

    print("\nMatch Score:")
    print(analysis.get("match_score"))

    # --------------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------------

    print("\nMatched Skills:")

    for skill in analysis.get("matched_skills", []):
        print("✅", skill)

    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    print("\nMissing Skills:")

    for skill in analysis.get("missing_skills", []):
        print("❌", skill)

    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    print("\n===== SKILL GAP =====")

    skill_gap = analysis.get("skill_gap")

    if skill_gap:
        print(skill_gap)

    else:
        print("No skill gap information found")

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    print("\n===== AI ANALYSIS =====")

    ai_analysis = analysis.get(
        "ai_analysis",
        {}
    )

    # --------------------------------------------------------
    # OVERALL ASSESSMENT
    # --------------------------------------------------------

    print("\nOverall Assessment:")

    print(
        ai_analysis.get(
            "overall_assessment",
            "Not available"
        )
    )

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    print("\nStrengths:")

    strengths = ai_analysis.get(
        "strengths",
        []
    )

    for item in strengths:
        print("✅", item)

    # --------------------------------------------------------
    # AI SKILL GAPS
    # --------------------------------------------------------

    print("\nAI Skill Gaps:")

    ai_skill_gaps = ai_analysis.get(
        "skill_gaps",
        []
    )

    for item in ai_skill_gaps:
        print("❌", item)

    # --------------------------------------------------------
    # LEARNING RECOMMENDATIONS
    # --------------------------------------------------------

    print("\nLearning Recommendations:")

    recommendations = ai_analysis.get(
        "learning_recommendations",
        []
    )

    for item in recommendations:
        print("📚", item)

    # --------------------------------------------------------
    # RESUME SUGGESTIONS
    # --------------------------------------------------------

    print("\nResume Suggestions:")

    suggestions = ai_analysis.get(
        "resume_suggestions",
        []
    )

    for item in suggestions:
        print("📝", item)

    # --------------------------------------------------------
    # JOB FIT
    # --------------------------------------------------------

    print("\nJob Fit:")

    print(
        ai_analysis.get(
            "job_fit",
            "Not available"
        )
    )