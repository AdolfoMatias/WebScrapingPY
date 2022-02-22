"""
Importanto as bibliotecas
Precisa instalar a biblioteca pandas, então use o código de pip abaixo sem o #: 
"""
import requests #Faz o request
from bs4 import BeautifulSoup #Faz a procura e seleciona arquivos da web
from urllib .error import HTTPError, URLError #Para tratar erros HTTP e de URL

#pip install pandas
import pandas as pd


try:
     """
     Pasando a página e o requests.get, também serve para fazer post
     Tratando erros com Try e Except em HTTP e URL
     """
     url =r'https://g1.globo.com' #passo uma página de teste 
     response = requests.get(url) #Faço o request
     print('--------------------------------- ↓↓ CONEXÃO ↓↓ ---------------------------------')
     print(f'Conexão estabelecidada com sucesso, status: {response.status_code} código.') #verifico se a conexão está ok em 200.
     print()
except HTTPError as erroH:
     print(erroH)
except URLError as erroU:
     print(erroU)


content = response.content
html = BeautifulSoup(content, 'html.parser')
materia =[]

"""
Adiciono toda a resposta em um conteudo que será utilizado pelo BeautifulSoup
Crio as Listas para terem as máterias adicionadas junto com títulos e sublinks
"""


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

          #Aqui irá criar um atributo que recebe o subtitulo se houver, caso negativorecebe um sem subtitulo*
          subtitulo = noticia.find('a', attrs ={'class':'bstn-relatedtext'})
          if subtitulo is not None:
               print(f'Subtitulo: {subtitulo.text}')
               
               materia.append([titulo.text, subtitulo.text, titulo['href']]) #adiciona uma lista contendo uma lista com o titulo, subtitulo e linkl
          else:
               materia.append([titulo.text, 'Sem Subtitulo', titulo['href']]) # Opção que substitui o subtitulo caso não tenha
             


def gerar_csv():
     """
     Função que gera um DataFrame com pandas e posteriormente gera um CSV, 
     é uma função que depende da função gerar_noticias()
     
     Com as máterias adicionadas nas listas, gero um DataFrame atráves de lista de listas
     Também é feito um tratamento de erros
     """
     try:
          conjunto = pd.DataFrame(materia, columns=['Titulo', 'Subtitulo', 'Links'])#crio o dataframe
          conjunto.to_csv('link_noticias.csv', index=False) #aqui finalmente gero o csv e o index é False, retira o 0,1,2,3...n
     except FileNotFoundError as e:
          print(e)
     except AttributeError as atre:
          print('Nada foi denifido')
          raise atre
     return conjunto #Retorna o datafreme caso queira ver dando print no metodo


if __name__ == '__main__':#testes no seu módulo main
     gera_noticias()
     print(gerar_csv())



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