#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Importando Bibliotecas
#

# Bibliotecas Padrão
import os, sys, threading

# Bibliotecas Personalizadas
from campo import Campo
from getch import Getch
import constantes as c

#
# Instanciando Classes
#

# Classe Campo
campo = Campo()

# Classe Getch
getch = Getch()

#
# Variáveis Auxiliares (Listas)
#

# Armazena a direção do movimento da Snake
direc = []

# Armazena a pontuação do jogo
pontos = []

#
# Incializando Variáveis
#

# Primeiro movimento à direita
direc.insert(0, c.C_DIR)

# Zerando a pontuação
pontos.insert(0, 0)

#
# Preparando o início do jogo
#

# Limpa a tela
os.system("clear")

# Cria o campo
campo.cria()

# Imprime campo na tela
campo.imprime()

#
# Funções
#

# Função _valida
#
# 	Valida o movimento a partir da tecla pressionada
#
#	@param 		d1 		Direção 01
#	@param 		d2 		Direção 02
#	@param 				boolean (True, se movimento OK, False, caso contrário)
#
def _valida(d1, d2):

	if   d1 == c.C_CIMA  and d2 == c.C_BAIXO: return False
	elif d1 == c.C_BAIXO and d2 == c.C_CIMA : return False
	elif d1 == c.C_DIR   and d2 == c.C_ESQ  : return False
	elif d1 == c.C_ESQ   and d2 == c.C_DIR  : return False

	else: return True

# Função _snake (Thread)
#
# 	Thread para mover a snake pelo campo
#
#	@param 		num 	Número da Thread		
#	@param 		term 	Evento para sinalizar a interrupção da thread
#
def _snake(num, term):

	# Movimenta a Snake
	while not term.is_set():

		ret = campo.moveSnake(direc[0])

		# Atualiza a pontuação
		if ret == 1:
			pontos[0] += 10

		# Encerra o jogo
		elif ret == -1:
			_finaliza(term)
	
# Função _getch (Thread)
#
# 	Thread para ler os caracteres informados
#
#	@param 		num 	Número da Thread		
#	@param 		term 	Evento para sinalizar a interrupção da thread
#
def _getch(num, term):

	while not term.is_set():

		# Lê a tecla pressionada
		ch = getch()

		# Sem informação
		if ch == None:
			pass

		# Encerra o jogo
		elif (ch == c.C_Q) or (ch == c.C_q):
			_finaliza(term)

		# Valida direção informada
		elif _valida(ch, direc[0]):

			# Atualiza a direção do movimento
			direc[0] = ch

# Função _finaliza
#
# 	Procedimentos para encerrar o jogo
#
#	@param 		term 	Evento para sinalizar a interrupção das threads
#
def _finaliza(term):

	# Condição para encerrar as Threads
	term.set()

	# Captura a altura do campo
	x = campo.__get__('altura')

	# Imprime a pontuação do jogo
	print "%s\033[%d;1HLamentável! Você fez apenas %d pontos! ='(" % (c.ORIGINAL, (x + 2), pontos[0])

	# Move cursor para o final do campo
	print "\033[%d;1H" % (x + 3)

#
# Função MAIN
#
#	Inicia o jogo
#
if __name__ == "__main__":

	# Evento para interromper a execução das Threads
	t_term = threading.Event()

	# Definindo Thread para movimento da Snake
	t_snake = threading.Thread(target=_snake, args=(1, t_term)) 

	# Definindo Thread para leitura do teclado
	t_getch = threading.Thread(target=_getch, args=(2, t_term))

	# Inicia as Threads
	t_snake.start()
	t_getch.start()