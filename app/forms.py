from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ContactForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Regexp(r"^[A-Za-z\s]+$", message="Only letters allowed"),
        ],
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Regexp(r"^[A-Za-z\s]+$", message="Only letters allowed"),
        ],
    )

    email = StringField("Email", validators=[DataRequired(), Email()])

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(r"^[0-9]{10,15}$", message="Enter a valid phone number"),
        ],
    )

    user_question = TextAreaField(
        "Your Question", validators=[DataRequired(), Length(min=10)]
    )

    user_knew = TextAreaField(
        "How did you hear about JOBGENIE?", validators=[DataRequired(), Length(min=5)]
    )

    submit = SubmitField("Submit")


# ✅ NEW Form
class ResumeMatchForm(FlaskForm):
    resume_file = FileField(
        "Upload Resume in PDF only:",
        validators=[FileRequired(), FileAllowed(["pdf"], "PDF files only!")],
    )
    job = TextAreaField("Paste Job Description:", validators=[DataRequired()])
    submit = SubmitField("Match")
