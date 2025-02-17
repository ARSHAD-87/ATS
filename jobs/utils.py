import re

def extract_salary(salary_str):
    """Extracts numeric salary value from a formatted salary string."""
    match = re.search(r'\d+', salary_str)
    return int(match.group()) if match else None

def calculate_average_salary(job_listings):
    """Calculates the average salary from a list of job salary strings."""
    salaries = [extract_salary(job.salary) for job in job_listings if extract_salary(job.salary) is not None]
    
    if salaries:
        return sum(salaries) // len(salaries) 
    return 0  
