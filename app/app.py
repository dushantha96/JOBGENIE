from contact_info import contact_info

# avoid name collision
from service_data import services as service_data_list
from accordion import (
    get_about_accordion,
    get_contact_accordion,
    get_service_accordion,
)
from flask import render_template, redirect, flash, url_for, abort
from forms import ContactForm, ResumeMatchForm
from skill_extractor import SKILL_KEYWORDS
from flask import Flask, render_template, request
from resume_utils import parse_resume, extract_text_from_pdf
from matcher import match_resume_to_job
import os

app = Flask(__name__)
app.secret_key = "your-very-secret-key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

STOPWORDS = {
    "the",
    "and",
    "or",
    "a",
    "an",
    "in",
    "on",
    "at",
    "to",
    "for",
    "with",
    "of",
    "by",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "has",
    "have",
    "had",
    "from",
    "that",
    "this",
    "it",
    "your",
    "but",
    "not",
    "can",
    "will",
    "we",
    "they",
    "their",
    "which",
    "also",
    "if",
    "about",
    "all",
    "more",
    "other",
    "some",
    "such",
    "no",
    "any",
    "may",
    "should",
    "do",
    "does",
    "did",
    "so",
    "these",
    "those",
    "i",
    "you",
    "he",
    "she",
    "him",
    "her",
    "them",
    "my",
    "our",
    "us",
    "what",
    "when",
    "where",
    "how",
    "why",
    "who",
    "whom",
}


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    error = None
    form = ResumeMatchForm()

    if form.validate_on_submit():
        uploaded_file = form.resume_file.data
        job_text = form.job.data

        filename = uploaded_file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(file_path)

        resume_text = extract_text_from_pdf(file_path)
        parsed = parse_resume(resume_text)
        score, matched_skills = match_resume_to_job(resume_text, job_text)

        if score >= 85:
            verdict = "Excellent Fit – Highly recommended"
        elif score >= 70:
            verdict = "Good Fit – Likely suitable"
        elif score >= 50:
            verdict = "Moderate Fit – Review recommended"
        elif score >= 30:
            verdict = "Low Fit – Probably not suitable"
        else:
            verdict = "Poor Fit – Not recommended"

        resume_set = set(skill.lower() for skill in matched_skills)
        jd_words = set(word.lower().strip(".,") for word in job_text.split())
        jd_skills = set(word for word in jd_words if word in SKILL_KEYWORDS)

        missing_skills = jd_skills - resume_set

        filtered_missing_skills = [
            skill
            for skill in missing_skills
            if skill not in STOPWORDS and len(skill) > 1 and skill.isalpha()
        ]

        limited_missing_skills = sorted(filtered_missing_skills)[:10]

        if score < 50 and limited_missing_skills:
            feedback = (
                "Your skills do not match the job description well. "
                "Consider acquiring or emphasizing: "
                + ", ".join(limited_missing_skills)
            )
        else:
            feedback = "Your skills match the job description well."

        result = {
            "parsed": parsed,
            "score": score,
            "verdict": verdict,
            "feedback": feedback,
        }

    return render_template("index.html", form=form, result=result, error=error)


@app.context_processor
def inject_contact_info():
    return dict(contact_info=contact_info)


@app.route("/about")
def about():
    accordion_services = get_about_accordion()
    return render_template("about.html", accordion_services=accordion_services)


@app.route("/footer")
def footer():
    return render_template("footer.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    contact_accordion = get_contact_accordion()
    if form.validate_on_submit():
        flash("Your message was submitted successfully!", "success")
        return redirect(url_for("contact"))
    return render_template(
        "contact.html", form=form, contact_accordion=contact_accordion
    )


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/services")
@app.route("/services/<service_name>")
def services(service_name=None):
    # existing service templates mapping
    service_templates = {
        "resume-matching": "service_partials/resume_matching.html",
        "job-description": "service_partials/job_description.html",
        "resume-score": "service_partials/resume_score.html",
        "smart-screening": "service_partials/smart_screening.html",
    }

    # links data
    sidebar_links = [
        {
            "name": "Resume Matching",
            "endpoint": "services",
            "service_name": "resume-matching",
        },
        {
            "name": "Job Description Analysis",
            "endpoint": "services",
            "service_name": "job-description",
        },
        {
            "name": "Resume Score Calculator",
            "endpoint": "services",
            "service_name": "resume-score",
        },
        {
            "name": "Smart Resume Screening",
            "endpoint": "services",
            "service_name": "smart-screening",
        },
    ]

    service_accordion = get_service_accordion()

    if service_name is None:
        return render_template(
            "services.html",
            content_template=None,
            sidebar_links=sidebar_links,
            services=service_data_list,
            service_accordion=service_accordion,
        )

    content_template = service_templates.get(service_name)
    if not content_template:
        abort(404)

    # Match service by route key
    service_index_map = {
        "resume-matching": 0,
        "job-description": 1,
        "resume-score": 2,
        "smart-screening": 3,
    }
    service_index = service_index_map.get(service_name)
    selected_service = service_data_list[service_index]
    features = selected_service["features"]

    return render_template(
        "services.html",
        content_template=content_template,
        sidebar_links=sidebar_links,
        services=service_data_list,
        features=features,
        service=selected_service,
        service_accordion=service_accordion,
    )


if __name__ == "__main__":
    app.run(debug=True)
