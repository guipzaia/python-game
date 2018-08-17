#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Classe Getch
#
#   Lê as teclas informadas
#
class Getch:

    # Construtor
    def __init__(self):

        # Chamada para Plataforma Unix
        try:
            self.impl = GetchUnix()

        # Chamada para Plataforma Windows
        except ImportError:
            self.impl = GetchWindows()

    # Chamador
    def __call__(self):
        return self.impl()

    # Destrutor
    def __del__(self):
        del self.impl

# Classe GetchUnix
#
#   Lê as teclas informadas (Plataforma Unix)
#
class GetchUnix:

    # Construtor
    def __init__(self):

        # Bibliotecas Padrão
        import sys, termios

        # Atributos da Classe
        #
        #   Guarda configurações originais do terminal
        #
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

    # Chamador
    def __call__(self):

        # Bibliotecas Padrão
        import sys, tty

        # Bibliotecas Personalizadas
        import constantes as c

        # Lê caracter informado
        try:
            tty.setraw(sys.stdin.fileno())

            # Verifica se há conteúdo
            if self.isData():
                ch = sys.stdin.read(1) # Lê conteúdo

                # Caracter de ESCAPE
                if ch == c.C_27:
                    ch = sys.stdin.read(1) # Lê conteúdo

                    # Caracter de ESCAPE
                    if ch == c.C_91:            
                        ch = sys.stdin.read(1) # Lê conteúdo
                        return ch

                # Caracteres "Q" ou "q"
                elif (ch == c.C_Q) or (ch == c.C_q):
                    return ch

        except ImportError:
            pass

        return None

    # Destrutor
    def __del__(self):

        # Bibliotecas Padrão
        import termios

        # Reseta as configurações orignais do terminal
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    # Método isData
    #
    #   Verifica se há conteúdo digitado
    #
    #   @return     boolean (True / False)
    #
    def isData(self):

        # Bibliotecas Padrão
        import sys, select

        # Retorno boleano
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# Classe GetchWindows
#
#   Lê as teclas informadas (Plataforma Windows)
#
class GetchWindows:

    # Construtor
    def __init__(self):

        # Bibliotecas Padrão
        import msvcrt

    # Chamador
    def __call__(self):

        # Bibliotecas Padrão
        import msvcrt

        # Lê caracter informado
        return msvcrt.getch()

    # Destrutor
    def __del__(self):
        pass