from bs4 import BeautifulSoup
import requests
import csv
import time

def idiom_scraper(output_name, page_count=152, limit=140, timer=True):
    csv_file = open(output_name, 'w')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['PHRASE', 'MEANING'])

    if timer==True:
        time_start=time.perf_counter()

    for i in range(page_count):
        print(f'scraping page {i+1} of {page_count}...')
        source = requests.get(f'http://theidioms.com/list/page/{i+1}/').text
        soup = BeautifulSoup(source, 'lxml')

        content = soup.find('div', class_='new-list').dl

        id_phrase = []
        id_mean = []
        omit = []

        for n,idiom_meaning in enumerate(content.find_all('dd')):
            meaning = idiom_meaning.p.text[9::].split(', i.e.')[0]
            meaning = meaning.split(' example:')[0]
            try:
                meaning = meaning.split('meaning:')[1]
            except:
                pass
            else:
                meaning = meaning.split('meaning:')[1]
            meaning = meaning.replace('\n',' ').replace('\xa0',' ').replace('’','')
            meaning = meaning.lower()

            if len(meaning) > limit:
                omit.append(n)
                continue
            if idiom_meaning.p.text[-1]!='.':
                
                id_mean.append(meaning+'.')
            else:
                id_mean.append(meaning)

        for m,idiom in enumerate(content.find_all('dt')):
            if m in omit:
                continue
            id_phrase.append(idiom.text.strip('\ufeff').replace('’','\''))

        for j in range(len(id_phrase)):
            csv_writer.writerow([id_phrase[j], id_mean[j]])

    if timer==True:
        time_end = time.perf_counter()
        print(f'Total time: {time_end-time_start} seconds')

    csv_file.close()