import re


def extract_keywords_from_jd(jd_text):
    return re.findall(r"\b[A-Za-z\+\#]+\b", jd_text)
