from skill_extractor import extract_skills


def match_resume_to_job(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = set(resume_skills).intersection(job_skills)
    score = int(len(matched) / max(len(job_skills), 1) * 100)

    return score, list(matched)
