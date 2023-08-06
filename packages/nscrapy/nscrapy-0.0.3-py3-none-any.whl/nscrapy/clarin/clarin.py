import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time
import unicodedata
from math import ceil

def dict_extract(key, var):
    ''' saca value de la key recurrentemente'''
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in dict_extract(key, v):
                    yield unicodedata.normalize('NFKC',bs(result).text).strip()
            elif isinstance(v, list):
                for d in v:
                    for result in dict_extract(key, d):
                        yield unicodedata.normalize('NFKC',bs(result).text).strip()

class clarin():
    def __init__(self):
        self.url='https://www.clarin.com'
    
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
        self.get_comments()    


    def get_comments(self):
        url=self.url
        url0='https://login.clarin.com/comments.getStreamInfo'
        keys_0={'categoryID': ['Com_03'],
         'APIKey': ['2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW'],
         'sdk': ['js_latest'],
         'authMode': ['cookie'],
         'format': ['jsonp'],
         'callback': ['gigya.callback']}

        keys_0['streamID']=url[-14:-5]
        cm0=r.get(url0,params=keys_0)
        info = json.loads(cm0.text[15:-2])
        N=info['streamInfo']['threadCount']

        keys = {'categoryID': ['Com_03'],
         'includeSettings': ['true'],
         'threaded': ['true'],
         'includeStreamInfo': ['true'],
         'includeUserOptions': ['true'],
         'includeUserHighlighting': ['true'],
         'lang': ['es'],
         'ctag': ['comments_v2'],
         'APIKey': ['2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW'],
         'source': ['showCommentsUI'],
         'sdk': ['js_latest'],
         'authMode': ['cookie'],
         'format': ['jsonp'],
         'callback': ['gigya.callback']}

        keys['streamID']=url[-14:-5]
        coms=[]
        urlcm='https://login.clarin.com/comments.getComments'
        for x in range(ceil(N/10)):    
            req = json.loads(r.get(urlcm,params=keys).text[15:-2])

            #hay replies dentro de replies, busco recursivamente comentarios
            coms.extend(list(dict_extract('commentText', req)))

            #coms.extend([unicodedata.normalize('NFKC',bs(x['commentText']).text) for x in req['comments']])
            #for k in req['comments']:
            #    try: 
            #        coms.extend([unicodedata.normalize('NFKC',bs(rep['commentText']).text) for rep in k['replies']])
            #    except:
            #        pass

            req['comments'][-1]['timestamp']
            keys['start']='ts_'+str(req['comments'][-1]['timestamp'])
        self.coms=coms
      
    def hoy(self):            
        notas=r.get(self.url)
        sopa=bs(notas.content,features="lxml")
        urls=[x.find('a').get('href') for x in sopa.find_all('article')]
        boxs=list()

        for x in sopa.find_all('div', {'class':'on-demand'}):
            boxs.append(hoy.url+x.get('data-src'))

        reqs=list()
        # son 69 pero hasta el 8 tienen cosas
        for x in boxs[:9]:
            reqs.append(r.get(x))
            #para evitar ban pongo pausa
            time.sleep(0.2)

        box0=json.loads(reqs[0].content.decode().strip('()'))['data']
        sopa0=bs(box0)

        for x in sopa0.find_all('a'): 
            urls.append(x.get('href'))


        for n,x in enumerate(reqs[1:]):
            box=json.loads(x.content.decode().strip('()'))['data']
            sopa=bs(box)
            for y in sopa.find_all('article'):      
                urls.append(y.find('a').get('href'))                                        

        box7=json.loads(reqs[7].content.decode().strip('()'))['data']
        sopa7=bs(box7)
        try:
            for x in sopa7.find('div',{'class':'mas-vistas'}).find_all('div')[1].find_all('div',{'onclick' : True}):
                urls.append(x.get('onclick')[13:-11])  
        except:
            pass
        urls2=list()    
        for u in urls:
            if u[:4] == 'http':
                urls2.append(u)
            else:
                urls2.append('https://www.clarin.com'+u)
        self.urls=urls2   
        
        
def get(lista):
    arts=list()
    print('total notas: '+ str(len(lista)))
    for j,u in enumerate(lista):
        if u[:23] == 'https://www.clarin.com/':
            art=clarin()
            try:
                art.get(u)
                time.sleep(0.2)
                #print(j,u)
                #print('ok')
                arts.append(art)
            except:
                print(j,u)
                print('fail') 
        else:
            pass
    return(arts)    