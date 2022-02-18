import requests
from bs4 import BeautifulSoup
from urllib .error import HTTPError, URLError
import pandas as pd

try:
     url =r'https://g1.globo.com'
     response = requests.get(url)
     print('--------------------------------- ↓↓ CONEXÃO ↓↓ ---------------------------------')
     print(f'Conexão estabelecidada com sucesso, status: {response.status_code} código.')
     print()
except HTTPError as erroH:
     print(erroH)
except URLError as erroU:
     print(erroU)


content = response.content
html = BeautifulSoup(content, 'html.parser')

#cirnado listas pra gerar csv
materia =[]
submateria =[]
linkm =[]

def gera_noticias():

     print('-------------------------------- ↓↓ PORTAL G! ↓↓ --------------------------------')
     print()
     comfind = html.findAll('div', attrs={'class': 'feed-post-body'})
     for noticia in comfind:
          titulo = noticia.find('a', attrs={'class': 'feed-post-link'})
          print(f'Título: {titulo.text}')
          print(f'Link: {titulo["href"]}')

          materia.append(titulo.text)
          linkm.append(titulo['href'])
          
          subtitulo = noticia.find('a', attrs ={'class':'bstn-relatedtext'})
          if subtitulo is not None:
               print(f'Subtitulo: {subtitulo.text}')
               submateria.append(subtitulo.text)
          else:
               submateria.append('Sem subtitulo')
             


def gerar_csv():
     #pip install pandas
     try:
          conjunto = pd.DataFrame({
               'Titulo':materia,
               'Subtitulo': submateria,
               'Link':linkm
          })

          conjunto.to_csv('link_noticias.csv')
     except FileNotFoundError as e:
          print(e)
     except AttributeError as atre:
          print('Nada foi denifido')
          raise atre


if __name__ == '__main__':
     gera_noticias()
     gerar_csv()


          




'''
REFINANDO:
Atráves de Selecionadores consigo fazer  seleção atraves de CSS
'''
# def selecionar():
#      post = html.select('.feed-post-body')
#      for noticia in post:
#           titulo = noticia.select_one('.feed-post-body-title')
#           print(f'Titulo: {titulo.text}')
#           subtitulo =noticia.select_one('.bstn-relatedtext')
#           try:
#                #if subtitulo is not None:
#                subtitulo =noticia.select_one('.bstn-relatedtext')
#                print(f'Subtitutlo: {subtitulo.text}')
#           except AttributeError as e:
#                pass

# selecionar()
          
 
