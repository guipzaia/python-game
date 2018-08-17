#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bibliotecas Padrão
import time

# Bibliotecas Personalizadas
import printer
import constantes as c

# Classe Snake (extendes Printer)
class Snake(printer.Printer):

	# Construtor da classe
	def __init__(self):

		# Atributos da classe
		self.data = {
			'corpo' : [],    # Corpo da Snake
			'tam'   : 5,     # Tamanho inicial da Snake (metade: 5)
			'veloc' : 0.2,   # Velocidade da Snake
		}

		# Espaçamento das colunas
		self.data['tam'] *= 2

	# Método GET (mágico)
	#
	#	Retorna o valor de um atributo específico da classe
	#
	#	@param		 attr 		Nome do atributo
	#	@return      			Valor do atributo
	#
	def __get__(self, attr):
		return self.data[attr]

	# Método SET (mágico)
	#
	#	"Seta" um valor específico a um determinado atributo da classe
	#	
	#	@param		attr 		Nome do atributo
	# 	@return  	val 		Valor do atributo
	#
	def __set__(self, attr, val):
		self.data[attr] = val

	# Método cria
	#
	#	Cria a Snake
	#
	#	@param 		altura 		Altura máxima do campo
	#	@param 		largura 	Largura máxima do campo
	#
	def cria(self, altura, largura):

		# Cria o corpo da Snake no meio do campo
		for i in xrange(self.data['tam'], 1, -2):

			# Define as coordenada X e Y de cada parte do corpo
			corpo = {
				'x': (altura / 2),
				'y': (largura / 2) + 1 + i
			}

			self.data['corpo'].append(corpo)

	# Método imprime
	#
	#	Imprime a Snake na tela
	#
	def imprime(self):
		for corpo in self.data['corpo']:
			self.imprimeXY(corpo['x'], corpo['y'], c.C_x, c.BRANCO)

	# Método move
	#
	#	Move a Snake pelo campo
	#
	#	@param 			direc 		Direção do movimento
	#	@param 			seed 		Seed (para a Snake crescer)
	#	@param 			altura 		Altura máxima do campo
	# 	@param 			largura		Largura máxima do campo
	#
	#	@return 		integer     1: Movimento sem colisão e Snake cresceu
	#								0: Movimento sem colisão
	#							   -1: Colisão
	#
	def move(self, direc, seed, altura, largura):

		# Captura abeça e cauda da Snake
		tail = self.data['corpo'][-1]
		head = self.data['corpo'][0]

		# Variável para indicar a "projeção" do próximo movimento
		proj = {}

		# Movimenta a Snake para cima
		if direc == c.C_CIMA:
			proj['x'] = head['x'] - 1
			proj['y'] = head['y']

		# Movimenta a Snake para baixo
		elif direc == c.C_BAIXO:
			proj['x'] = head['x'] + 1
			proj['y'] = head['y']

		# Movimenta a Snake para a direita
		elif direc == c.C_DIR:
			proj['x'] = head['x']
			proj['y'] = head['y'] + 2

		# Movimenta a Snake para a esquerda
		elif direc == c.C_ESQ:
			proj['x'] = head['x']
			proj['y'] = head['y'] - 2

		# Verifica colisão
		if not self.colide(proj, altura, largura):

			# Verifica se a Snake cresce
			if self.cresce(proj, seed):
				
				# Atualiza a velocidade
				self.data['veloc'] -= 0.01

				# Indica o crescimento da Snake
				ret = 1

			else:

				# Limpa a posição da cauda da Snake no campo
				self.imprimeXY(tail['x'], tail['y'], c.C_ESPACO, c.ORIGINAL)

				# Remove a cauda da Snake
				self.data['corpo'].pop()

				# Indica que a Snake não cresceu
				ret = 0

			# Desenha o movimento no campo
			self.imprimeXY(proj['x'], proj['y'], c.C_x, c.BRANCO)

			# Insere a cauda na posição inicial (cabeça)
			self.data['corpo'].insert(0, proj)

			# Delay do movimento
			time.sleep(self.data['veloc'])

			return ret

		# Movimento NOK (Houve colisão)
		else:
			return -1

	# Método cresce
	#
	#	Verifica se a Snake irá "comer a Seed" e se deve "crescer"
	#
	#	@param 		proj 		Projeção do próximo movimento
	#	@param 		seed 		Seed (para a Snake crescer)
	# 	@return 				boolean (True, se a Snake irá "comer a Seed", False, caso contrário)
	#
	def cresce(self, proj, seed):
	
		# Verifica se a Snake irá "comer" a Seed
		if proj['x'] == seed['x'] and proj['y'] == seed['y']:
		    return True

		else:
			return False

	# Método colide
	#
	#	Verifica se a Snake irá colidir
	#
	#	@param 		proj 		Projeção do próximo movimento
	#	@param 		altura 		Altura máxima do campo
	# 	@param 		largura 	Largura máxima do campo
	#	@return 				boolean (True, se houve colisão, False, caso contrário)
	#
	def colide(self, proj, altura, largura):

		# Verifica se a Snake irá colidir com as paredes
		if proj['x'] <= 1 or proj['y'] <= 1:
		    return True

		elif proj['x'] >= altura or proj['y'] >= (largura - 1):
			return True

		# Verifica se a Snake irá colidir com ela mesma
		for corpo in self.data['corpo']:
			if proj['x'] == corpo['x'] and proj['y'] == corpo['y']:
			   	return True

		return False