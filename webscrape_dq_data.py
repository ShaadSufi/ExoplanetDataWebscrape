from urllib.request import urlopen 
from bs4 import BeautifulSoup as soup
import os

site_name = 'http://var2.astro.cz'
star = input("Enter star system : ")
planet = input("Enter planet in star system : ")
try:
    #makes file path according to star/explanet name    
    dir_name = 'dq_data_'+ star + planet + '/'
    os.makedirs(os.path.dirname(dir_name), exist_ok=True)
    dq_url = 'http://var2.astro.cz/ETD/'
    url = "http://var2.astro.cz/ETD/etd.php?STARNAME=" + star + "&PLANET=" + planet
    urlclient = urlopen(url)
    page_html = urlclient.read()
    urlclient.close() 
        
    page_soup = soup(page_html, 'html.parser')
    data_table = page_soup.findAll('div',{'class' : 'center'})
    obs_data = data_table[3].findAll('tr')
    maxLen = len(obs_data)
    for i in range(1,maxLen):
        
    # find all data with dq<3
        data_set = obs_data[i]
        td = data_set.findAll('td')
        dq = int(td[7].text)
        idx = td[0].text
        if (dq<3 ):

            link_list  = obs_data[i].findAll('a')
            dq_p_url= link_list[0].get('href')
            dq_link = dq_url + dq_p_url
            #print(dq_link)
            dq_client = urlopen(dq_link)
            dq_html = dq_client.read()
            dq_client.close()
            dq_soup = str(soup(dq_html, 'html.parser')) 
            file_name = dir_name + star+ planet+'_'+ idx+ '.text'
            with open(file_name + ".txt",'w+') as f:
                f.write(dq_soup)
                f.close()
except IndexError : 
    print("Exoplanet does not exist in the database")