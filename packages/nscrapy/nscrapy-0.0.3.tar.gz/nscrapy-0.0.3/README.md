# NSCRAPY: Scraper de principales portales de noticias argentinos.</h1>



Libreria para bajar notas de clarin , pagina12, cronica y cronista.

Instalacion:

```python
pip install nscrapy
``` 

Clases para scrapear una url de una nota.

```python
clarin()
p12()
cronica()
cronista()
``` 

Ejemplo de uso, scrapear el portal de clarin de hoy (para pagina 12 cambiar clarin por p12) con comentarios:

```python
from nscrapy import nscrap as ns
from nscrapy.clarin import get

notasclarin=ns.clarin()

#scrapeo el portal
notasclarin.hoy()

#las urls a las notas de hoy estan en .urls

notashoy=get(notasclarin.urls)

```
notashoy es una lista de objetos nota:

```python
nota.titulo : titulo de la nota
nota.comm : comentarios
nota.com : ' '.join(comentarios)
nota.volanta : volanta de la nota
nota.bajada : resumen o subtitulo
nota.cuerpo : cuerpo nota
nota.bolds : textos en negrita
nota.bold : ' '.join(bolds)
``` 