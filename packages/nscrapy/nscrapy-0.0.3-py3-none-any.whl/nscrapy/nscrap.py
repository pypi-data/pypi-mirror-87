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


def dic_p12(key, var):
    ''' saca value de la key recurrentemente comm p12'''
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield unicodedata.normalize('NFKC',bs(v).text).replace('\n',' ')
            if isinstance(v, dict):
                for result in dic_p12(key, v):
                    yield unicodedata.normalize('NFKC',bs(result).text).replace('\n',' ')
            elif isinstance(v, list):
                for d in v:
                    for result in dic_p12(key, d):
                        yield unicodedata.normalize('NFKC',bs(result).text).replace('\n',' ')

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
            boxs.append(self.url+x.get('data-src'))

        reqs=list()
        # son 69 pero hasta el 8 tienen cosas
        for x in boxs[:9]:
            reqs.append(r.get(x))
            #para evitar ban pongo pausa
            time.sleep(0.2)

        box0=json.loads(reqs[0].content.decode().strip('()'))['data']
        sopa0=bs(box0,features="lxml")

        for x in sopa0.find_all('a'): 
            urls.append(x.get('href'))


        for n,x in enumerate(reqs[1:]):
            box=json.loads(x.content.decode().strip('()'))['data']
            sopa=bs(box,features="lxml")
            for y in sopa.find_all('article'):      
                urls.append(y.find('a').get('href'))                                        

        box7=json.loads(reqs[7].content.decode().strip('()'))['data']
        sopa7=bs(box7,features="lxml")
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
        
class p12():
    
    def __init__(self):
        self.url='https://www.pagina12.com.ar'
  
    
    def get(self):
        url=self.url
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','article-inner padding-right').findAll('p')
        st=sopa.find('div','article-inner padding-right').findAll('b')
        self.volanta=sopa.find('h2','article-prefix').text
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div','article-summary').text
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
                coms.append(bs(x['content']['bodyHtml'],features="lxml").get_text().strip())
            except:
                pass    
        self.coms=coms

    def hoy(self):
        hoy=r.get('https://www.lanacion.com.ar')
        urls=[]
        h1s=bs(hoy.content,features="lxml").find_all('h1')
        urls.extend([h1.find('a').get('href') for h1 in h1s])
        h2s=bs(hoy.content,features="lxml").find_all('h2')
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
            urls2.extend([x.find('a').get('href') for x in bs(tema['Value'],features="lxml").find_all('h2')])
            try:
                urls2.extend([x.get('href') for x in bs(tema['Value'],features="lxml").find('ul').find_all('a')])
            except:
                pass
        urls.extend(urls2)
        urls.sort()
        self.urls=urls       
        
class cronica():
    def __init__(self,url):
        self.url=url
   
    def get(self):
        ucr=self.url
        nota=r.get(ucr)
        sopa=bs(nota.content,features="lxml")
        self.volanta=None
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div',{'class' : 'title'}).text
        bolds=[x.text for x in sopa.find('div', { 'class' :"entry-body text-font"}).findAll('strong')]           
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=sopa.find('div', { 'class' :"entry-body text-font"}).text        
        
        
class cronista():
    def __init__(self):
        self.url='https://www.cronista.com/'
   
    def get(self,url):
        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.volanta=None
        self.titulo=sopa.find('h1').get_text(strip=True)
        self.bajada=sopa.find('p',{'class':'bajada'}).get_text(strip=True)
        bolds=[ unicodedata.normalize("NFKD",x.get_text(strip=True)) for x in sopa.find('div',{'class':"article-container"}).find_all('strong')]         
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=''.join([unicodedata.normalize("NFKD",x.get_text().strip()) for x in sopa.find('div',{'class':"article-container"}).find_all('p') ]) 
        
    def hoy(self):
        url=self.url
        req=r.get(url)
        sopa=bs(req.content,features="lxml")
        titulos=sopa.find_all('h2',{'itemprop':"headline"})
        #urls=[url[:-1]+x.find('a').get('href') for x in titulos]
        urls=list()
        for x in titulos:
            if x.find('a').get('href')[:4] == 'http':
                urls.append(x.find('a').get('href'))
            else:
                urls.append(url[:-1]+x.find('a').get('href'))
            
        self.urls=urls
        
class dshow():

    def __init__(self):
        self.url='https://www.diarioshow.com/'

    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.volanta=None
        self.titulo=sopa.find('h1').text
        self.bajada=unicodedata.normalize("NFKD",sopa.find('div',{'class' : 'title'}).get_text(strip=True))
        bolds=[unicodedata.normalize("NFKD",x.get_text(strip=True)) for x in sopa.find('div', { 'class' :"entry-body text-font"}).findAll('strong')]           
        self.bold=' / '.join(bolds)
        self.bolds=bolds   
        bulk=sopa.find('div', { 'class' :"entry-body text-font"}).find_all('p')
        self.cuerpo=''.join([unicodedata.normalize("NFKD",x.get_text()) for x in bulk])
        self.quotes=' / '.join([x.split('”')[0] for x in self.cuerpo.split('“')[1:]])       
        

class ibae():
    def __init__(self):
        self.url='https://www.infobae.com/'
   
    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.titulo=sopa.find('h1').get_text(strip=True)
        self.bajada=sopa.find('h2').get_text(strip=True)
        mask=[ True  if x.find('mark',{'class':'hl_orange'}) else False for x in sopa.find('article').find_all('p')]
        ind=[i for i, x in enumerate(mask) if x == True][-1]
        self.cuerpo=' '.join([x.get_text() for x in sopa.find('article').find_all('p')[:ind]])
        self.bolds=[x.get_text(strip=True) for x in sopa.find('article').find_all('b')[:ind]][:-1]    
        self.bold=' / '.join(self.bolds)        
        self.quotes=' / '.join([x.split('”')[0] for x in self.cuerpo.split('“')[1:]])        

class ext():
    def __init__(self):
        self.url='https://exitoina.perfil.com/'
   
    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        body=sopa.find('div',{'id':'news-body'})
        self.cuerpo=' '.join([unicodedata.normalize("NFKD",x.get_text()).strip() for x in body.find_all('p')])
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('p','headline').text.strip()
        ps=body.find_all('p')
        bolds=[]
        for p in ps:
            bolds.extend([unicodedata.normalize("NFKD",x.get_text()).strip() for x in p.find_all('strong',recursive=False)])
        self.bolds=bolds
        self.quotes=[self.cuerpo.split('"')[1::2]]
        self.quot=' / '.join(self.cuerpo.split('"')[1::2])
        self.bold=' / '.join(bolds)
