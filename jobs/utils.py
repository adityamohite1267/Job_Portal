from pdfminer.high_level import extract_text

def extract_resume_text(resume_file):  # this extract text from uploaded resume pdf 
    try:
        text = extract_text(resume_file)
        return text.lower()
    except Exception as e:
        print("Resume extraction error:",e)
        return ""
    
def calculate_match_score(job_skills,resume_text):
    """Compaire job skills with resume text and return percentage match score"""
    matched_skills = 0
    total_skills = job_skills.count()

    if total_skills == 0:
        return 0
    for skill in job_skills:
        skill_name = skill.name.lower()

        if skill_name in resume_text:
            matched_skills +=1
    score = (matched_skills / total_skills)*100
    return round(score)