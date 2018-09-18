import csv
import requests
from bs4 import BeautifulSoup
type_list = ["nut", "cam", "tricam", "hex", "bigbro", "ballnut"]

result_dict_list = []


def url_list(type_of_gear):
    url = 'https://weighmyrack.com/' + type_of_gear
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    anchors = soup.find_all('a', attrs={'class', 'fullsize-link'})
    links = []

    for item in anchors:
        link = item['href']
        if link.find("/nut/") == -1:
            link = "https://weighmyrack.com" + link
            links.append(link)

    return(links)

for item in type_list:
    urls = url_list(item)
    dict_item = {"type": item, "urls": urls}
    result_dict_list.append(dict_item)

print(result_dict_list[0])