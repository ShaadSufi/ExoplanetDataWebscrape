

#READ ME : the file name follows following format (Exoplanet name_index of image listed on the table on ETD_ dq value)
from urllib.request import urlopen 
from bs4 import BeautifulSoup as soup
import os

site_name = 'http://var2.astro.cz'
star = input("Enter star system : ")
planet = input("Enter planet in star system : ")
try:
    #makes file path according to star/explanet name    
    dir_name = 'lc_images_'+ star + planet + '/'
    os.makedirs(os.path.dirname(dir_name), exist_ok=True)
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
            img_data_lst = obs_data[i].findAll('img')
            #if image exists
            if (len(img_data_lst)>=1):
                img_src = (img_data_lst[0]).get('src')
                img_url = site_name + img_src
                file_name = dir_name + star+planet+'_'+ idx +'_'+ str(dq) + '.jpeg'
                with open(file_name,'wb') as f:
                    f.write(urlopen(img_url).read())
                    f.close()
except IndexError : 
    print("Exoplanet does not exist in the database")
    

