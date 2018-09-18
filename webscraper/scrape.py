import csv
import requests
# from beautifulsoup4 import BeautifulSoup

url = 'https://weighmyrack.com/Cam/Metolius-Ultralight-TCU-0'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find('table', attrs={'class': 'technical-specs table'})

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

outfile = open("./cam.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)