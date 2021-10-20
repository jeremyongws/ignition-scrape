from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import csv


URL = "https://ignition.devpost.com/project-gallery"
N_PAGES = 21
OUTER_CLASS = "large-4 small-12 columns gallery-item"
INNER_CLASS = "software-entry-name entry-body"
LINK_CLASS = "block-wrapper-link fade link-to-software"
LIKE_CLASS = "count like-count"
OUTFILE_HEADERS= ['name', 'url', 'likes', 'description']

page_urls = []
for n in range(1,N_PAGES+1):
    page_urls.append(URL + f'?page={n}')

names = []
urls = []
likes = []
descriptions = []

print('scraping project data...')
for _url in tqdm(page_urls):
    page = requests.get(_url).content
    soup = BeautifulSoup(page, 'html.parser')
    entries = soup.find_all(class_=OUTER_CLASS)

    for entry in entries:
        data = entry.find(class_=LINK_CLASS)

        urls.append(data.get('href'))
        likes.append(int(data.footer.find(class_=LIKE_CLASS).get_text().strip(' \n')))
        names.append(data.find(class_=INNER_CLASS).h5.get_text().strip(' \n'))
        descriptions.append(data.find(class_=INNER_CLASS).p.get_text().strip(' \n'))

# -- debugging --
# print(names)
# print(urls)
# print(likes)
# print(descriptions)

project_data = set(zip(names, urls, likes, descriptions))
# print(project_data)

print('saving data to csv...')
with open('projects.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(OUTFILE_HEADERS)
    for row in tqdm(list(project_data)):
        csv_out.writerow(row)

print('done!')




