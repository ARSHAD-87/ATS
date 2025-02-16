from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# View function to scrape and display jobs
def index(request):
    query = request.GET.get('q', 'python developer')  # Default search: Python Developer
    location = 'Lucknow%2C+Uttar+Pradesh'
    radius = 25

    payload = {
        'api_key': 'adb898ac2753c04974154370c83b6dd0',
        'url': f'https://in.indeed.com/jobs?q={query}&l={location}&radius={radius}&start=0',
        'device_type': 'desktop'
    }

    r = requests.get('https://api.scraperapi.com/', params=payload)

    job_listings = []  # Use a list to store job data
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for job_card in job_cards:
            title = job_card.find("h2", class_="jobTitle")
            company = job_card.find("span", class_="css-1h7lukg")
            location = job_card.find("div", class_="company_location")
            link = job_card.find("a", class_="jcs-JobTitle")

            job_entry = {
                'title': title.text.strip() if title else 'N/A',
                'company': company.text.strip() if company else 'N/A',
                'location': location.text.strip() if location else 'N/A',
                'link': "https://in.indeed.com" + link['href'] if link else 'N/A'
            }

            job_listings.append(job_entry)

    else:
        print(f"Request failed with status code: {r.status_code}")

    return render(request, 'index.html', {'job_listings': job_listings, 'query': query})
