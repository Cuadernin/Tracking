from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
import csv
from RecargaV2 import config
""" Title: TRACKING A PRODUCTOS DE CUALQUIER SITIO WEB
    By: Cuadernin

    Task: Recopilado de informacion de productos(nombre, precio,link y fecha de recopilado) correspondientes a una categoria de 
        cualquier sitio web. Recopila hasta n paginas de la categoria. 
    
    Parameters:
           Pagina ---> 'Sitio web'
           P ---- > Numero de paginas a realizar el tracking 
    Ejemplo: P=0 recopila la pagina dada
             P=1 recopila la pagina dada y la segunda pagina
             P=2 recopila la pagina dada,la segunda pagina y la tercera
    Returns: Archivo CSV llamado ProductosV2
"""
options=Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless")
options.add_argument('--disable-gpu')
driver=webdriver.Chrome(options=options)
liga=[]
def tracker(sitio):
    info=config()['Sitios'][sitio]
    url=info['url']
    driver.get(url)
    titulos=info['titulos']
    precio=info['precio']
    links=info['links']
    titulasos=driver.find_elements_by_css_selector(titulos)
    price=driver.find_elements_by_css_selector(precio)
    links=driver.find_elements_by_css_selector(links)
    return titulasos,price,links

def trackerP(sitio):
    info=config()['Sitios'][sitio]
    sig=info['siguiente']
    sig=driver.find_element_by_css_selector(sig)
    sig=sig.get_attribute("href")
    driver.get(sig)
    titulos=info['titulos']
    precio=info['precio']
    links=info['links']
    titulasos=driver.find_elements_by_css_selector(titulos)
    price=driver.find_elements_by_css_selector(precio)
    links=driver.find_elements_by_css_selector(links)
    return titulasos,price,links

###################################################### BLOQUE
pagina='cyberpuerta'
T=tracker(pagina)
P=2
######################################################
for i in range(P+1):
    if i==0:
        for p,t,l in zip(T[0],T[1],T[2]):
            titulo=p.get_attribute("textContent")
            precio=t.get_attribute("textContent")
            linkss=l.get_attribute("href")
            if titulo.startswith('\n') or titulo.startswith(' '):
                titulo=titulo[1:len(titulo)]
            else:
                pass  
            if titulo.endswith('\n') or titulo.endswith(' '):
                titulo=titulo[:len(titulo)-1]
            else:
                pass
                
            if precio.startswith('\n') or precio.startswith(' '):
                precio=precio[1:len(precio)]
            else:
                pass 
            if precio.endswith('\n') or precio.endswith(' '):
                precio=precio[:len(precio)-1]
            else:
                pass
            liga.append([titulo,precio,linkss,datetime.datetime.now()])
    else:
        T2=trackerP(pagina)
        for p,t,l in zip(T2[0],T2[1],T2[2]):
            titulo=p.get_attribute("textContent")
            precio=t.get_attribute("textContent")
            linkss=l.get_attribute("href")
            if titulo.startswith('\n') or titulo.startswith(' '):
                titulo=titulo[1:len(titulo)]
            else:
                pass  
            if titulo.endswith('\n') or titulo.endswith(' '):
                titulo=titulo[:len(titulo)-1]
            else:
                pass
                
            if precio.startswith('\n') or precio.startswith(' '):
                precio=precio[1:len(precio)]
            else:
                pass 
            if precio.endswith('\n') or precio.endswith(' '):
                precio=precio[:len(precio)-1]
            else:
                pass
            liga.append([titulo,precio,linkss,datetime.datetime.now()])
            
####### llenado CSV ###############
columns=['Productos','Precios','links','Fecha']
titu=pd.DataFrame(liga, columns=columns) 
titu.to_csv('ProductosV2.csv',index=False,header=False,mode='a')
driver.quit()
