import csv
import requests
from bs4 import BeautifulSoup

def single_piece_search(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('table')
    header = soup.find_all('h1')[0].text
    list_of_rows = []
    list_of_rows.append(["Name", header])
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            for item in cell:
                if str(type(item)) != "<class 'bs4.element.Tag'>":
                    text = item
                    
                    clean = ""
                    prev = ""
                    for character in text:
                        if character == " " and prev == " ":
                            prev = character
                        else:
                            clean = clean + prev
                            prev = character
                    list_of_cells.append(clean)

        
        list_of_rows.append(list_of_cells)
    return list_of_rows

single_piece_search('https://weighmyrack.com/BallNut/Trango-BallNutz-1')
