from urllib.request import urlopen 
from bs4 import BeautifulSoup as soup
import astropy.io.fits as fits
from astropy import time, coordinates as coord
import glob
import datetime





star = input("Enter star system : ")
planet = input("Enter planet in star system : ")
url = "http://var2.astro.cz/ETD/etd.php?STARNAME=" + star + "&PLANET=" + planet
#print(website)

try :

    urlclient = urlopen(url)
    page_html = urlclient.read()
    urlclient.close() 
    
    page_soup = soup(page_html, 'html.parser')
    data_table = page_soup.findAll('div',{'class' : 'center'})
    
    obs_data = data_table[3].findAll('tr')
    maxLen = len(obs_data)
    compiled_list = []
    #list does not start from 0 because of table headers
    for i in range(1,maxLen) : 
        my_list = []
        
        data_set = obs_data[i]
        td = data_set.findAll('td')
        idx = int(td[0].text)
        jd_time = td[1].text 
        #splitting jd time and error amount for each value, find idx of +/- and slice string , then convert to float
        plus_idx = jd_time.index('+')
        minus_idx = jd_time.index('-') + 1
        jd = float(jd_time[:plus_idx]) + 2400000
        error = jd_time[minus_idx:].strip()
        if (error == ''):
            error = 0
        error = float(error)
        dq = int(td[7].text)
        my_list = [idx,jd,error,dq]
        compiled_list.append(my_list)
    
    # find RA and DEC for exoplanet
    ra_dec_data = page_soup.findAll('div', {'class' : 'centerlike'})
    x = ra_dec_data[1].findAll('td')
    #x[7] will give RA
    # x[8] will give DEC
    
    ra_ = (x[7].text).split()
 
    dec_ = (x[8].text).split()
    
    
    ra_dec_dict = {
            'ra' : (ra_),
            'dec' :(dec_)  
            
            }
    auth_check = False
    # refine list for good values  i.e. dq = 1,2
    for lst in compiled_list:
        if (lst[3]> 2):
            compiled_list.remove(lst)
    
    
    # check if all authentic data is conserved
    for lst in compiled_list:
        if (lst[3]> 2):
            auth_check = True
    
    print("JD data below [serial number , BJD , Error, DQ] : ")
    print(compiled_list)
# convert JD to BJD (location of observatory not included in calculations )
    for lst in compiled_list: 
        JD_UTC = lst[1]
        NEW_JD = time.Time(JD_UTC , format='jd',scale='utc', location=observatory)
        RA= ra_dec_dict['ra']
        DEC = ra_dec_dict['dec']
        RA_ = RA[0] + 'h' + RA[1] + 'm' + RA[2] + 's'
        DEC_ = DEC[0] + 'd' + DEC[1] + 'm' + DEC[2] + 's'
        
        target = coord.SkyCoord(RA_, DEC_, frame='icrs')
        ltt_bary = NEW_JD.light_travel_time(target)
        time_barycentre = NEW_JD.tdb + ltt_bary
        real_bjd=time_barycentre.value
        lst[1] = real_bjd
        
    print("BJD data below [serial number , BJD , Error, DQ] : ")
    print(compiled_list)

    
except IndexError :
    print("Exoplanet does not exist in the database")




# output result to text file
