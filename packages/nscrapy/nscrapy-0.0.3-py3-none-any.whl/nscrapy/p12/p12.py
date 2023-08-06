import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time

class p12():
    
    def __init__(self):
        self.url='https://www.pagina12.com.ar'

    
    def get(self,url):
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','article-inner padding-right').findAll('p')
        st=sopa.find('div','article-inner padding-right').findAll('b')
        try:
            self.volanta=sopa.find('h2','article-prefix').text
        except:
            pass
        self.titulo=sopa.find('h1').text
        try:
            self.bajada=sopa.find('div','article-summary').text
        except:
            pass
        texto=list()
        for p in ps:
            texto.append(p.text)
        bolds=list()    
        for b in st:
            bolds.append(b.text)            
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=' '.join(texto)
        #comentarios
        with open('qp12', 'r') as file:
            qp12 = file.read()
        payload=json.loads(qp12)
        aid=url.split('/')[-1].split('-')[0]
        payload['variables']['assetId']=aid
        payload['variables']['assetUrl']=url
        payload.pop('operationName')
        pp=r.post("https://talk.pagina12.com.ar/api/v1/graph/ql", json=payload)
        coms=[]
        for x in pp.json()['data']['asset']['comments']['nodes']:
            coms.extend(list(dic_p12('body',x)))        
        self.coms=coms
        
    def hoy(self):            
        notas=r.get(self.url)
        sopa=bs(notas.content,features="lxml")
        urls=[x.find('a').get('href') for x in sopa.find_all('article')]
        self.urls=urls

        
def get(urls):
    notas=list()
    for url in urls:
        if url[:28]=='https://www.pagina12.com.ar/':
            nota=p12()
            try:
                nota.get(url)
                notas.append(nota)
                time.sleep(0.4)
            except:
                print(url)
        else:
            pass
    return(notas)
  