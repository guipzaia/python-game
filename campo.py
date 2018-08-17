#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bibliotecas Padrão
import random

# Bibliotecas Personalizadas
import printer
import constantes as c
from snake import Snake

# Classe Campo (extends Printer)
class Campo(printer.Printer):

	# Construtor da classe
	def __init__(self):

		# Atributos da classe
		self.data = {
			'altura'  : 30,      # Altura do campo
			'largura' : 50,      # Largura do campo
			'snake'   : Snake(), # Snake
			'seed'    : None     # Seed
		}

		# Espaçamento das colunas
		self.data['largura'] *= 2

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
	#	Cria o campo do jogo
	#
	def cria(self):

		self.criaSnake() # Cria a Snake
		self.criaSeed()  # Cria Seed

	# Método criaSnake
	#
	#	Cria a Snake no campo
	#
	def criaSnake(self):
		self.data['snake'].cria(self.data['altura'], self.data['largura'])

	# Método criaSeed
	#
	#	Cria a "Seed" (para fazer a Snake crescer)
	#
	def criaSeed(self):

		while True:

			# Gera números randômicos para as coordenadas X e Y da Seed
			#	dentro dos limites do campo
			x = random.randrange(2, (self.data['altura'] - 1), 1)
			y = random.randrange(3, (self.data['largura'] - 1), 2)

			# Flag para validar se a Seed foi criada corretamente
			valida = True

			# Percorre o "corpo" da Snake
			for corpo in self.data['snake'].data['corpo']:

				# Verifica se a Seed foi criada em um ponto onde a Snake já se econtra
				if corpo['x'] == x and corpo['y'] == y:
					valida = False
					break

			# Verifica se a Seed foi criada corretamente
			if valida:

				# "Seta" as coordenadas da Seed no campo
				self.data['seed'] = {'x': x, 'y': y}
				break

	# Método imprimeSeed
	#
	#	Imprime a Seed no campo
	#
	def imprimeSeed(self):
		self.imprimeXY(self.data['seed']['x'], self.data['seed']['y'], c.C_x, c.AMARELO)

	# Método imprime
	#
	#	Imprime o campo na tela
	#
	def imprime(self):

		# Imprime as partes superior e inferior do campo
   		for i in xrange(1, self.data['largura'], 2):
			self.imprimeXY(1, i, c.C_x, c.VERDE)
			self.imprimeXY(self.data['altura'], i, c.C_x, c.VERDE)

		# Imprime as partes laterais do campo
		for i in xrange(2, self.data['altura'], 1):
			self.imprimeXY(i, 1, c.C_x, c.VERDE)
			self.imprimeXY(i, (self.data['largura'] - 1), c.C_x, c.VERDE)

		# Imprime a Snake no campo
		self.data['snake'].imprime()

		# Imprime a Seed no campo
		self.imprimeSeed()

	# Método moveSnake
	#
	#	Movimenta a Snake pelo campo de acordo com a direção informada
	#
	#	@param 		direc 		Direção informada
	#
	#	@return 	integer     1: Movimento sem colisão e Snake cresceu
	#							0: Movimento sem colisão
	#						   -1: Colisão
	#
	def moveSnake(self, direc):

		# Movimenta a Snake
		ret = self.data['snake'].move(direc, self.data['seed'], self.data['altura'], self.data['largura'])

		# Verifica se Snake "comeu" a Seed
		if ret == 1:
			self.criaSeed()		# Gera nova Seed
			self.imprimeSeed()	# Imprime a Seed no campo

		return ret