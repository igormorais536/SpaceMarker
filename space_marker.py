import os
import pygame
import random
import pickle
from tkinter import Tk, simpledialog

pygame.init()
tamanho = (1000, 500)
tela = pygame.display.set_mode(tamanho)
clock = pygame.time.Clock()
fundo = pygame.image.load("bg.jpg")
pontos = []
linhas = []
pygame.mixer.music.load("som.mp3")
pygame.mixer.music.play(-1)
pygame.display.set_caption("Space Marker")
space = pygame.image.load("space.png")
pygame.display.set_icon(space)

def obter_nome():
    root = Tk()
    root.withdraw()
    nome = simpledialog.askstring("Nome da Estrela", "Nome da Estrela:")
    root.destroy()
    return nome

def exibir_texto(texto, posicao, tamanho_fonte=12, cor=(255, 255, 255)):
    fonte = pygame.font.SysFont("Arial", tamanho_fonte)
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, posicao)

def calcular_distancia(x1, y1, x2, y2):
    distancia_x = abs(x2 - x1)
    distancia_y = abs(y2 - y1)
    return distancia_x + distancia_y

def salvar_marcacoes():
    with open('marcacoes.pkl', 'wb') as arquivo:
        pickle.dump(pontos, arquivo)
    print("Marcações salvas com sucesso!")

def carregar_marcacoes():
    global pontos, linhas
    try:
        with open('marcacoes.pkl', 'rb') as arquivo:
            pontos = pickle.load(arquivo)
        linhas = []
        if len(pontos) >= 2:
            for i in range(len(pontos) - 1):
                linha = (pontos[i][:2], pontos[i+1][:2])
                linhas.append(linha)
        print("Marcações carregadas com sucesso!")
    except FileNotFoundError:
        print("Nenhum arquivo de marcações encontrado!")

def excluir_marcacoes():
    global pontos, linhas
    pontos.clear()
    linhas.clear()
    print("Marcações excluídas!")

carregar_marcacoes()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salvar_marcacoes()
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                x, y = event.pos
                nome = obter_nome()  
                if nome == "":
                    nome = "Desconhecido ({}, {})".format(x, y)
                ponto = (x, y, nome)
                pontos.append(ponto)
                if len(pontos) >= 2:
                    linha = (pontos[-2][:2], pontos[-1][:2])
                    linhas.append(linha)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10:  
                salvar_marcacoes()
            elif event.key == pygame.K_F11:  
                carregar_marcacoes()
            elif event.key == pygame.K_F12:  
                excluir_marcacoes()
            elif event.key == pygame.K_ESCAPE:  
                salvar_marcacoes()

    tela.blit(fundo, (0, 0))

    for i, linha in enumerate(linhas):
        pygame.draw.line(tela, (255, 255, 255), linha[0], linha[1], 2)  
        (x1, y1), (x2, y2) = linha
        soma_distancias = calcular_distancia(x1, y1, x2, y2)
        texto_distancia = f"Distância: {soma_distancias}"
        exibir_texto(texto_distancia, ((x1 + x2) / 2, (y1 + y2) / 2 - 10 * i))  

    for ponto in pontos:
        x, y, nome = ponto
        pygame.draw.circle(tela, (255, 255, 255), (x, y), 5)  
        exibir_texto(nome, (x + 10, y))

    exibir_texto("Pressione F10 para salvar as marcações", (10, 10))
    exibir_texto("Pressione F11 para carregar as marcações", (10, 20))
    exibir_texto("Pressione F12 para excluir as marcações", (10, 30))

    pygame.display.update()
    clock.tick(60)
pygame.quit()