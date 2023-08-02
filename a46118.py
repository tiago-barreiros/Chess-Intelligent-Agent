import socket, sys
import math
import random

interactive_flag = False

# Variável usada para definir o nivel de profundidade da pesquisa
depth_analysis_original = 3

# Variável usada para obrigar a que a primeira jogada seja sempre a mesma e manter a profundidade a 1
## de forma e evitar pesquisas desnecessárias (visto que vou começar sempre com a mesma jogada)
decisao = 1

# Variável usada para definir qual a Tática de Defesa a usar, tendo em conta o primeiro movimento do adversário
defesa = 0

# Variável usada para evitar que após entrar uma vez em determinado "if", não volte a entrar
aux = 0

# Declarar variavel globar 'ronda'
ronda = 0

# Converte coordenadas 2D para a posição 1D no tabuleiro
def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]

# Converte a posição 1D no tabuleiro para as suas coordenadas 2D
def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]

# Função criada para reconhecer todos os movimentos possíveis de cada peça.
## A função está completa, só que após todos os testes que fiz, apenas retorno um valor caso qualquer pela possa atacar
## o rei adversario.
### Esta alteração após longos testes foi única significativa, as outras apenas me levavam a perder.
def ameaca_ativa(board, piece, play):
    ataque = []
    defesa = []
    score = 0
    pos = board.find(piece)
    pos2 = pos1_to_pos2(pos)

    if piece == 'a' or piece == 'h' or piece == 'A' or piece == 'H':  # TORRES
        for i in range(1, 8): # NORTE
            if pos2[0] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SUL
            if pos2[0] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):   # ESTE
            if pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # OESTE
            if pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break
        # ciclo for a percorrer a lista ataque
        for p in ataque:
            if p == 'E' or p == 'e':
                score += 20
            #elif p == 'D' or p == 'd':
            #    score += 50
            #elif p == 'A' or p == 'a' or p == 'H' or p == 'h':
            #    score += 25
            #elif p == 'B' or p == 'b' or p == 'F' or p == 'f' or p == 'G' or p == 'g' or p == 'C' or p == 'c':
            #    score += 10

    elif piece == 'b' or piece == 'g' or piece == 'B' or piece == 'G':  # CAVALOS
        for i in range(1, 2):
            for j in range(1, 2):
                if i != j:
                    # Analisar jogadas possiveis
                    if pos2[0] + i < 8 and pos2[1] + j < 8: # NORDESTE
                        o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + j))]
                        if 'a' <= o <= 'p':
                            if play == 0:
                                break
                            else:
                                ataque.append(o)
                                break
                        if 'A' <= o <= 'P':
                            if play == 0:
                                ataque.append(o)
                                break
                            else:
                                break

                    if pos2[0] + i < 8 and pos2[1] - j >= 0: # NOROESTE
                        o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - j))]
                        if 'a' <= o <= 'p':
                            if play == 0:
                                break
                            else:
                                ataque.append(o)
                                break
                        if 'A' <= o <= 'P':
                            if play == 0:
                                ataque.append(o)
                                break
                            else:
                                break

                    if pos2[0] - i >= 0 and pos2[1] + j < 8: # SUDESTE
                        o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + j))]
                        if 'a' <= o <= 'p':
                            if play == 0:
                                break
                            else:
                                ataque.append(o)
                                break
                        if 'A' <= o <= 'P':
                            if play == 0:
                                ataque.append(o)
                                break
                            else:
                                break

                    if pos2[0] - i >= 0 and pos2[1] - j >= 0: # SUDOESTE
                        o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - j))]
                        if 'a' <= o <= 'p':
                            if play == 0:
                                break
                            else:
                                ataque.append(o)
                                break
                        if 'A' <= o <= 'P':
                            if play == 0:
                                ataque.append(o)
                                break
                            else:
                                break

        # ciclo for a percorrer a lista ataque
        for p in ataque:
            if p == 'E' or p == 'e':
                score += 20
            #elif p == 'D' or p == 'd':
            #    score += 70
            # cavalo comer uma torre vale mais do que a torre comer um cavalo, mas menos que a torre comer uma rainha
            # ou rei
            #elif p == 'A' or p == 'a' or p == 'H' or p == 'h':
            #    score += 40
            #elif p == 'B' or p == 'b' or p == 'F' or p == 'f' or p == 'G' or p == 'g' or p == 'C' or p == 'c':
            #    score += 10

    elif piece == 'f' or piece == 'F' or piece == 'C' or piece == 'c':  # BISPOS
        for i in range(1, 8):  # NORDESTE
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SULDESTE
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SUDOESTE
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # NOROESTE
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break


        # ciclo for a percorrer a lista ataque
        for p in ataque:
            if p == 'E' or p == 'e':
                score += 20
            #elif p == 'D' or p == 'd':
            #    score += 70
            # bispo comer uma torre vale mais do que a torre comer um bispo, mas menos que a torre comer uma rainha
            # ou rei
            #elif p == 'A' or p == 'a' or p == 'H' or p == 'h':
            #    score += 40
            #elif p == 'B' or p == 'b' or p == 'F' or p == 'f' or p == 'G' or p == 'g' or p == 'C' or p == 'c':
            #    score += 10

    elif piece == 'd' or piece == 'D': #Rainhas
        for i in range(1, 8):  # NORTE
            if pos2[0] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SUL
            if pos2[0] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # ESTE
            if pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # OESTE
            if pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # NORDESTE
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SULDESTE
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # SUDOESTE
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break

        for i in range(1, 8):  # NOROESTE
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break

            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]
            if 'a' <= o <= 'p':  # ascii
                if play == 0:
                    break
                else:
                    ataque.append(o)
                    break
            if 'A' <= o <= 'P':
                if play == 0:
                    ataque.append(o)
                    break
                else:
                    break
        # ciclo for a percorrer a lista ataque
        for p in ataque:
            if p == 'E' or p == 'e':
                score += 20
            #Comer uma rainha vale menos do que ser comido por uma torre, cavalo, bispo ou piao
            #elif p == 'D' or p == 'd':
            #    score += 50
            #elif p == 'A' or p == 'a' or p == 'H' or p == 'h':
            #    score += 40
            #elif p == 'B' or p == 'b' or p == 'F' or p == 'f' or p == 'G' or p == 'g' or p == 'C' or p == 'c':
            #    score += 10

    #Caso a peca seja um peao
    elif 'i' <= piece <= 'p' or 'I' <= piece <= 'P': #Peoes
        if play == 0:
            if pos2[0] + 1 <= 7: #NORTE
                if pos2[1] + 1 <= 7:
                    o = board[pos2_to_pos1((pos2[0] + 1, pos2[1] + 1))]
                    if 'A' <= o <= 'P':
                        ataque.append(o)
                if pos2[1] - 1 >= 0: #NOROESTE
                    o = board[pos2_to_pos1((pos2[0] + 1, pos2[1] - 1))]
                    if 'A' <= o <= 'P':
                        ataque.append(o)
        else:
            if pos2[0] - 1 >= 0: #SUL
                if pos2[1] + 1 <= 7:
                    o = board[pos2_to_pos1((pos2[0] - 1, pos2[1] + 1))]
                    if 'a' <= o <= 'p':
                        ataque.append(o)
                if pos2[1] - 1 >= 0: #SUDOESTE
                    o = board[pos2_to_pos1((pos2[0] - 1, pos2[1] - 1))]
                    if 'a' <= o <= 'p':
                        ataque.append(o)

        # ciclo for a percorrer a lista ataque
        for p in ataque:
            if p == 'E' or p == 'e':
                score += 20
            #Comer uma rainha vale menos do que ser comido por uma torre, cavalo, bispo ou piao
            #elif p == 'D' or p == 'd':
            #    score += 300
            #elif p == 'A' or p == 'a' or p == 'H' or p == 'h':
            #    score += 150
            #elif p == 'B' or p == 'b' or p == 'F' or p == 'f' or p == 'G' or p == 'g' or p == 'C' or p == 'c':
            #    score += 90

    return score

# Funcao que devolve o peso que cada peça branca tem em determinada posicao do tabuleiro
def avaliar_posicao_brancas(p, pos, play):

    pts_peoes_pos = [0, 0, 0, 0, 0, 0, 0, 0,
                     5, 10, 10, -20, -20, 10, 10, 5,
                     5, -5, -10, 0, 0, -10, -5, 5,
                     0, 0, 0, 20, 20, 0, 0, 0,
                     5, 5, 10, 25, 25, 10, 5, 5,
                     10, 10, 20, 30, 30, 20, 10, 10,
                     50, 50, 50, 50, 50, 50, 50, 50,
                     60, 60, 60, 60, 60, 60, 60, 60]

    # caso seja o jogador 0 (brancas)
    if play == 0:
        pts_torres_pos = [0, 5, 0, 5, 5, 0, 5, 0,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          5, 10, 10, 10, 10, 10, 10, 5,
                          0, 0, 0, 0, 0, 0, 0, 0]
    else:
        pts_torres_pos = [0, 0, 0, 10, 10, 0, 0, 0,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          -5, 0, 0, 0, 0, 0, 0, -5,
                          5, 10, 10, 10, 10, 10, 10, 5,
                          0, 0, 0, 0, 0, 0, 0, 0]


    pts_cavalos_pos = [-50, -40, -30, -30, -30, -30, -40, -50,
                       -40, -20, 0, 5, 5, 0, -20, -40,
                       -30, 5, 10, 15, 15, 10, 5, -30,
                       -30, 0, 15, 20, 20, 15, 0, -30,
                       -30, 5, 15, 20, 20, 15, 5, -30,
                       -30, 0, 10, 15, 15, 10, 0, -30,
                       -40, -20, 0, 0, 0, 0, -20, -40,
                       -50, -40, -30, -30, -30, -30, -40, -50]


    pts_bispos_pos = [-20, -10, -10, -10, -10, -10, -10, -20,
                      -10, 5, 0, 0, 0, 0, 5, -10,
                      -10, 10, 10, 10, 10, 10, 10, -10,
                      -10, 0, 10, 5, 10, 10, 0, -10,
                      -10, 5, 5, 10, 10, 5, 5, -10,
                      -10, 0, 5, 10, 10, 5, 0, -10,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -20, -10, -10, -10, -10, -10, -10, -20]

    pts_rainha_pos = [-20, -10, -10, -5, -5, -10, -10, -20,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -10, 5, 5, 5, 5, 5, 0, -10,
                      0, 0, 5, 5, 5, 5, 0, -5,
                      -5, 0, 5, 5, 5, 5, 0, -5,
                      -10, 0, 5, 5, 5, 5, 0, -10,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -20, -10, -10, -5, -5, -10, -10, -20]

    pts_rei_pos = [20, 30, 10, 0, 0, 10, 30, 20,
                   20, 20, 0, 0, 0, 0, 20, 20,
                   -10, -20, -20, -20, -20, -20, -20, -10,
                   -20, -30, -30, -40, -40, -30, -30, -20,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30]

    if p == 'a' or p == 'h':
        return pts_torres_pos[pos]
    elif p == 'b' or p == 'g':
        return pts_cavalos_pos[pos]
    elif p == 'c' or p == 'f':
        return pts_bispos_pos[pos]
    elif p == 'd':
        return pts_rainha_pos[pos]
    elif p == 'e':
        return pts_rei_pos[pos]
    elif p == 'i' or p == 'j' or p == 'k' or p == 'l' or p == 'm' or p == 'n' or p == 'o' or p == 'p':
        return pts_peoes_pos[pos]

# Funcao que devolve o peso que cada peça preta tem em determinada posicao do tabuleiro
def avaliar_posicao_pretas(p, pos):

    global ronda

    pts_peoes_pos = [0, 0, 0, 0, 0, 0, 0, 0,
                     50, 50, 50, 50, 50, 50, 50, 50,
                     10, 10, 20, 30, 30, 20, 10, 10,
                     5, 5, 10, 25, 25, 10, 5, 5,
                     0, 0, 0, 20, 20, 0, 0, 0,
                     5, -5, -10, 0, 0, -10, -5, 5,
                     5, 10, 10, -20, -20, 10, 10, 5,
                     0, 0, 0, 0, 0, 0, 0, 0]

    pts_torres_pos = [0, 0, 0, 0, 0, 0, 0, 0,
                      5, 10, 10, 10, 10, 10, 10, 5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      0, 0, 0, 5, 5, 0, 0, 0]

    pts_cavalos_pos = [-50, -40, -30, -30, -30, -30, -40, -50,
                       -40, -20, 0, 0, 0, 0, -20, -40,
                       -30, 0, 10, 15, 15, 10, 0, -30,
                       -30, 5, 15, 20, 20, 15, 5, -30,
                       -30, 0, 15, 20, 20, 15, 0, -30,
                       -30, 5, 10, 15, 15, 10, 5, -30,
                       -40, -20, 0, 5, 5, 0, -20, -40,
                       -50, -40, -30, -30, -30, -30, -40, -50]

    pts_bispos_pos = [-20, -10, -10, -10, -10, -10, -10, -20,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -10, 0, 5, 10, 10, 5, 0, -10,
                      -10, 5, 5, 10, 10, 5, 5, -10,
                      -10, 0, 10, 10, 10, 10, 0, -10,
                      -10, 10, 10, 10, 10, 10, 10, -10,
                      -10, 5, 0, 0, 0, 0, 5, -10,
                      -20, -10, -10, -10, -10, -10, -10, -20]

    pts_rainha_pos = [-20, -10, -10, -5, -5, -10, -10, -20,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -10, 0, 5, 5, 5, 5, 0, -10,
                      -5, 0, 5, 5, 5, 5, 0, -5,
                      0, 0, 5, 5, 5, 5, 0, -5,
                      -10, 5, 5, 5, 5, 5, 0, -10,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -20, -10, -10, -5, -5, -10, -10, -20]

    pts_rei_pos = [-30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -30, -40, -40, -50, -50, -40, -40, -30,
                   -20, -30, -30, -40, -40, -30, -30, -20,
                   -10, -20, -20, -20, -20, -20, -20, -10,
                   20, 20, 0, 0, 0, 0, 20, 20,
                   20, 30, 10, 0, 0, 10, 30, 20]

    if p == 'A' or p == 'H':
        return pts_torres_pos[pos]
    elif p == 'B' or p == 'G':
        return pts_cavalos_pos[pos]
    elif p == 'C' or p == 'F':
        return pts_bispos_pos[pos]
    elif p == 'D':
        return pts_rainha_pos[pos]
    elif p == 'E':
        return pts_rei_pos[pos]
    elif p == 'I' or p == 'J' or p == 'K' or p == 'L' or p == 'M' or p == 'N' or p == 'O' or p == 'P':
        return pts_peoes_pos[pos]


# Função Objetivo
def f_obj(board, play):
    # Dá peso às jogadas, define o quão longe a peça se vai mover
    weight_positions = 2e-1

    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdedghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'

    # Declaração da valoração de cada uma das peças
    if play == 0:
        pts = [10, 7, 6, 100, 9999, 6, 7, 10, 2, 2, 2, 2, 2, 2, 2, 2]
    else:
        pts = [20, 12, 12, 36, 9999, 12, 12, 20, 4, 4, 4, 4, 4, 4, 4, 4]

    score_w = 0
    score_w_positions = 0

    global aux

    # Abertura Ruy Lopez + abertura Ataque Fegatello
    ## As peças brancas (letras minusculas), fazem sempre as mesmas jogadas iniciais (mediante o adversário)
    # defesa a 1 = Defesa Siciliana + Defesa Caro-Kann
    # defesa a 2 = Defesa Nimzoíndia
    ## As peças pretas (letras maiusculas), fazem determinada jogada caso o adversário comece de acordo com algum if
    if ronda == 1 and board[28] == 'm' and play == 0:
        return 1000
    elif ronda == 1 and board[34] == 'K' and play == 1 and defesa == 1:
        return 1000
    elif ronda == 1 and board[45] == 'G' and play == 1 and defesa == 2:
        return 1000
    elif ronda == 2 and board[21] == 'g' and play == 0:
        return 1000
    elif ronda == 2 and board[43] == 'L' and play == 1 and defesa == 1:
        return 1000
    elif ronda == 2 and board[44] == 'M' and play == 1 and defesa == 2:
        return 1000
    elif ronda == 2 and board[35] == 'L' and play == 1 and defesa == 4:
        return 1000
    elif ronda == 3 and board[26] == 'f' and play == 0:
        return 1000
    elif ronda == 3 and board[27] == 'K' and play == 1 and defesa == 1:
        return 1000
    elif ronda == 3 and board[44] == 'M' and play == 1 and defesa == 2:
        return 1000
    elif ronda == 3 and board[28] == 'L' and play == 1 and defesa == 4:
        return 1000
    elif ronda >= 4 and board[25] == 'F' and play == 1 and defesa == 2 and aux == 1:
        aux += 1
        return 1000
    elif ronda >= 5 and board[18] == 'F' and play == 1 and defesa == 2 and aux == 3:
        aux += 1
        return 1000
    elif ronda == 4 and board[38] == 'g' and play == 0:
        return 1000
    elif ronda == 5 and board[35] == 'm' and play == 0:
        return 1000
    elif ronda == 6 and board[53] == 'g' and play == 0:
        return 1000

    # Heurística para as peças brancas
    ## vai percorrer todas as posições do tabuleiro
    for i in range(64):
        if board[i] in w:
            # vai somar o valor de cada peça
            score_w += pts[w.index(board[i])]
            # vai somar o valor da posição de cada peça
            score_w_positions += avaliar_posicao_brancas(board[i], i, play)
            # somar em score_w o valor da ameaca_ativa
            score_w += ameaca_ativa(board, board[i], 0)


    score_b = 0
    score_b_positions = 0

    # Heurística para as peças brancas
    for i in range(64):
        if board[i] in b:
            score_b += pts[b.index(board[i])]
            score_b_positions += avaliar_posicao_pretas(board[i], i)
            score_b += ameaca_ativa(board, board[i], 1)

    # Retornar o score para as peças brancas
    if play == 0:
        return score_w + score_w_positions * weight_positions - score_b - score_b_positions * weight_positions
    # Retornar o score para as peças pretas
    else:
        return score_b + score_b_positions * weight_positions - score_w - score_w_positions * weight_positions

# Função que retorna o nodo anterior
def find_node(tr, id):
    if len(tr) == 0:
        return None
    if tr[0] == id:
        return tr
    for t in tr[-1]:
        aux = find_node(t, id)
        if aux is not None:
            return aux
    return None

# Função que retorna as direções possíveis para cada peça
def get_positions_directions(state, piece, p2, directions):
    ret = []
    for d in directions:
        for r in range(1, d[1] + 1):
            if d[0] == 'N':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1]])
                break

            if d[0] == 'S':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1]])
                break
            if d[0] == 'W':
                if p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] - r])] == 'z':
                    ret.append([p2[0], p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] - r])
                break
            if d[0] == 'E':
                if p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] + r])] == 'z':
                    ret.append([p2[0], p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] + r])
                break
            if d[0] == 'NE':
                if p2[0] - r < 0 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] + r])] == 'z':
                    ret.append([p2[0] - r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] + r])
                break
            if d[0] == 'SW':
                if p2[0] + r > 7 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] - r])] == 'z':
                    ret.append([p2[0] + r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] - r])
                break
            if d[0] == 'NW':
                if p2[0] - r < 0 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] - r])] == 'z':
                    ret.append([p2[0] - r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] - r])
                break
            if d[0] == 'SE':
                if p2[0] + r > 7 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] + r])] == 'z':
                    ret.append([p2[0] + r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] + r])
                break
            if d[0] == 'PS':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue
                break
            if d[0] == 'PN':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue
                break
            if d[0] == 'PS2':
                if p2[0] + r <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] + 1])

                if p2[0] + r <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] - 1])
                continue
            if d[0] == 'PN2':
                if p2[0] - r >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] + 1])

                if p2[0] - r >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] - 1])
                continue
            if d[0] == 'H':
                if p2[0] - 2 >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] - 1])

                if p2[0] - 2 >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] + 1])

                if p2[0] - 1 >= 0 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] + 2])

                if p2[0] + 1 <= 7 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] + 2])

                if p2[0] + 2 <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] + 1])

                if p2[0] + 2 <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] - 1])

                if p2[0] + 1 <= 7 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] - 2])

                if p2[0] - 1 >= 0 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] - 2])
    return ret

# Função que verifica se o movimento é válido
def get_available_positions(state, p2, piece):
    ret = []
    if piece in ('a', 'h', 'A', 'H'):  # Tower
        aux = get_positions_directions(state, piece, p2, [['N', 7], ['S', 7], ['W', 7], ['E', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('c', 'f', 'C', 'F'):  # Bishop
        aux = get_positions_directions(state, piece, p2, [['NE', 7], ['SE', 7], ['NW', 7], ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('d', 'D'):  # Queen
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 7], ['S', 7], ['W', 7], ['E', 7], ['NE', 7], ['SE', 7], ['NW', 7],
                                        ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('e', 'E'):  # King
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 1], ['S', 1], ['W', 1], ['E', 1], ['NE', 1], ['SE', 1], ['NW', 1],
                                        ['SW', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('b', 'g', 'B', 'G'):  # Horse
        aux = get_positions_directions(state, piece, p2, [['H', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    # Pawn
    if ord('i') <= ord(piece) <= ord('p'):
        if p2[0] == 1:
            aux = get_positions_directions(state, piece, p2, [['PS', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PS', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PS2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if ord('I') <= ord(piece) <= ord('P'):
        if p2[0] == 6:
            aux = get_positions_directions(state, piece, p2, [['PN', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PN', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PN2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
    return ret

# Função que conta o númeor de nodos gerados
def count_nodes(tr):
    ret = 0
    if len(tr) > 0:
        for t in tr[-1]:
            ret += count_nodes(t)
        return (1 + ret)
    return ret

def find_all(s, ch):
    #print('Find_all(_%s_%c' % (s, ch))
    return [i for i, letter in enumerate(s) if letter == ch]

# Função que verifica se o movimento é válido e se um pião chegou ao fim do tabuleiro transforma-se
# em uma rainha
def sucessor_states(state, player):
    ret = []

    for x in range(ord('a') - player * 32, ord('p') - player * 32 + 1):

        p_all = find_all(state, chr(x))

        if len(p_all) == 0:
            continue

        for p in p_all:
            p2 = pos1_to_pos2(p)

            pos_available = get_available_positions(state, p2, chr(x))
            # print('%c - Tot %d' % (chr(x), len(pos_available)))

            for a in pos_available:
                state_aux = list('%s' % state)
                state_aux[p] = 'z'
                if ord('i') <= x <= ord('p') and a[0] == 7:
                    state_aux[pos2_to_pos1(a)] = 'd'
                elif ord('I') <= x <= ord('P') and a[0] == 0:
                    state_aux[pos2_to_pos1(a)] = 'D'
                else:
                    state_aux[pos2_to_pos1(a)] = chr(x)
                ret.append(''.join(state_aux))

    return ret

# Função que insere um novo nodo na árvore
def insert_state_tree(tr, nv, parent):
    nd = find_node(tr, parent[0])
    if nd is None:
        return None
    nd[-1].append(nv)
    return tr


# #####################################################################################################################
# PRINT Board

pieces = ''.join(chr(9812 + x) for x in range(12))
pieces = u' ' + pieces[:6][::-1] + pieces[6:]
allbox = ''.join(chr(9472 + x) for x in range(200))
box = [allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60)]
(vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box

h3 = hbar * 3

# useful constant unicode strings to draw the square borders

topline = ul + (h3 + nt) * 7 + h3 + ur
midline = wt + (h3 + plus) * 7 + h3 + et
botline = ll + (h3 + st) * 7 + h3 + lr

tpl = u' {0} ' + vbar


def inter(*args):
    """Return a unicode string with a line of the chessboard.

    args are 8 integers with the values
        0 : empty square
        1, 2, 3, 4, 5, 6: white pawn, knight, bishop, rook, queen, king
        -1, -2, -3, -4, -5, -6: same black pieces
    """
    assert len(args) == 8
    return vbar + u''.join((tpl.format(pieces[a]) for a in args))


print
pieces
print
' '.join(box)
print

start_position = (
        [
            (-4, -2, -3, -5, -6, -3, -2, -4),
            (-1,) * 8,
        ] +
        [(0,) * 8] * 4 +
        [
            (1,) * 8,
            (4, 2, 3, 5, 6, 3, 2, 4),
        ]
)


def _game(position):
    yield topline
    yield inter(*position[0])
    for row in position[1:]:
        yield midline
        yield inter(*row)
    yield botline


game = lambda squares: "\n".join(_game(squares))
game.__doc__ = "Retur the chessboard as a string for a given position."


# #####################################################################################################################


def get_description_piece(piece):
    if ord(piece) < 97:
        ret = 'Black '
        type = 1
    else:
        ret = 'White '
        type = 0
    if piece.lower() in ('a', 'h'):
        ret = ret + 'Tower'
    elif piece.lower() in ('b', 'g'):
        ret = ret + 'Horse'
    elif piece.lower() in ('c', 'f'):
        ret = ret + 'Bishop'
    elif piece.lower() == 'd':
        ret = ret + 'Queen'
    elif piece.lower() == 'e':
        ret = ret + 'King'
    else:
        ret = ret + 'Pawn'
    return ret, type


def description_move(prev, cur, idx, nick):
    # print('description_move(idx=%d)' % idx)
    # print('prev_%s_' % prev)
    # print('%s' % print_board(None, prev, idx, nick))
    # print('cur_%s_' % cur)
    # print('%s' % print_board(None, cur, idx, nick))
    ret = 'Move [%d - %s]: ' % (idx, nick)

    cur_blank = [i for i, ltr in enumerate(cur) if ltr == 'z']
    prev_not_blank = [i for i, ltr in enumerate(prev) if ltr != 'z']
    # print('Cur Blank')
    # print(cur_blank)
    # print('Prev not blank')
    # print(prev_not_blank)
    moved = list(set(cur_blank) & set(prev_not_blank))
    # print(moved)
    moved = moved[0]

    desc_piece, type_piece = get_description_piece(prev[moved])

    fr = pos1_to_pos2(moved)

    # to = pos1_to_pos2(cur.find(prev[moved]))

    to = None
    tos = find_all(cur, prev[moved])
    for t in tos:
        if prev[t] != cur[t]:
            to = pos1_to_pos2(t)
            break

    if to is None:  # pawn --> queen
        print('Handle exceptional case.............................')
        print('Cur_%s_' % cur)
        print('Prev_%s_' % prev)
        print('Char_%c_' % chr(ord('d') - type_piece * 32))
        tos = find_all(cur, chr(ord('d') - type_piece * 32))
        fr_aux = find_all(prev, chr(ord('d') - type_piece * 32))
        for t in tos:
            if t not in fr_aux:
                to = pos1_to_pos2(t)
                break

    ret = ret + desc_piece + ' (%d, %d) --> (%d, %d)' % (fr[0], fr[1], to[0], to[1])
    if prev[pos2_to_pos1(to)] != 'z':
        desc_piece, type_piece = get_description_piece(prev[pos2_to_pos1(to)])
        ret = ret + ' eaten ' + desc_piece
    # print('Out description_move()')
    return ret


def show_board(prev, cur, idx, nick):
    print('print_board(obj: %f)...' % idx)
    state_show = []
    for r in range(0, 8):
        row = []
        for c in range(0, 8):
            if cur[pos2_to_pos1([r, c])] == 'z':
                row.append(0)

            if cur[pos2_to_pos1([r, c])] == 'a':
                row.append(-4)
            if cur[pos2_to_pos1([r, c])] == 'b':
                row.append(-2)
            if cur[pos2_to_pos1([r, c])] == 'c':
                row.append(-3)
            if cur[pos2_to_pos1([r, c])] == 'd':
                row.append(-5)
            if cur[pos2_to_pos1([r, c])] == 'q':
                row.append(-5)
            if cur[pos2_to_pos1([r, c])] == 'e':
                row.append(-6)
            if cur[pos2_to_pos1([r, c])] == 'f':
                row.append(-3)
            if cur[pos2_to_pos1([r, c])] == 'g':
                row.append(-2)
            if cur[pos2_to_pos1([r, c])] == 'h':
                row.append(-4)
            if ord('i') <= ord(cur[pos2_to_pos1([r, c])]) <= ord('p'):
                row.append(-1)

            if cur[pos2_to_pos1([r, c])] == 'A':
                row.append(4)
            if cur[pos2_to_pos1([r, c])] == 'B':
                row.append(2)
            if cur[pos2_to_pos1([r, c])] == 'C':
                row.append(3)
            if cur[pos2_to_pos1([r, c])] == 'D':
                row.append(5)
            if cur[pos2_to_pos1([r, c])] == 'Q':
                row.append(5)
            if cur[pos2_to_pos1([r, c])] == 'E':
                row.append(6)
            if cur[pos2_to_pos1([r, c])] == 'F':
                row.append(3)
            if cur[pos2_to_pos1([r, c])] == 'G':
                row.append(2)
            if cur[pos2_to_pos1([r, c])] == 'H':
                row.append(4)
            if ord('I') <= ord(cur[pos2_to_pos1([r, c])]) <= ord('P'):
                row.append(1)
        state_show.append(tuple(row))

    ret = game(state_show) + '\n'

    if prev is None:
        return ret
    ret = ret + description_move(prev, cur, idx, nick)

    return ret


def expand_tree(tr, dep, n, play):
    if n == 0:
        return tr
    suc = sucessor_states(tr[0], play)
    for s in suc:
        tr = insert_state_tree(tr, expand_tree([s, random.random(), dep + 1, 0, f_obj(s, play), []], dep + 1, n - 1,
                                               1 - play), tr)
    return tr


def show_tree(tr, play, nick, depth):
    if len(tr) == 0:
        return
    print('DEPTH %d' % depth)
    print('%s' % show_board(None, tr[0], f_obj(tr[0], play), nick))
    for t in tr[-1]:
        show_tree(t, play, nick, depth + 1)


def get_father(tr, st):
    if len(tr) == 0:
        return None
    for sun in tr[-1]:
        if sun[1] == st[1]:
            return tr

    for sun in tr[-1]:
        aux = get_father(sun, st)
        if aux is not None:
            return aux

    return None


def get_next_move(tree, st):
    old = None
    while get_father(tree, st) is not None:
        old = st
        st = get_father(tree, st)
    return old


def minimax_alpha_beta(tr, d, play, max_player, alpha, beta):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], play)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        aux, val = minimax_alpha_beta(s, d - 1, play, not max_player, alpha, beta)
        if max_player:
            if val > ret:
                ret = val
                ret_nd = aux
            alpha = max(alpha, ret)
        else:
            if val < ret:
                ret = val
                ret_nd = aux
            beta = min(beta, ret)
        if beta <= alpha:
            break

    return ret_nd, ret


def decide_move(board, play, nick):

    global depth_analysis_original
    global ronda
    global decisao
    global defesa
    global aux

    # incrementar a cada jogada
    ronda += 1

    # Abertura Ruy Lopez + Abertura Ataque Fegatello
    ## O movimento inicial das peças brancas é sempre o mesmo
    ### existe a continuidade desse movimento caso o adversário responda mediante algum if
    # defesa a 1 = Defesa Siciliana + Defesa Caro-Kann
    # defesa a 2 = Defesa Nimzoíndia
    # se for a primeira jogada do jogo e for as brancas, coloco a profundidade a 1 porque a jogada inicial
    ## é sempre a mesma
    if ronda == 1 and play == 0:
        decisao = 1
    #se o jogador for as brancas e na sua primeira jogada (depois de mim) for colocar o pião na posição 28 do tabuleiro
    ##entao a profundidade continua a 1 e a tatica de defesa é a 1
    ##e assim sucessivamente
    elif ronda == 1 and board[28] == 'm' and play == 1:
        decisao = 1
        defesa = 1
    elif ronda == 1 and board[27] == 'l' and play == 1:
        decisao = 1
        defesa = 2
    elif ronda == 2 and board[36] == 'M' and play == 0:
        decisao = 1
    elif ronda == 2 and board[31] == 'g' and play == 1 and defesa == 1:
        decisao = 1
    elif ronda == 2 and board[27] == 'l' and play == 1 and defesa == 1:
        decisao = 1
        defesa = 4
    elif ronda == 2 and board[26] == 'k' and play == 1 and defesa == 2:
        decisao = 1
    elif ronda == 3 and board[42] == 'B' and play == 0:
        decisao = 1
    elif ronda == 3 and board[27] == 'l' and play == 1 and defesa == 1:
        decisao = 1
    elif ronda == 3 and play == 1 and defesa == 2:
        decisao = 1
    elif ronda == 3 and board[18] == 'b' and play == 1 and defesa == 4:
        decisao = 1
    elif ronda >= 4 and board[18] == 'k' and play == 1 and defesa == 2 and aux == 0:
        decisao = 1
        aux += 1
    elif ronda >= 5 and board[16] == 'i' and board[25] == 'F' and play == 1 and defesa == 2 and aux == 2:
        decisao = 1
        aux += 1
    elif ronda == 4 and board[45] == 'G' and play == 0:
        decisao = 1
    elif ronda == 5 and board[35] == 'L' and play == 0:
        decisao = 1
    elif ronda == 6 and board[35] == 'G' and play == 0:
        decisao = 1
    else:
        decisao = 0

    if decisao == 1:
        depth_analysis = 1
    else:
        depth_analysis = depth_analysis_original


    states = expand_tree([board, random.random(), 0, f_obj(board, play), []], 0, depth_analysis,
                         play)  # [board, hash, depth, g(), f_obj(), [SUNS]]

    # show_tree(states, play, nick, 0)
    print('Total nodes in the tree: %d' % count_nodes(states))

    choice, value = minimax_alpha_beta(states, depth_analysis, play, True, -math.inf, math.inf)

    # print('Choose f()=%f' % value)
    # print('State_%s_' % choice[0])

    next_move = get_next_move(states, choice)

    # print('Next_%s_' % next_move[0])
    # input('Trash')

    return next_move[0]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect((sys.argv[1], int(sys.argv[2])))  # connecting client to server

hello_msg = '%s_%s' % (sys.argv[4], sys.argv[3])
client.send(hello_msg.encode('ascii'))

nickname = sys.argv[3]

player = int(sys.argv[4])

while True:  # making valid connection
    while True:
        message = client.recv(1024).decode('ascii')
        if len(message) > 0:
            break

    if interactive_flag:
        row_from = int(input('Row from > '))
        col_from = int(input('Col from > '))
        row_to = int(input('Row to > '))
        col_to = int(input('Col to > '))

        p_from = pos2_to_pos1([row_from, col_from])
        p_to = pos2_to_pos1([row_to, col_to])

        if (0 <= p_from <= 63) and (0 <= p_to <= 63):
            message = list(message)
            aux = message[p_from]
            message[p_from] = 'z'
            message[p_to] = aux
            message = ''.join(message)
    else:
        message = decide_move(message, player, nickname)

    client.send(message.encode('ascii'))
