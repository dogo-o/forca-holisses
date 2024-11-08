import pygame as pg
import random

# Cores do jogo
branco = (255, 255, 255)
preto = (0, 0, 0)

# Setup da tela do Jogo
window = pg.display.set_mode((1000, 800))

# Inicializando fonte
pg.font.init()
fonte = pg.font.SysFont("Courier New", 50)
fonte_rb = pg.font.SysFont("Courier New", 30)
fonte_dica = pg.font.SysFont("Segoe UI Symbol", 20)

# Dicas lógicas e possíveis palavras
dica = [
    'A ∧ ¬B ∧ ¬C', 'A ∧ B ∧ ¬C', 'A ∧ ¬B ∧ C', '¬A ∧ B ∧ ¬C',
    '¬A ∧ ¬B ∧ C', '(A ∧ B) → (¬C)', '(¬A ∨ B) ∧ (¬B ∨ C)',
    '(A ∧ ¬C) ∨ (B ∧ ¬A) ∨ (C ∧ ¬B)', '(A ∧ ¬C) ∨ (¬A ∧ B)',
    '(¬A ∧ C) ∨ (A ∧ ¬B)'
]
dica2 = {
    0: ['maca'], 1: ['laranja', 'pessego', 'tangerina', 'uva'],
    2: ['banana'], 3: ['manga'], 4: ['abacaxi', 'abacate', 'amora'],
    5: ['laranja', 'pessego', 'tangerina', 'uva'],
    6: ['banana', 'abacaxi', 'abacate', 'amora', 'manga'],
    7: ['maca', 'manga', 'abacaxi', 'abacate', 'amora'],
    8: ['maca', 'manga'], 9: ['maca', 'abacaxi']
}

# Conjuntos para exibir
conjuntos = {
    'A': ['banana', 'maca', 'laranja', 'pessego', 'tangerina', 'uva'],
    'B': ['laranja', 'pessego', 'tangerina', 'uva', 'manga'],
    'C': ['abacaxi', 'banana', 'abacate', 'amora']
}

palavras = []

def setarPalavras():
    palavras.clear()
    indice = random.randint(0, len(dica) - 1)
    dica_logica = dica[indice]
    palavras_possiveis = dica2[indice]
    for item in palavras_possiveis:
        palavras.append(item)
    return palavras, dica_logica

# Inicializa palavras e dica
palavras, dica_logica = setarPalavras()

# Variáveis do jogo
tentativas_de_letras = [' ', '-']
palavra_escolhida = ''
palavra_camuflada = ''
end_game = True
chance = 0
letra = ' '
click_last_status = False
jogo_encerrado = False

def Desenho_da_Forca(window, chance):
    pg.draw.rect(window, branco, (0, 0, 1000, 800))  # Move o fundo para baixo
    pg.draw.line(window, preto, (100, 600), (100, 300), 10)
    pg.draw.line(window, preto, (50, 600), (150, 600), 10)
    pg.draw.line(window, preto, (100, 300), (300, 300), 10)
    pg.draw.line(window, preto, (300, 300), (300, 350), 10)
    if chance >= 1:
        pg.draw.circle(window, preto, (300, 400), 50, 10)
    if chance >= 2:
        pg.draw.line(window, preto, (300, 450), (300, 550), 10)
    if chance >= 3:
        pg.draw.line(window, preto, (300, 460), (225, 550), 10)
    if chance >= 4:
        pg.draw.line(window, preto, (300, 460), (375, 550), 10)
    if chance >= 5:
        pg.draw.line(window, preto, (300, 550), (375, 650), 10)
    if chance >= 6:
        pg.draw.line(window, preto, (300, 550), (225, 650), 10)

def Desenho_Restart_Button(window):
    pg.draw.rect(window, preto, (700, 600, 200, 65))
    texto = fonte_rb.render('Restart', 1, branco)
    window.blit(texto, (740, 620))

def Exibir_Dica_e_Conjuntos(window, dica_logica, conjuntos):
    # Exibir dica lógica
    texto_dica = fonte_dica.render(f'Dica Lógica: {dica_logica}', 1, preto)
    window.blit(texto_dica, (50, 20))

    # Exibir conjuntos A, B e C
    y_pos = 60
    for conjunto, elementos in conjuntos.items():
        texto_conjunto = fonte_dica.render(f'{conjunto} = {elementos}', 1, preto)
        window.blit(texto_conjunto, (50, y_pos))
        y_pos += 30

def Sorteando_Palavra(palavras, palavra_escolhida, end_game):
    if end_game:
        palavra_n = random.randint(0, len(palavras) - 1)
        palavra_escolhida = palavras[palavra_n]
        end_game = False
    return palavra_escolhida, end_game

def Camuflando_Palavra(palavra_escolhida, tentativas_de_letras):
    palavra_camuflada = ""
    for letra in palavra_escolhida:
        if letra.upper() in tentativas_de_letras:
            palavra_camuflada += letra
        else:
            palavra_camuflada += "#"
    return palavra_camuflada

def Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, chance):
    if letra not in tentativas_de_letras:
        tentativas_de_letras.append(letra)
        if letra.upper() not in palavra_escolhida.upper():
            chance += 1
    return tentativas_de_letras, chance

def Palavra_do_Jogo(window, palavra_camuflada):
    palavra = fonte.render(palavra_camuflada, 1, preto)
    window.blit(palavra, (200, 700))  # Posição ajustada para a palavra camuflada

def Restart_do_Jogo(click_last_status, click, x, y):
    if not click_last_status and click[0]:
        if 700 <= x <= 900 and 600 <= y <= 665:
            return True
    return False

def Verificar_Vitoria_Derrota(palavra_camuflada, chance):
    if palavra_camuflada == palavra_escolhida:
        return "Você Venceu!"
    elif chance >= 6:
        return f'Você Perdeu!'
    return None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN and not jogo_encerrado:
            letra = str(pg.key.name(event.key)).upper()

    mouse = pg.mouse.get_pos()
    mouse_position_x = mouse[0]
    mouse_position_y = mouse[1]
    click = pg.mouse.get_pressed()

    Desenho_da_Forca(window, chance)
    Desenho_Restart_Button(window)
    Exibir_Dica_e_Conjuntos(window, dica_logica, conjuntos)
    
    palavra_escolhida, end_game = Sorteando_Palavra(palavras, palavra_escolhida, end_game)
    palavra_camuflada = Camuflando_Palavra(palavra_escolhida, tentativas_de_letras)
    tentativas_de_letras, chance = Tentando_uma_Letra(tentativas_de_letras, palavra_escolhida, letra, chance)
    Palavra_do_Jogo(window, palavra_camuflada)

    resultado = Verificar_Vitoria_Derrota(palavra_camuflada, chance)
    if resultado:
        mensagem = fonte_rb.render(resultado, 1, preto)
        window.blit(mensagem, (450, 720))  # Ajustado para a mensagem de vitória/derrota
        jogo_encerrado = True

    if Restart_do_Jogo(click_last_status, click, mouse_position_x, mouse_position_y):
        palavras, dica_logica = setarPalavras()
        tentativas_de_letras = [' ', '-']
        palavra_escolhida = ''
        palavra_camuflada = ''
        end_game = True
        chance = 0
        letra = ' '
        jogo_encerrado = False

    click_last_status = click[0]
    pg.display.flip()
