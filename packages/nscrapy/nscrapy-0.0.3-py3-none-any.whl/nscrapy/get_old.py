import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib
import numpy as np
import time
import json
from tqdm import tqdm


uri='https://www.clarin.com'


class clarin():
    def __init__(self):
        self.url='https://www.clarin.com'
    
    
    urlc='https://login.clarin.com/comments.getComments'
    urlcp='https://login.clarin.com/comments.getComments?categoryID=Com_03&streamID=H1Y2WMTS-&includeSettings=true&threaded=true&includeStreamInfo=true&includeUserOptions=true&includeUserHighlighting=true&lang=es&ctag=comments_v2&APIKey=2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW&source=showCommentsUI&sourceData=%7B%22categoryID%22%3A%22Com_03%22%2C%22streamID%22%3A%22H1Y2WMTS-%22%7D&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fwww.clarin.com%2Fpolitica%2Facuerdo-cambiemos-massismo-echar-vido-camara-diputados_0_H1Y2WMTS-.html&format=jsonp&callback=gigya.callback&context=R4169081209'
    urlp=urllib.parse.urlparse(urlcp)
    keys=urllib.parse.parse_qs(urlp.query)
 
    
    def get(self,url):

        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','body-nota').findAll('p')
        st=sopa.find('div','body-nota').findAll('strong')
        self.volanta=sopa.find('p','volanta').text
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div','bajada').find('h2').text
        texto=list()
        for p in ps:
            if p.text == "COMENTARIOS":
                break
            texto.append(p.text)
        bolds=list()    
        for b in st:
            bolds.append(b.text)            
        self.cuerpo=' '.join(texto)
        self.bold=' '.join(bolds)
        self.bolds=bolds
        self.date=sopa.find('span',{'class':'publishedDate'}).get_text(strip=True)
        keys=self.keys
        keys['pageURL'][0]=url
        keys['streamID'][0]=url[-14:-5]
        cm=r.get(self.urlc,params=keys)
        d = json.loads(cm.text[15:-2])
        self.comm=[x['commentText'] for x in d['comments']]
        self.com=' '.join(self.comm)



def get_notas(year,month):
    url='https://www.clarin.com/contents/sitemap_news_'+ year + '_' + month +'.xml'
    xml=r.get(url)
    sopa=bs(xml.content,features="lxml")
    urls=[x.get_text() for x in sopa.find_all('loc')]
    
    notas=[]
    fails=[]
    for i,x in enumerate(tqdm(urls)):
        nota=clarin()
        try:
            nota.get(x)
            notas.append(nota)
            time.sleep(0.1)
        except:
            fails.append(x)

    data=[]
    for l,k in enumerate(notas):
        pupi=list()
        try:
            pupi.append(k.date)
            pupi.append(k.volanta)   
            pupi.append(k.bajada)
            pupi.append(k.titulo)
            pupi.append(k.cuerpo)
            pupi.append(k.bold)    
            pupi.append(k.com)
            pupi.append(urls[l])
            data.append(pupi)
        except:
            pass
    df=pd.DataFrame(data,columns=['date','volanta','bajada','titulo','cuerpo','bold','com','url'])
    df['cat']=df.url.apply( lambda x: x.split('/')[3])
    df.to_csv( year + '_' + month+'.csv')
    print('fails: ',len(fails))


