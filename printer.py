#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bibliotecas Padrão
import sys

# Classe Printer
class Printer:

	# Construtor da classe
	def __init__(self):
		pass		

	# Método imprimeXY
	#	
	#	Imprime um caracter em uma coordenada específica da tela
	#
	#	@param 			x 			Posição X da tela 
	#	@param 			y 			Posição Y da tela 		
	#	@param 			c 			Caracter a ser impresso
	#	@param 			cor			Cor do caracter a ser impresso
	#
	def imprimeXY(self, x, y, c, cor):
		sys.stdout.write("%s\x1b7\x1b[%d;%df%s\x1b8" % (cor, x, y, c))
		print "\033[%d;1H" % x