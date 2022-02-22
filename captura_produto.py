
"""Importando bibliotecas necessárias"""
import requests 
from re import sub
from bs4 import BeautifulSoup
from abc import ABC
from urllib.error import HTTPError, URLError
import pandas as pd

"""
O código abaixo atráves do instacniamento de Produto  e o metodo conexao_coup(), 
solicita que o usuarioinsira um produto para buscar na plataforma do Mercado Livre o produto, 
Deixando o nome do produto e o preço, outros métodos instanciados podem gerar um dataframe com pandas e um CSV.
"""
class Mercado(ABC):

    "Classe abstrata que recebe um atributo de instância pre definido em loja"
    def __init__(self, loja = "Mercado Livre"):
        self.__loja = loja
        self.produtos = [] #lista vazia para geração de csv na classe herdada
    
    """
    Getter e Setter de Loja para alguma necessidade
    """
    @property
    def loja(self):
        return self.__loja
    
    @loja.setter
    def loja(self,valor):
        self.__loja = valor
        self.__loja

#criando o input do produto
class Produto(Mercado):
    """
    Classe que herda de Mercado
    """
       
    def seleciona(self):
        """
        Metodo que  solicita ao usuário um produto desejado
        """
        sitepage = "https://lista.mercadolivre.com.br/"
        while True:
            produto = input("Digite o produto: ").lower() #solicita o nome do produto
            produto = sub("[^A-Za-z0-9 ]", "", produto) #remove simbolos e caracteres epsceiais
            try:
                if len(produto) >=1 or (produto):
                    produto =sitepage+produto #concatenção do produto desejado com o site
                    print(produto)
                    break
                else:
                    print("Você não digitou um valor compatível.")
                    continue
            except ValueError as e:
                print(e)
        return produto
    
    def requisicao(self):
        """
        Método que faz a conexão e tratamento de erros de HTTP e URL
        """
        url = self.seleciona() 
        try:
            requisito = requests.get(url)#implementa o get no endereço solicitado
            if (requisito):
                print(f"Conexão estabelecida código número {requisito.status_code}") #mostra o código da requisição
                conteudo = requisito.content #todo o conteudo do request
        except HTTPError as e:
            print(e)
        except URLError as e:
            print(e)
        return conteudo

    def conexao_soup(self):
        """
        Médoto que  implementa a requisicão e faz a procura por todos itens e os valores especificos atráves de um laço
        """
        site = BeautifulSoup(self.requisicao(), "html.parser")
        webpage = site.find_all("div", attrs={"class": "ui-search-result__wrapper"}) #procura todas as divs com a classe do produto solicitado
        for item in webpage:
            prod = item.find("div", attrs={"class": "ui-search-item__group ui-search-item__group--title"})#Procura o nome do produto
            preco = item.find("span", attrs={"class":"price-tag-amount"}) #preco do produto procurado

            if  (prod) or (preco): #verifica se o preço ou produto não são None
                elemento = f"Produto: {prod.text}" #nome do produto
                elemento_preco =f"Preço Total: {preco.text}" #preço do produto
                print(elemento)
                print(elemento_preco)
                self.produtos.append([prod.text, preco.text[2:]]) #adiciona a uma lista 

    def gerar_csv(self):

        """
        Método que gera um csv, primeiramente implementa um dataframe e posteriormente gera o o csv
        """
        dataset = pd.DataFrame(self.produtos, columns=["Produto", "Preço"]) #gera o dataframe com pandas
        print(dataset)
        dataset.to_csv('produtos_ml.csv', index=False, sep=",")#gera o csv


if __name__ == "__main__": #implementando os testes 
    produto1 = Produto()
    produto1.conexao_soup()
    produto1.gerar_csv()
