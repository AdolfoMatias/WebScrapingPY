"""Importanto as bibliotecas"""
import requests #Faz o request
from bs4 import BeautifulSoup #Faz a procura e seleciona arquivos da web

from urllib .error import HTTPError, URLError #Para tratar erros HTTP e de URL

"""Precisa instalar a biblioteca pandas, então use o código abaixo sem o #: """
#pip install pandas
import pandas as pd

"""
Pasando a página e o requests.get, também serve para fazer post
Tratando erros com Try e Except em HTTP e URL
"""
try:
     url =r'https://g1.globo.com' #passo uma página de teste 
     response = requests.get(url) #Faço o request
     print('--------------------------------- ↓↓ CONEXÃO ↓↓ ---------------------------------')
     print(f'Conexão estabelecidada com sucesso, status: {response.status_code} código.') #verifico se a conexão está ok em 200.
     print()
except HTTPError as erroH:
     print(erroH)
except URLError as erroU:
     print(erroU)

"""
Adiciono toda a resposta em um conteudo que será utilizado pelo BeautifulSoup
"""
content = response.content
html = BeautifulSoup(content, 'html.parser')

"""Crio as Listas para terem as máterias adicionadas junto com títulos e sublinks"""
materia =[]
submateria =[]
linkm =[]


def gera_noticias():
     """
     A função usa o método findAll percorrentdo todo o conteúdo da página e depois 
     procura atráves das classes, o material solicitado: título, subtítulo e link
     """

     print('-------------------------------- ↓↓ PORTAL G1 ↓↓ --------------------------------')
     print()
     comfind = html.findAll('div', attrs={'class': 'feed-post-body'})

     for noticia in comfind:
          titulo = noticia.find('a', attrs={'class': 'feed-post-link'})
          print(f'Título: {titulo.text}') #exibe o titulo da matéria
          print(f'Link: {titulo["href"]}') #exibe o link da página

          materia.append(titulo.text) #adiciona lista o titulo
          linkm.append(titulo['href']) #adiciona a lista o link
          
          #Aqui irá criar um atributo que recebe o subtitulo se houver, caso negativorecebe um sem subtitulo*
          subtitulo = noticia.find('a', attrs ={'class':'bstn-relatedtext'})
          if subtitulo is not None:
               print(f'Subtitulo: {subtitulo.text}')
               submateria.append(subtitulo.text)
          else:
               submateria.append('Sem subtítulo')
             

"""
Função que gera um DataFrame com pandas e posteriormente gera um CSV, 
é uma função que depende da função gerar_noticias()
"""
def gerar_csv():

     """Com as máterias adicionadas nas listas, gero um DataFrame atráves de um dicionário.
     Também é feito um tratamento de erros"""
     try:
          conjunto = pd.DataFrame({
               'Titulo':materia,
               'Subtitulo': submateria,
               'Link':linkm
          })

          conjunto.to_csv('link_noticias.csv') #aqui finalmente gero o csv
     except FileNotFoundError as e:
          print(e)
     except AttributeError as atre:
          print('Nada foi denifido')
          raise atre

#testes no seu módulo main
if __name__ == '__main__':
     gera_noticias()
     gerar_csv()



'''
REFINANDO:
Atráves de Selecionadores consigo fazer  seleção atraves de CSS, não faz parte do código, é trivial
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
          
 
