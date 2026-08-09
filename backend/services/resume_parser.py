import re


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text):

    pattern = r"(?:\+91[\s-]?)?\d{3}[\s-]?\d{3}[\s-]?\d{4}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_contact_line(text):

    lines = text.splitlines()

    for line in lines:

        if "|" in line and re.search(
            r"\d{3}[\s-]?\d{3}[\s-]?\d{4}",
            line
        ):

            parts = [part.strip() for part in line.split("|")]

            return parts

    return []


def extract_name(text):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "bachelor" in line.lower():
            break

        if re.match(r"^[A-Za-z.\s]+$", line):
            return line.strip()

    return None


def extract_education_section(text):

    lines = text.splitlines()

    education_lines = []

    inside_education = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Start of education section
        if line.upper() == "EDUCATION":
            inside_education = True
            continue

        # Stop at the next major section
        if inside_education and line.upper() in [
            "PROJECT",
            "PROJECTS",
            "SKILLS",
            "CERTIFICATIONS",
            "EXPERIENCE",
            "WORK EXPERIENCE"
        ]:
            break

        if inside_education:
            education_lines.append(line)

    return education_lines


def parse_education(education_lines):

    education = []
    i = 0

    while i < len(education_lines):

        first_line = education_lines[i]

        # Detect date such as:
        # Sept 2023 - April 2027
        # June 2021 - Mar 2023
        # May 2021
        date_match = re.search(
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*"
            r"\s+\d{4}"
            r"(?:\s*[–-]\s*"
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*"
            r"\s+\d{4})?",
            first_line,
            re.IGNORECASE
        )

        if date_match:

            # Institution is everything before the date
            institution = first_line[:date_match.start()].strip()

            degree = None
            score = None

            # Usually degree / score are on the next line
            if i + 1 < len(education_lines):

                second_line = education_lines[i + 1]

                # Extract CGPA
                cgpa_match = re.search(
                    r"CGPA\s*[:\-]?\s*([\d.]+)",
                    second_line,
                    re.IGNORECASE
                )

                # Extract GPA
                gpa_match = re.search(
                    r"GPA\s*[–\-:]?\s*([\d.]+)",
                    second_line,
                    re.IGNORECASE
                )

                # Extract total marks
                marks_match = re.search(
                    r"Total Marks\s*[–\-:]?\s*(\d+)",
                    second_line,
                    re.IGNORECASE
                )

                # Extract degree
                if "|" in second_line:
                    degree = second_line.split("|")[0].strip()
                else:
                    degree = second_line.strip()

                # Extract score
                if cgpa_match:
                    score = "CGPA: " + cgpa_match.group(1)

                elif gpa_match:
                    score = "GPA: " + gpa_match.group(1)

                elif marks_match:
                    score = "Total Marks: " + marks_match.group(1)

                # Remove score information from degree
                if cgpa_match:

                    degree = re.sub(
                        r"CGPA\s*[:\-]?\s*[\d.]+",
                        "",
                        degree,
                        flags=re.IGNORECASE
                    ).strip()

                elif gpa_match:

                    degree = re.sub(
                        r"GPA\s*[–\-:]?\s*[\d.]+",
                        "",
                        degree,
                        flags=re.IGNORECASE
                    ).strip()

                elif marks_match:

                    degree = re.sub(
                        r"Total Marks\s*[–\-:]?\s*\d+",
                        "",
                        degree,
                        flags=re.IGNORECASE
                    ).strip()

                # Remove location from degree
                degree = re.sub(
                    r"(?:Hyderabad|Khammam),\s*Telangana",
                    "",
                    degree,
                    flags=re.IGNORECASE
                ).strip()

                i += 1

            education.append({
                "institution": institution,
                "degree": degree,
                "score": score
            })

        i += 1

    return education

def extract_project_section(text):

    lines = text.splitlines()

    project_lines = []

    inside_project = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Start project section
        if line.upper() in ["PROJECT", "PROJECTS"]:
            inside_project = True
            continue

        # Stop at next major section
        if inside_project and line.upper() in [
            "SKILLS",
            "CERTIFICATIONS",
            "EXPERIENCE",
            "WORK EXPERIENCE",
            "EDUCATION"
        ]:
            break

        if inside_project:
            project_lines.append(line)

    return project_lines

def parse_projects(project_lines):

    projects = []

    i = 0

    while i < len(project_lines):

        # A project title is followed by Tech Stack
        if (
            i + 1 < len(project_lines)
            and project_lines[i + 1].lower().startswith("tech stack:")
        ):

            title = project_lines[i].strip()

            # Extract tech stack
            tech_stack_line = project_lines[i + 1]

            tech_stack_text = tech_stack_line.split(":", 1)[1].strip()

            tech_stack = [
                skill.strip()
                for skill in tech_stack_text.split(",")
            ]

            # Collect description until the next
            # project title + Tech Stack
            description_lines = []

            i += 2

            while i < len(project_lines):

                # Check whether next project starts
                if (
                    i + 1 < len(project_lines)
                    and project_lines[i + 1].lower().startswith("tech stack:")
                ):
                    break

                description_lines.append(
                    project_lines[i].strip()
                )

                i += 1

            description = " ".join(description_lines)

            projects.append({
                "title": title,
                "tech_stack": tech_stack,
                "description": description
            })

        else:
            i += 1

    return projects

def extract_skills_section(text):

    lines = text.splitlines()

    skills = {}

    inside_skills = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Start of skills section
        if line.upper() == "SKILLS":
            inside_skills = True
            continue

        # Stop at next major section
        if inside_skills and line.upper() in [
            "CERTIFICATIONS",
            "PROJECT",
            "PROJECTS",
            "EDUCATION",
            "EXPERIENCE",
            "WORK EXPERIENCE"
        ]:
            break

        if inside_skills and ":" in line:

            category, skill_text = line.split(":", 1)

            category = category.strip()
            skill_text = skill_text.strip()

            skills[category] = [
                skill.strip()
                for skill in skill_text.split(",")
            ]

    return skills

def extract_certifications_section(text):

    lines = text.splitlines()

    certification_lines = []

    inside_certifications = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Start of certifications section
        if line.upper() in [
            "CERTIFICATIONS",
            "CERTIFICATION"
        ]:
            inside_certifications = True
            continue

        # Stop at another major section
        if inside_certifications and line.upper() in [
            "SKILLS",
            "PROJECT",
            "PROJECTS",
            "EDUCATION",
            "EXPERIENCE",
            "WORK EXPERIENCE"
        ]:
            break

        if inside_certifications:
            certification_lines.append(line)

    return certification_lines
def parse_certifications(certification_lines):

    certifications = []

    for line in certification_lines:

        line = line.strip()

        if not line:
            continue

        # Separate additional details
        parts = [part.strip() for part in line.split("|")]

        main_part = parts[0]

        details = " | ".join(parts[1:])

        # Split certification name and issuer
        # Example:
        # Programming in Java – NPTEL
        if "–" in main_part:
            name, issuer = main_part.split("–", 1)

        elif "-" in main_part:
            name, issuer = main_part.split("-", 1)

        else:
            name = main_part
            issuer = ""

        certifications.append({
            "name": name.strip(),
            "issuer": issuer.strip(),
            "details": details
        })

    return certifications

def extract_experience_section(text):

    lines = text.splitlines()

    experience_lines = []

    inside_experience = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Start of experience section
        if line.upper() in [
            "EXPERIENCE",
            "WORK EXPERIENCE",
            "PROFESSIONAL EXPERIENCE",
            "WORK HISTORY"
        ]:
            inside_experience = True
            continue

        # Stop at another major section
        if inside_experience and line.upper() in [
            "SKILLS",
            "PROJECT",
            "PROJECTS",
            "EDUCATION",
            "CERTIFICATIONS",
            "CERTIFICATION"
        ]:
            break

        if inside_experience:
            experience_lines.append(line)

    return experience_lines
def parse_resume(text):

    # Basic information
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    # Education
    education_lines = extract_education_section(text)
    education = parse_education(education_lines)

    # Projects
    project_lines = extract_project_section(text)
    projects = parse_projects(project_lines)

    # Skills
    skills = extract_skills_section(text)

    # Certifications
    certification_lines = extract_certifications_section(text)
    certifications = parse_certifications(certification_lines)

    # Experience
    experience = extract_experience_section(text)

    # Final structured resume
    resume = {
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "skills": skills,
        "projects": projects,
        "certifications": certifications,
        "experience": experience
    }

    return resume