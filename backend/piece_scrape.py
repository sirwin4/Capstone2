import csv
import requests
from django.db import models
from backend.models import Piece
from bs4 import BeautifulSoup

type_list = ["Nut", "Cam", "Hex", "Ballnut", "Bigbro", "Tricam"]

result_dict_list = []


def url_list(type_of_gear):
    x = [0, 66, 112, 485]
    y = [0, 16, 27, 35, 51]
    base_urls = []
    links = []
    if type_of_gear == "Cam":
        for num in x:
            urlss = 'https://weighmyrack.com/' + type_of_gear +"?f[]=field_weight:%5B" + str(num) + "%20TO%20990%5D"
            base_urls.append(urlss)
        
    if type_of_gear == "Nut":
        for num in y:
            urlss = 'https://weighmyrack.com/' + type_of_gear +"?f[]=field_weight:%5B" + str(num) + "%20TO%20990%5D"
            base_urls.append(urlss)
    if len(base_urls) !=0:
        for url in base_urls:
            response = requests.get(url)
            html = response.content
            soup = BeautifulSoup(html)
            anchors = soup.find_all('a', attrs={'class', 'fullsize-link'})

            for item in anchors:
                link = item['href']
                if link.find("/nut/") == -1:
                    link = "https://weighmyrack.com" + link
                    links.append(link)
    else:
        url = 'https://weighmyrack.com/' + type_of_gear
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html)
        anchors = soup.find_all('a', attrs={'class', 'fullsize-link'})

        for item in anchors:
            link = item['href']
            if link.find("/nut/") == -1:
                link = "https://weighmyrack.com" + link
                links.append(link)
    return(links)

for item in type_list:
    urls = url_list(item)
    dict_item = {"item_type": item, "urls": urls}
    result_dict_list.append(dict_item)



def piece_scrape(result, item_type):
    url = result
    final_dict = {'Offset': False, "url": url}
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('table')
    header = soup.find_all('h1')[0].text
    list_of_rows = []
    list_of_rows.append(['Name', header])
    list_of_rows.append(['Type', item_type])
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
                    clean = ""
                    prev = ""
                    for character in comp:
                        
                        if character == " " and prev == " ":
                            prev = character
                        else:
                            clean = clean + prev
                            prev = character
                    clean = clean + prev
                    if clean != "":
                        list_of_cells.append(clean)

        
        list_of_rows.append(list_of_cells)
    for item in list_of_rows:
        if item[0] == 'Name':
            final_dict['Name'] = item[1]
        if item[0] == 'Type':
            final_dict['Type'] = item[1]
        if item[0] == 'Offset':
            if "Yes" in item[1]:
                final_dict['Offset'] = True
        if 'Range' in item[0]:
            check = []
            worst_case= []
            for section in item:
                if section == " ":
                    final_dict['min_size'] = "micro"
                    final_dict['max_size'] = "micro"
                elif "mm" in section and "in" in section and not "Cam" in section and not "\xa0" in section:
                    new = section.split("mm")
                    new_list = []
                    for new_thing in new:
                        asdf = new_thing.replace("/", " /")
                        asdf = new_thing.replace("-", " -")
                        asdf = asdf.split("/")
                        for given in asdf:
                            new_list.append(given)
                    for thing in new_list:
                        if not "in" in thing and "in)" not in thing:
                            check.append(thing)
                elif "mm" in section and "Cam" not in section and "\xa0" not in section and "in" not in section and "in)" not in section:
                    check.append(section)
                elif "mm" not in section and "in" in section and not "Cam" in section and not "\xa0" in section:
                    worst_case.append(section)
            converted = []
            if len(worst_case) > 0 and len(check) == 0:
                newer = section.split("in")
                newer_list = []
                for newer_thing in newer:
                    asdf = newer_thing.replace("/", " /")
                    asdf = newer_thing.replace("-", " -")
                    asdf = asdf.split("/")
                    for given in asdf:
                        newer_list.append(given)
                ult = ""
                pen = ""
                for x in newer_list:
                    for char in x:
                        if char is not "-" and char is not "m"and char is not "/":
                            if char == " ":
                                if pen != ",":
                                    pen = ","
                                    ult = ult + ","
                            else:
                                ult = ult + char
                                pen = char
                    conv_list = ult.split(",")
                    for conv in conv_list:
                        if conv != "":
                            fixed = float(conv) / 0.039370
                            converted.append(fixed)

            if len(check) > 0 or len(converted) > 0:
                final = ""
                prev = ""
                checked = []
                if len(check) > 0:
                    for gear in check:
                        for letter in gear:
                            if letter is not "-" and letter is not "m"and letter is not "/":
                                if letter == " ":
                                    if prev != ",":
                                        prev = ","
                                        final = final + ","
                                else:
                                    final = final + letter
                                    prev = letter
                        range_list = final.split(",")
                        for stuff in range_list:
                            if stuff != "":
                                checked.append(stuff)
                if len(checked) == 0:
                    for checkout in converted:
                        checked.append(checkout)
                low = ""
                high = ""
                for size in checked:
                    
                    try:
                        float(size)
                        if high == "":
                            high = size
                        if size > high:
                            high = size
                    except:
                        pass
                for size in checked:
                    try:
                        float(size)
                        if low == "":
                            low = size
                        elif size < low:
                            low = size
                    except:
                        pass
                if low == "":
                    final_dict = "buggy piece"
                else:
                    final_dict['min_size'] = low
                    final_dict['max_size'] = high
    if final_dict != "buggy piece":
        if final_dict['min_size'] == "micro" or final_dict['max_size'] == "micro":
            if final_dict['min_size'] == "micro" and final_dict['max_size'] == "micro" and "Offset Micro" in final_dict['Name']:
                if "1" in final_dict['Name']:
                    final_dict['min_size'] = 3.0
                    final_dict['max_size'] = 5.3
                if "2" in final_dict['Name']:
                    final_dict['min_size'] = 3.4
                    final_dict['max_size'] = 6.5
                if "3" in final_dict['Name']:
                    final_dict['min_size'] = 4.6
                    final_dict['max_size'] = 7.8
                if "4" in final_dict['Name']:
                    final_dict['min_size'] = 5.9
                    final_dict['max_size'] = 9.5
                if "5" in final_dict['Name']:
                    final_dict['min_size'] = 8.0
                    final_dict['max_size'] = 10.5
                if "6" in final_dict['Name']:
                    final_dict['min_size'] = 9.0
                    final_dict['max_size'] = 12.5
            else: 
                final_dict = "buggy piece"
    if final_dict != "buggy piece":
        name_mod = final_dict["url"].split("/")
        name_add = ""
        ok = []
        for item in name_mod:
            k = item.split("-")
            for item in k:
                ok.append(k)
        for stringer in k:
            if stringer != "weighmyrack.com" and stringer != "https:" and stringer != "" and stringer != " " and stringer != final_dict['Type']:
                v = stringer.split("-")
                for string in v:
                    x = final_dict['Name'].split(" ")
                    if string not in x:
                        name_add = name_add + string + " "
        if name_add != "":
            final_dict['Name'] = name_add + " " + final_dict['Name']

    return final_dict

def convert(result_dict):
    if result_dict == "buggy piece":
        return
    else:
        exp_keys = ['Name', 'min_size', 'max_size', 'Type']
        cont = True
        for item in exp_keys:
            if item not in result_dict.keys():
                cont = False
        if cont == True:
            piece = Piece()
            piece.name = result_dict['Name']
            piece.min_size = result_dict['min_size']
            piece.max_size = result_dict['max_size']
            piece.gear_type = result_dict['Type']
            if result_dict['Type'] == "Cam":
                piece.SLCD = True
            piece.offset = result_dict['Offset']
            piece.save()
        else:
            return

for item in result_dict_list:
    #dict_item = {"item_type": item, "urls": urls}
    item_type = item['item_type']
    urls = item['urls']
    for url in urls:
        generic = piece_scrape(url, item_type)
        convert(generic)


