import csv
# import mechanize
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import shutil, os

# template = 'https://www.indeed.com/jobs?q={}&l={}'
def get_url(position, location):
    """
    Generate a URL from position and location
    """

    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    """
    Extract Job data from a single Job Post.
    Will extract information such as: title, url link, salary, location, and others.
    """
    atag = card.h2.a
    # title
    try:
        job_title = atag.get('title')
    except:
        job_title = ''
    # link
    try:
        job_link = 'https://www.indeed.com'+atag.get('href')
    except:
        job_link = ''
    # company
    try:
        job_company = card.find('span', 'company').text.strip()
    except:
        job_company = ''
    # location
    try:
        job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    except:
        job_location = ''
    # summary
    try:
        job_summary = card.find('div', 'summary').text.strip()
    except:
        job_summary = ''
    # post date
    try:
        post_date = card.find('span', 'date').text
    except:
        post_date = ''
    # today date
    try:
        today_date = datetime.today().strftime('%Y-%m-%d')
    except:
        today_date = ''
    # salary
    try:
        job_salary = card.find('span', 'salaryText').text.strip()
    except:
        job_salary = ''
    # remote job
    try:
        job_remote = card.find('span', 'remote').text.strip()
    except:
        job_remote = ''
    # rating
    try:
        job_rating = card.find('span', 'ratingsContent').text.strip()
    except:
        job_rating = ''

    result = (
        job_title,
        job_salary,
        job_company,
        job_location,
        job_remote,
        job_rating,
        job_summary, 
        post_date, 
        today_date, 
        job_link
        )
    return result

def extract(position, location):
    """
    position: job of interest
    location: place where you want to work

    Using the position and location of interest, the function will extract information and write it in a csv file.
    """
    url = get_url(position, location)
    print(url)
    records = []

    while True:
        # header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}

        response = requests.get(url)
        # response = mechanize.urlopen(url)
        # print(response.reason) # Expected to be OK
        # print(response.text)
        # print(response.content)
        soup = BeautifulSoup(response.text, "html.parser" )
        # soup = BeautifulSoup(response.read(), "html.parser" )
        # print(soup)
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')

        # print(len(cards))

        for card in cards:
            rec = get_record(card)
            records.append(rec)
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    print(len(records))
    with open("./outputs_3/job_postings_"+position+"_"+location+".csv", mode= 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_title','salary', 'company', 'location','is_remote', 'job_rating', 'job_summary', 'post_date', 'extract_date', 'job_url'])
        writer.writerows(records)

# cities = [
#     'Austin, TX',
#     'Dallas, TX',
#     'Raleigh, NC',
#     'San Jose, CA',
#     'Sunnyvale, CA',
#     'Santa Clara, CA',
#     'Charlotte, NC',
#     'Seattle, WA',
#     'San Francisco',
#     'Oakland, CA',
#     'Hayward, CA',
#     'Atlanta, GA',
#     'Huntsville, AL',
#     'Denver, CO',
#     'Washington, D.C.',
#     'Boulder, CO',
#     'Durham, NC',
#     'Columbus, OH',
#     'Colorado Springs, CO',
#     'Boston, MA',
#     'Baltimore, MD',
#     'Madison, WI',
#     'San Diego, CA',
#     'Trenton, NJ',
#     'Los Angeles, CA',
#     'Houston, TX',
#     'New York, NY']

def main(cities):
    """
    Main function that passes the list of cities of interest.
    """
    for i in cities:
        # print(i)
        # extract('data analyst', i)
        # extract('data scientist', i)
        # extract('machine learning engineer', i)
if __name__ == "__main__":
    cities = [
        'New York NY',
        'San Francisco CA',
        'Anchorage AK',
        'Oakland CA',
        'Boston MA',
        'Seattle WA',
        'Honolulu HI', 
        'Washington DC',
        'Miami FL',
        'Charleston SC',
        'Minneapolis MN',
        'Chicago IL',
        'Fort Lauderdale FL',
        'Portland OR',
        'Irvine CA',
        'Los Angeles CA',
        'Philadelphia PA',
        'Pittsburgh PA',
        'Cleveland OH',
        'Milwaukee WI',
        'Sacramento CA',
        'San Diego CA',
        'Asheville NC',
        'San Jose CA',
        'New Orleans LA',
        'Birmingham AL',
        'Tampa FL',
        'Atlanta GA',
        'Charlotte NC',
        'Baltimore MD',
        'Ann Arbor MI',
        'Rochester NY',
        'Denver CO',
        'Spokane WA',
        'Columbus OH',
        'Albany NY',
        'Colorado Springs CO',
        'Knoxville TN',
        'Orlando FL',
        'Nashville TN',
        'Buffalo NY',
        'Olympia WA',
        'Kansas City MO',
        'Jacksonville FL',
        'Raleigh NC',
        'Detroit MI',
        'Tucson AZ',
        'Eugene OR',
        'Reno NV',
        'Richmond VA',
        'Las Vegas NV',
        'Louisville KY',
        'Houston TX',
        'Toledo OH',
        'Des Moines IA',
        'San Antonio TX',
        'Phoenix AZ',
        'Tulsa OK',
        'Madison WI',
        'Salt Lake City UT',
        'Dallas TX',
        'Indianapolis IN',
        'Little Rock AR',
        'Austin TX',
        'Cincinnati OH',
        'Albuquerque NM',
        'Fresno CA',
        'Memphis TN',
        'Huntsville AL',
        'Wichita KS',
        'Boise ID',
        'El Paso TX'
        ]
    main(cities)