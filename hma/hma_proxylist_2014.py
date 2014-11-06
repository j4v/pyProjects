#!/usr/bin/python3

import requests
import bs4

class proxy_entry():
    def __init__(self, 
            ip_address,
            port,
            country,
            proxy_type,
            anonymity_level):
        self.ip_address = ip_address
        self.port = port
        self.country = country
        self.proxy_type = proxy_type
        self.anonymity_level = anonymity_level

# base URI
hma_url = "http://proxylist.hidemyass.com/"

# request page and parse
r = requests.get(hma_url)
bs = bs4.BeautifulSoup(r.text, "lxml")

# number of pages
pagination_table = bs.find('section', {'class': 'hma-pagination'})
max_pages = pagination_table.find_all("li")[-2].text

# fill proxy_list with proxy_entry objects
proxy_list = []
for page_num in range(1,int(max_pages)):

    # request page and parse
    r = requests.get("%s/%d" % (hma_url, page_num))
    bs = bs4.BeautifulSoup(r.text, "lxml")

    # get table of proxies
    try:
        proxy_table = bs.find('table', {'id': 'listable', 'class': 'hma-table'}).find('tbody')
        proxy_table_rows = proxy_table.find_all('tr')
    except Exception:
        print(bs)

    # parse each row
    for row in proxy_table_rows:
        # parse each row element
        row_elements = row.find_all('td')
        '''
        for elem in row_elements:
            print("%s\n" % elem)
            print("%s\n" % elem.text)
            print("--------------------------------------\n")
        exit()
        '''
        # parse styles
        # will be used to define what span attributes contain printable values
        row_ip_style = row_elements[1].find('style')
        row_ip_style_dict = {}  # save style values
        for style in row_ip_style.text.strip().split('\n'):
            tag = style.split('{')[0][1:]
            value = style.split('{')[1][:-1]
            row_ip_style_dict[tag] = value
        # get all span/div/normal elements
        row_ip_elements = []
        for element in row_elements[1].span.children:
            row_ip_elements.append(element)
        row_ip_elements = row_ip_elements[1:]  # remove <style>
        # find printable ip bytes
        row_ip_string = ""
        for element in row_ip_elements:
            if isinstance(element, bs4.NavigableString):  # NavigableString
                row_ip_string += element.string
            elif str(element.name) == 'span':  # <span>
                if 'class' in element.attrs:
                    if element.attrs['class'][0] in row_ip_style_dict:
                        if 'inline' in row_ip_style_dict[element.attrs['class'][0]]:
                            row_ip_string += element.text
                    else:
                            row_ip_string += element.text
                    if 'inline' in element.attrs['class'][0]:
                            row_ip_string += element.text
                if 'style' in element.attrs:
                    if element.attrs['style'] in row_ip_style_dict:
                        if 'inline' in row_ip_style_dict[element.attrs['style']]:
                            row_ip_string += element.text
                    if 'inline' in element.attrs['style']:
                            row_ip_string += element.text
            elif element.name == 'div':  # <div>, not used for anything
                pass
            else:  # other
                print("Unhandled element type: %s" % element)
        proxy_list.append(proxy_entry(row_ip_string,
                                        row_elements[2].text.strip(),
                                        row_elements[3].text.strip(),
                                        row_elements[6].text.strip(),
                                        row_elements[7].text.strip()))

'''
# remove non-High entries
for entry in proxy_list:
    if "High" not in entry.anonymity_level:
        proxy_list.remove(entry)
'''

'''
# test all proxies
for entry in proxy_list:
    if entry.proxy_type == "HTTPS":
        proxies = {"https": "http://%s:%s" % (entry.ip_address, entry.port)}
        response = requests.get("https://google.com", proxies=proxies)
        print(response)
    if entry.proxy_type == "HTTP":
        pass
    if entry.proxy_type == "socks4/5":
        pass
'''
