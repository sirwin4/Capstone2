import csv
import requests
from django.db import models
from backend.models import Piece
from bs4 import BeautifulSoup

def piece_scrape(result, item_type):
    url = result
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('table')
    header = soup.find_all('h1')[0].text
    list_of_rows = []
    list_of_rows.append(["Name", header])
    list_of_rows.append(["Type", item_type])
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            for item in cell:
                if str(type(item)) != "<class 'bs4.element.Tag'>":
                    text = item
                    filter_char = lambda char: char.isalnum() or char == '-' or char == '/' or char == " " or char == "."
                    x = list(filter(filter_char, text))
                    comp = ""
                    for letter in x:
                        comp = comp + letter
                    print(comp)
                    clean = ""
                    prev = ""
                    for character in comp:
                        
                        if character == " " and prev == " ":
                            prev = character
                        else:
                            clean = clean + prev
                            prev = character
                    clean = clean + prev
                    print(clean)
                    if clean != "":
                        list_of_cells.append(clean)

        
        list_of_rows.append(list_of_cells)
    final_dict = {'Offset': False}
    for item in list_of_rows:
        if item[0] == 'Name':
            final_dict['Name'] = item[1]
        if item[0] == 'Type':
            final_dict['Type'] = item[1]
        if item[0] == 'Offset':
            final_dict['Offset'] = True
        if 'Range' in item[0]:
            check = []
            for section in item:
                if "mm" in section and "in" in section and not "Cam" in section and not "\xa0" in section:
                    new = section.split("mm")
                    new_list = []
                    for new_thing in new:
                        asdf = new_thing.replace("/", " /")
                        asdf = new_thing.replace("-", " -")
                        asdf = asdf.split("/")
                        for given in asdf:
                            new_list.append(given)
                    
                    print("new_list", new_list)
                    for thing in new_list:
                        if not "in" in thing and "in)" not in thing:
                            check.append(thing)
                elif "mm" in section and "Cam" not in section and "\xa0" not in section and "in" not in section and "in)" not in section:
                    print("elif apended", section)
                    check.append(section)
            print("check", check)

            if len(check) > 0:
                final = ""
                prev = ""
                checked = []
                for gear in check:
                    print("gear", gear)
                    for letter in gear:
                        if letter is not "-" and letter is not "m"and letter is not "/":
                            if letter == " ":
                                if prev != ",":
                                    prev = ","
                                    final = final + ","
                            else:
                                final = final + letter
                                prev = letter
                    print("final", final)
                    range_list = final.split(",")
                    for stuff in range_list:
                        if stuff != "":
                            checked.append(stuff)
                low = ""
                high = 0
                for size in checked:
                    if low == "":
                        low = float(size)
                    elif float(size) < low:
                        low = float(size)
                    if float(size) > high:
                        high = float(size)
                    
                final_dict['min_size'] = low
                final_dict['max_size'] = high

        print(final_dict)
    return final_dict

def convert(result_dict):
    piece = Piece()
    piece.name = result_dict['Name']
    piece.min_size = result_dict['min_size']
    piece.max_size = result_dict['max_size']
    piece.gear_type = result_dict['Type']
    if result_dict['Type'] == "Cam":
        piece.SLCD = True
    piece.offset = result_dict["Offset"]

generic = piece_scrape('https://weighmyrack.com/Tricam/CAMP-Nylon-025', 'Tricam')

convert(generic)


