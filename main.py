import requests
import json

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent()
HEADERS = {'user-agent': f'{UA.random}'}
HOST = 'https://www.work.ua'
URL = 'https://www.work.ua/jobs-chernihiv/?days=122'
request = requests.Session()

job_content = []


def get_count_page():
    res = request.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'lxml')
    pagination = soup.find(
        'ul', class_='hidden-xs').find_all('li')[-2].get_text()
    return pagination


def get_link_pages(count_page):
    job_links = []
    for cp in range(count_page):
        if cp == 0:
            link = f'{URL}'
        else:
            link = f'{URL}&page={cp+1}'
        job_links.append(link)
    return job_links


def collect_data(job_links):
    for job_link in job_links:
        resource = request.get(url=job_link, headers=HEADERS)
        soup = BeautifulSoup(resource.text, 'lxml')
        link_positions = soup.find(
            'div', id="pjax-job-list").find_all('div', class_='job-link')
        for link_position in link_positions:
            title = link_position.find('h2', class_='').find('a').get('title')
            link_title = link_position.find(
                'h2', class_='').find('a').get('href')
            try:
                added = link_position.find('span', class_='small').get_text()

            except Exception:
                added = link_position.find(
                    'span', class_='label-hot').get_text()

            try:
                salary = link_position.find('div', class_=False)
                slr = salary.find('b').text

            except Exception:
                slr = 'Уточнюйте'

            job_content.append({
                'title': title.strip(),
                'link_title': f'{HOST}{link_title.strip()}',
                'salary': slr.strip(),
                'added': added,
            })

    with open('main.json', 'a', encoding='utf-8') as file:
        json.dump(job_content, file, indent=4, ensure_ascii=False)


def main():
    pagination = get_count_page()
    link_url = get_link_pages(int(pagination))
    collect_data(link_url)


if __name__ == '__main__':
    main()
