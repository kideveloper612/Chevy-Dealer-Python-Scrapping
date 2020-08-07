import requests
import csv
import os
import time
from bs4 import BeautifulSoup


def write(lines, file_name):
    with open(file=file_name, encoding='utf-8', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def read():
    with open(file='temp.csv', encoding='utf-8', mode='r') as csv_file:
        rows = list(csv.reader(csv_file))
    return rows


def send_request(url):
    res = requests.get(url).text
    return BeautifulSoup(res, 'html5lib')


def main():
    soup = send_request(url=base_url)
    cards = soup.select('.title-one.copy-one.media-one.links-few.leafy')
    for card in cards:
        if card.find(attrs={'class': 'media'}):
            img = card.find(attrs={'class': 'media'}).img['data-src']
        else:
            img = ''
        name = card.find(attrs={'itemprop': 'givenName'}).text.strip() + ' ' + card.find(attrs={'itemprop': 'familyName'}).text.strip()
        title = card.find(attrs={'itemprop': 'jobTitle'}).text.strip()
        if card.find(attrs={'itemprop': 'description'}):
            desc = card.find(attrs={'itemprop': 'description'}).text.strip()
        else:
            desc = ''
        if card.find(attrs={'itemprop': 'telephone'}):
            phone = card.find(attrs={'itemprop': 'telephone'}).text.strip()
        else:
            phone = ''
        if card.find(attrs={'itemprop': 'email'}):
            email = card.find(attrs={'itemprop': 'email'})['href'].replace('mailto:', '')
        else:
            email = ''
        line = ['Chevy', name, title, desc, phone, email, img]
        print(line)
        write(lines=[line], file_name='Chevy_Dealer.csv')


if __name__ == '__main__':
    base_url = 'https://www.georgeweberchevy.com/MeetOurDepartments#close'
    main()
