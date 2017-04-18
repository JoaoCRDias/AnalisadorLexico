#! python
#-*- conding: utf8 -*-
from sys import argv, exit
import re
# Operadores aritmeticos
operadoresAritmeticos = {'+','-','/','*','^',"++","--"}

# Operadores Logicos
operadoresLogicos = {"&&", "||","<=",">=","==","!=","=","<",">","!"}

# Palavras Reservadas
palavrasReservadas = {"char","int","float","if","else","return","for","while","continue","break","printf","void","scanf","include"}

# Separadores
separadores = {';','[',']','(',')','{','}','"',"'",'.','\t','\n',' ',","}

# Estruturas
numeros = {'1','2','3','4','5','6','7','8','9','0'}
letras = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
		'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		'_'}

regexNumber = r"^([+-]?[0-9]*)(\.{1}[\d]+)f?$|^\d+$"
regexTokens = r"^[a-zA-Z_]+[0-9a-zA-Z_]*$"

def tratandoLiterais(conteudo, i, arqSaida, strLiterais, linha, coluna):
	if conteudo[i] == '"':
		i+=1
		while True:
			if conteudo[i] == '"':
				strLiterais += str(linha) + " " + str(coluna) + " " + conteudo[i+1:i] + "\n"
				coluna += (i-(i-1))
				break
			else:
				i+=1
	return i, strLiterais, coluna

def anaLex(conteudo):
	arqSaida = open("saida.txt", "w")
	strPReservada = "Palavras Reservadas:\n"
	strOperadoresA = "Operadores Aritmeticos:\n"
	strOperadoresL = "Operadores Logicos:\n"
	strSeparadores = "Separadores:\n"
	strLiterais = "Literais:\n"
	strNumeros = "Numeros:\n"
	strComentarios = "Comentarios:\n"
	strErros = "Erros:\n"
	strBibliotecas = "Bibliotecas:\n"
	i = 0
	j = 0
	linha = 1
	coluna = 1
	while i < len(conteudo):
		if (conteudo[i] == '#'):
			strOperadoresL += str(linha) + " " + str(coluna) + " " + conteudo[i:i+1] + "\n"
			coluna+=1
			i+=1
			j = i
		if i < (len(conteudo)-1):
			#erro do tipo 8123a
			if (re.match(regexNumber, conteudo[i]) and conteudo[i+1] in letras) or (conteudo[i] == '*' and conteudo[i+1] =='*') or (conteudo[i] == '^' and conteudo[i+1] =='^'):
				strErros += "Erro na linha: " + str(linha) + " coluna:" + str(coluna) + "\n"
				while(True):
					if conteudo[i] in separadores:
						break
					else:
						i+=1
						coluna+=1


			#erros do tipo >> <<
			if conteudo[i] == conteudo[i+1] and (conteudo[i] == '>' or conteudo[i] == '<'):
				strErros += "Erro na linha: " + str(linha) + " coluna:" + str(coluna) + "\n"
				if conteudo[i+2] == '\n':
					i+=2
					coluna = 1
				else:
					coluna+=2
					i+=2
		#trata o erro de 3 operadores logicos ou aritmeticos juntos por exemplo ===, &&& ...
		if i < (len(conteudo)-2):
			if (conteudo[i] == conteudo[i+1]
				and conteudo[i] == conteudo[i+2]
				and ((conteudo[i] in operadoresLogicos)
				or (conteudo[i] in operadoresAritmeticos)
				or (conteudo[i:i+2] in operadoresLogicos)
				or (conteudo[i:i+2] in operadoresAritmeticos))):
				strErros += "Erro na linha: " + str(linha) + " coluna:" + str(coluna) + "\n"
				if conteudo[i+3] == '\n':
					i+=3
					coluna = 1
				else:
					coluna+=3
					i+=3
		#trata comentario de uma so linha //
		if conteudo[i] == '/' and conteudo[i+1] == '/':
			j = i+2
			auxColuna = coluna
			auxLinha = linha
			while(True):
				if conteudo[i] == '\n':
					linha+=1
					coluna=1
					break
				else:
					coluna+=1
					i+=1
			strComentarios += str(auxLinha) + " " + str(auxColuna) + " " + conteudo[j:i] + "\n"
			i+=1
			j = i
		#Trata comentarios de mais de uma linha /* */
		if conteudo[i] == '/' and conteudo[i+1] == '*':
			j = i+2
			auxColuna = coluna
			auxLinha = linha
			while(True):
				if conteudo[i] == '*' and conteudo[i+1] == '/':
					break
				else:
					if conteudo[i] == '\n':
						coluna = 1
						linha += 1
					coluna+=1
					i+=1
			strComentarios += str(auxLinha) + " " + str(auxColuna) + " " + conteudo[j:i] + "\n"
			coluna+=1
			i+=2
			j = i
		#if utilizado para tratar tokens que tem como separador elementos da classe de operadores logicos ou aritmeticos i=i, i+i (sem espaço)
		if re.match(regexTokens, conteudo[i]) and re.match(regexTokens,conteudo[i+1]) == None and not (conteudo[i+1] in separadores) and not (conteudo[i+1] in numeros):
			if j == i:
				strLiterais += str(linha) + " " + str(coluna) + " " + conteudo[i] + "\n"
				coluna+=1
			else:
				if(conteudo[j:i+1] in palavrasReservadas):
				 	strPReservada += str(linha) + " " + str(coluna) + " " + conteudo[j:i+1] + "\n"
				 	coluna+=((i+1)-j)
				else:
					strLiterais += str(linha) + " " + str(coluna) + " " + conteudo[j:i+1] + "\n"
					coluna+= ((i+1)-j)
			i+=1
			j = i
		#trata numeros separador por tokens exemplo 1==1
		if re.match(regexNumber, conteudo[i]) and re.match(regexNumber,conteudo[i+1]) == None and not (conteudo[i+1] in separadores) and not (conteudo[i+1] in letras):
			if j == i:
				strNumeros += str(linha) + " " + str(coluna) + " " + conteudo[i] + '\n'
				coluna+=1
			else:
				strNumeros += str(linha) + " " + str(coluna) + " " + conteudo[j:i+1] + "\n"
				coluna += ((i+1) - j)
			i+=1
			j = i
		#trata literais
		if conteudo[i] == '"':
			i, strLiterais, coluna = tratandoLiterais(conteudo, i, arqSaida, strLiterais, linha, coluna)
			i+=1
			j = i
		#trata os operadores artitmeticos de 2 caracteres ex ++ --
		if conteudo[i:i+2] in operadoresAritmeticos:
			strOperadoresA += str(linha) + " " + str(coluna) + " " + conteudo[i:i+2] + "\n"
			coluna+=2
			i+=2
			j = i
		#trata operadores aritmeticos de um caracter por exemplo + -
		if conteudo[i] in operadoresAritmeticos:
			strOperadoresA += str(linha) + " " + str(coluna) + " " + conteudo[i:i+1] + "\n"
			coluna+=1
			i+=1
			j = i
		#trata os operadores logicos de 2 caracteres ex || &&
		if conteudo[i:i+2] in operadoresLogicos:
			strOperadoresL += str(linha) + " " + str(coluna) + " " + conteudo[i:i+2] + "\n"
			coluna+=2
			i+=2
			j = i
		#trata os operadores logicos de um só caracter por exemplo = , < , >
		if conteudo[i] in operadoresLogicos:
			strOperadoresL += str(linha) + " " + str(coluna) + " " + conteudo[i:i+1] + "\n"
			coluna+=1
			i+=1
			j = i
		#trata os tokens separados por separadores simples exempo \n, ' '...
		if conteudo[i] in separadores:
			if conteudo[i] == '.':
				#garante float
				if re.match(regexNumber,conteudo[i+1]):
					i+=1
					continue
				#captura bibliotecas
				if conteudo[i+1] == 'h':
					strBibliotecas += str(linha) + " " + str(coluna) + " " + conteudo[j:i+2] + "\n"
					i+=2
					coluna += ((i+2)-j)
					continue
			#captura literais e palavras reservadas
			if re.match(regexTokens,conteudo[j:i]):
				if(conteudo[j:i] in palavrasReservadas):
				 	strPReservada += str(linha) + " " + str(coluna) + " " + conteudo[j:i] + "\n"
				 	coluna+= (i-j)
				else:
					strLiterais += str(linha) + " " + str(coluna) + " " + conteudo[j:i] + "\n"
					coluna+= (i-j)
			elif re.match(regexNumber,conteudo[j:i]):
				strNumeros += str(linha) + " " + str(coluna) + " " + conteudo[j:i] + "\n"
				coluna += (i - j)
			if conteudo[i] != ' ' and conteudo[i] != "\n" and conteudo[i] != "\t":
				strSeparadores += str(linha) + " " + str(coluna) + " " + conteudo[i] + "\n"
				coluna+=1
			else:
				coluna+=1
			j = i+1
		if conteudo[i] == '\n':
			auxCol = i+1
			coluna = 1
			linha += 1
		i+=1
	arqSaida.write(strLiterais + "\n")
	arqSaida.write(strOperadoresL + "\n")
	arqSaida.write(strOperadoresA + "\n")
	arqSaida.write(strSeparadores + "\n")
	arqSaida.write(strPReservada + "\n")
	arqSaida.write(strNumeros + "\n")
	arqSaida.write(strComentarios + "\n")
	arqSaida.write(strBibliotecas + "\n")
	arqSaida.write(strErros + "\n")

def main():
	try:
		if(not argv[1]):
			print ("Padrão de execução: python analex.py <nome_arquivo>\n")
			exit(0)
		else:
			arq = open(argv[1], 'r')
	except:
		print ("Padrão de execução: python analex.py <nome_arquivo>\n")
		exit()
	conteudo = arq.read()
	arq.close()
	if not conteudo:
		print("Arquivo vazio \n")
		exit()
	anaLex(conteudo)

if __name__ == '__main__':
	main()