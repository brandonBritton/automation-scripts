import requests
import re
from bs4 import BeautifulSoup
from collections import Counter


def check_jobs(link, keyword):
    job_details = []

    url = 'https://www.seek.com.au' + link
    response = requests.get(url)
    temp = BeautifulSoup(response.text, 'lxml')

    details = temp.find_all('p')
    for d in details:
        # print(d.text)
        clean_details = re.sub('[^A-Za-z0-9 ]+', '', d.text)
        keywords = clean_details.lower().split()
        job_details = job_details + keywords

    if job_details.count(keyword) > 0:
        print(url)

    # for word in job_details: print(word)


def main():
    job_listings = []
    job_links = []

    tick = 1
    keyword = input('Enter a keyword: ')

    while True:
        page_num = str(tick)

        url = 'https://www.seek.com.au/graduate-software-engineer-jobs/in-All-Sydney-NSW?page=' + page_num
        response = requests.get(url)
        temp = BeautifulSoup(response.text, 'lxml')

        listings = temp.find_all('article')

        for job in listings:
            link = job.find('a').get('href')
            job_links.append(link)

        if listings == []:
            print('No more listings found!' + '\n' +
                  'Number of listings:', len(job_links))
            break
        else:
            job_listings.append(listings)

        tick += 1

    for link in job_links:
        check_jobs(link, keyword)


if __name__ == '__main__':
    main()
