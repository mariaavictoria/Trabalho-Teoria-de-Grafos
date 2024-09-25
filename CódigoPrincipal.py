#Bibliotecas utilizadas na implementação do código
import math
import time
import random

class Grafo:
    def __init__(self, tipo):
        #Características do grafo
        self.n=0 #Número de vértices                                                                     
        self.m=0 #Número de arestas
        self.tipo=tipo #Tipo de representação do grafo
        self.arestas=[] #Lista de arestas do grafo  
        self.representacao=[] #Representação do grafo
        self.graus=[]  #Lista de graus dos vértices
        self.vertices=[] #Lista de vértices

        if self.tipo!='Matriz' and self.tipo!='Lista': #Erro para tipo de grafo inválido
            raise Exception('Tipo de grafo inválido!')
    
    def ImportarTxt(self, grafo_txt):
        #Função para ler um grafo de um arquivo texto
        with open(grafo_txt, 'r', encoding='utf-8') as arquivo:
            lista=[]
            for linha in arquivo:
                lista.append(linha.strip().split())
            self.n= int(lista[0][0])
            self.m= len(lista)-1
            self.arestas=lista[1:]
            self.graus=[0]*self.n
            for i in range(self.n):
                if self.tipo=='Matriz':     #Criando a representação do grafo de acordo com o tipo escolhido pelo usuário
                    self.representacao.append([False]*self.n)
                elif self.tipo=='Lista':    #Criando a representação do grafo de acordo com o tipo escolhido pelo usuário
                    self.representacao.append([])
            for aresta in self.arestas:
                self.graus[int(aresta[0])-1]+=1
                self.graus[int(aresta[1])-1]+=1
                if self.tipo=='Matriz':
                    self.representacao[int(aresta[0])-1][int(aresta[1])-1]=True
                    self.representacao[int(aresta[1])-1][int(aresta[0])-1]=True
                elif self.tipo=='Lista':
                    self.representacao[int(aresta[0])-1].append(int(aresta[1]))
                    self.representacao[int(aresta[1])-1].append(int(aresta[0]))
            if self.tipo=='Lista':
                for i in range(self.n):
                    self.representacao[i]=sorted(self.representacao[i])
     
        
    def BFS(self, raiz):
        #Função para realizar uma busca em largura no grafo
        pai=[None]*self.n
        nivel=[0]*self.n
        marcados=[False]*self.n
        fila=[raiz]
        marcados[raiz-1]=True
        while len(fila)!=0:
            v=fila.pop(0)
            if self.tipo=='Lista':      #Adaptação ao tipo escolhido pelo usuário
                for w in self.representacao[v-1]:
                    if not marcados[w-1]:
                        fila.append(w)
                        marcados[w-1]=True
                        pai[w-1]=v
                        nivel[w-1]=nivel[v-1]+1
            if self.tipo=='Matriz':     #Adaptação ao tipo escolhido pelo usuário
                for w in range(self.n):
                    if self.representacao[v-1][w]==True:
                        if not marcados[w]:
                            fila.append(w+1)
                            marcados[w]=True
                            pai[w]=v
                            nivel[w]=nivel[v-1]+1
        with open('InfoBFS.txt', 'w', encoding='utf-8') as infoBFS: #Criação de um arquivo com as informações da busca em largura
            infoBFS.write('Informações da Busca em Largura:\n')
            infoBFS.write('\n')
            for i in range(self.n):
                infoBFS.write(f'Vértice {i+1}: Pai: {pai[i]}, Nível: {nivel[i]}\n')

    def DFS(self,raiz):
        #Função para realizar uma busca em profundidade no grafo
        pai=[None]*self.n
        nivel=[0]*self.n
        marcados=[False]*self.n
        pilha=[raiz]
        while len(pilha)!=0:
            v=pilha.pop()
            if not marcados[v-1]:
                marcados[v-1]=True
                if self.tipo=='Lista':      #Adaptação ao tipo escolhido pelo usuário
                    for w in sorted(self.representacao[v-1], reverse=True):
                        pilha.append(w)
                        if not marcados[w-1]:
                            pai[w-1]=v
                            nivel[w-1]=nivel[v-1]+1
                elif self.tipo=='Matriz':       #Adaptação ao tipo escolhido pelo usuário
                    for w in range(self.n-1, -1, -1):
                        if self.representacao[v-1][w]==True:
                            pilha.append(w+1)
                            if not marcados[w]:
                                pai[w]=v
                                nivel[w]=nivel[v-1]+1
        with open('InfoDFS.txt', 'w', encoding='utf-8') as infoDFS: #Criação de um arquivo com as informações da busca em profundidade
            infoDFS.write('Informações da Busca em Profundidade:\n')
            infoDFS.write('\n')
            for i in range(self.n):
                infoDFS.write(f'Vértice {i+1}: Pai: {pai[i]}, Nível: {nivel[i]}\n')

    def BFS_Mais_Distante(self, raiz):
        #Função para realizar uma busca em largura no grafo e determinar o vértice mais distante da raiz
        #Função elaborada para auxiliar outras funções
        pai=[None]*self.n
        Mais_Distante=raiz
        nivel=[0]*self.n
        marcados=[False]*self.n
        fila=[raiz]
        marcados[raiz-1]=True
        while len(fila)!=0:
            v=fila.pop(0)
            if self.tipo=='Lista':
                for w in sorted(self.representacao[v-1]):
                    if not marcados[w-1]:
                        fila.append(w)
                        marcados[w-1]=True
                        pai[w-1]=v
                        nivel[w-1]=nivel[v-1]+1
                        if nivel[w-1]>nivel[Mais_Distante-1]:
                            Mais_Distante=w
            if self.tipo=='Matriz':
                for w in range(self.n):
                    if self.representacao[v-1][w]==True:
                        if not marcados[w]:
                            fila.append(w+1)
                            marcados[w]=True
                            pai[w]=v
                            nivel[w]=nivel[v-1]+1
                            if nivel[w]>nivel[Mais_Distante-1]:
                                Mais_Distante=w
        return pai, nivel, Mais_Distante
    
    def distancia(self, x, y):
        #Função para calcular a distância entre dois vértices
        pai, nivel, Mais_Distante= self.BFS_Mais_Distante(x)
        if nivel[y-1]==0:
            return 'Não existe caminho entre os vértices!' 
        else:
            return nivel[y-1]

    def diametro(self):
        #Função para calcular o diâmetro do grafo
        lista_auxiliar=[]
        for i in range(1, self.n+1):
            pai, nivel, Mais_Distante= self.BFS_Mais_Distante(i)
            lista_auxiliar.append(Mais_Distante)
        diametro= max(lista_auxiliar)
        return diametro    

    def ComponentesConexas(self):
        #Função para determinar as componentes conexas do grafo
        ComponentesConexas=[]
        Marcados=[]
        Num_Componentes=0
        pai, nivel, Mais_Distante= self.BFS_Mais_Distante(1)
        for i in range(self.n):
            if len(Marcados)==self.n:
                break
            elif pai[i]== None and i+1 not in Marcados:
                Num_Componentes+=1
                ComponentesConexas.append([i+1])
                Marcados.append(i+1)
                pai, nivel, Mais_Distante= self.BFS_Mais_Distante(i+1)
                for j in range(len(pai)):
                    if pai[j]!=None:
                        Marcados.append(j+1)
                        ComponentesConexas[Num_Componentes-1].append(j+1)
        resposta= f'Número de Componentes Conexas: {Num_Componentes} \n' 
        for z in range(Num_Componentes): 
            resposta+= f'Componente {z+1}: Tamanho: {len(sorted(ComponentesConexas, key=len, reverse=True)[z])}, Vértices: {sorted(ComponentesConexas, key=len, reverse=True)[z]}\n'
        return resposta
    
    def DiametroAprox(self):
        #Função para calcular um diâmetro aproximado do grafo
        vertice=random.randint(1, self.n)
        pai, nivel, Mais_Distante= self.BFS_Mais_Distante(vertice)      #Encontrando um vértice afastado do grafo
        pai, nivel, Mais_Distante= self.BFS_Mais_Distante(Mais_Distante)    #Aproximando o diâmetro a partir do vértice mais distante de um vértice afastado do grafo
        DiametroAprox= Mais_Distante
        return DiametroAprox

    def CriarTxt(self):
        #Função para criar um arquivo texto de saída com informações do grafo
        with open('Info.txt', 'w', encoding='utf-8') as info:
            if self.n%2==0:
                grau_med= (sorted(self.graus)[(self.n//2)-1]+sorted(self.graus)[(self.n//2)])/2
            else:
                grau_med= sorted(self.graus)[(math.ceil(self.n/2))-1]
            info.write('Informações do Grafo:\n')
            info.write('\n')
            info.write(f'Número de Vértices: {self.n}\n')
            info.write(f'Número de Arestas: {self.m}\n')
            info.write(f'Grau Mínimo: {min(self.graus)}\n')
            info.write(f'Grau Máximo: {max(self.graus)}\n')
            info.write(f'Grau Médio: {sum(self.graus)/self.n}\n')
            info.write(f'Grau Mediano: {grau_med}\n')
            info.write('\n')
            info.write('Informações das Componentes Conexas:\n')
            info.write(self.ComponentesConexas())	

