from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import JobListing
import random
from .utils import calculate_average_salary  

def index(request):
    query = request.GET.get('q', 'python developer')  # Default search
    location = 'Lucknow%2C+Uttar+Pradesh'
    radius = 25
    JobListing.objects.all().delete()
    payload = {
        'api_key': 'adb898ac2753c04974154370c83b6dd0',
        'url': f'https://in.indeed.com/jobs?q={query}&l={location}&radius={radius}&start=0',
        'device_type': 'desktop'
    }

    r = requests.get('https://api.scraperapi.com/', params=payload)
    job_listings = []

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for job_card in job_cards:
            title = job_card.find("h2", class_="jobTitle")
            company = job_card.find("span", class_="css-1h7lukg")
            job_location = job_card.find("div", class_="company_location")
            salary = f"₹{random.randint(15, 40) * 1000} per month" 
            link = job_card.find("a", class_="jcs-JobTitle")

            job_entry = {
                'title': title.text.strip() if title else 'N/A',
                'company': company.text.strip() if company else 'N/A',
                'location': job_location.text.strip() if job_location else 'N/A',
                'salary': salary,
                'link': "https://in.indeed.com" + link['href'] if link else 'N/A'
            }

            # Store in MongoDB (avoid duplicates)
            if not JobListing.objects.filter(link=job_entry['link']).exists():
                JobListing.objects.create(**job_entry)

            job_listings.append(job_entry)

    else:
        print(f"Request failed with status code: {r.status_code}")

    # Fetch all stored jobs from MongoDB to display
    stored_jobs = JobListing.objects.all()
    
    # Calculate the average salary
    average_salary = calculate_average_salary(stored_jobs)

    return render(request, 'index.html', {
        'job_listings': stored_jobs,
        'query': query,
        'average_salary': f"₹{average_salary} per month"  
    })


def delete_job(request, job_id):
    job = JobListing.objects.get(id=job_id)
    job.delete()
    return redirect('index')
