import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time
import unicodedata

class lnn():
    def __init__(self):
        self.url='https://www.lanacion.com.ar'
   
    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.titulo=sopa.find('h1').get_text(strip=True)
        self.bajada=sopa.find('epigrafe').get_text(strip=True)
        self.cuerpo=' '.join([unicodedata.normalize("NFKD",x.get_text()).strip() for x in sopa.find('section',{'id':'cuerpo'}).find_all('p')][:-1])
        bolds=sum([x.find_all('b') for x in sopa.find('section',{'id':'cuerpo'}).find_all('p', recursive=False)],[])
        self.bolds=[x.get_text(strip=True) for x in bolds]
        self.bold=' / '.join(self.bolds)     
        self.quotes=' / '.join([x.split('”')[0] for x in self.cuerpo.split('“')[1:]])
        #comentarios        
        token=base64.b64encode(bytes(sopa.find('div',{'id' : 'tokenLF'}).get('data-entrada'), 'utf-8')).decode('ascii')
        com=r.get('https://data.livefyre.com/bs3/v3.1/la-nacion.fyre.co/356483/'+token+'/init')
        data=com.json()
        np=data['collectionSettings']['archiveInfo']['nPages']
        comms=[]
        for n in range(0,np):
            com=r.get('https://data.livefyre.com/bs3/v3.1/la-nacion.fyre.co/356483/'+token+'/'+str(n)+'.json')
            comms.extend(com.json()['content'][:])
            time.sleep(0.2)
        coms=[]    
        for j,x in enumerate(comms):
            try:
                coms.append(bs(x['content']['bodyHtml']).get_text().strip())
            except:
                pass    
        self.coms=coms
      
    def hoy(self):
        hoy=r.get('https://www.lanacion.com.ar')
        urls=[]
        h1s=bs(hoy.content).find_all('h1')
        urls.extend([h1.find('a').get('href') for h1 in h1s])
        h2s=bs(hoy.content).find_all('h2')
        urls.extend([h2.find('a').get('href') for h2 in h2s])
        headers = {
        'authority': 'www.lanacion.com.ar',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.lanacion.com.ar/',
        'accept-language': 'es-419,es;q=0.9,en;q=0.8,gl;q=0.7',   
        }

        params = (
        ('utm_source', 'navigation'),
        ('datamodule', """anexo_2;tema_1;tema_2;tema_3;opinion;
         tema_4;tema_5;tema_6;mas-leidas;comercial_1;
         tema_7;tema_8;comercial_2;tema_9;tema_10;tema_11;
         tema_12;tema_13;tema_14;tema_15;tema_16;tema_17;tema_18
         """),
        )

        r1= r.get('https://www.lanacion.com.ar/', headers=headers, params=params)
        data=r1.json()['Modules']
        urls2=[]
        for tema in data:
            urls2.extend([x.find('a').get('href') for x in bs(tema['Value']).find_all('h2')])
            try:
                urls2.extend([x.get('href') for x in bs(tema['Value']).find('ul').find_all('a')])
            except:
                pass
        urls.extend(urls2)
        urls.sort()
        self.urls=urls
        
        
def get(lista):
    notas=[]
    for url in lista:
        nota=lnn()
        try:
            nota.get(nota.url+url)
            notas.append(nota)
            time.sleep(0.2)
        except:
            try:
                nota.get(url)
                notas.append(nota)
                time.sleep(0.2)
            except:
                print(url)
    return(notas)      