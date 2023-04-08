from typing import Counter
import requests
import json
from bs4 import BeautifulSoup

f = open("stop_list.json")
stop_list = json.load(f)

word_count = Counter()

base_url = "https://www.seek.com.au/job/66661340?type=standard#sol=580ce4711b1f2e857bf9939f44bb2772bcdedd49"

r = requests.get(base_url)

soup = BeautifulSoup(r.text, "html.parser")

all_words = soup.get_text(" ", strip=True).lower().split()

for word in all_words:
    clean_word = word.strip(".,?!")

    if clean_word in stop_list:
        continue
    word_count[clean_word] += 1

print(word_count.most_common(50))





def main():

    tick = 1

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
