# -*- coding: utf-8 -*-
import time, os
start_time=time.time()
import twint
# Configure
target = ''


#Esta función recibe un solo parámetro, el perfil a analizar.
#Primero chequea que el archivo no exista ya, para poder retomar en caso de haberse interrumpido
#Si el archivo no existe, corre las funciones following y followers y guarda el output en dos archivos diferentes: PERFIL_follow(ing/ers).txt
#Después de eso, al existir ya los archivos, llama a la función input para agregarlos al .csv
def scan(username):
	c = twint.Config()
	print(username)
	c.Username = username
	try:
		os.stat(str(target + '/' + username + '_followers.txt'))
	except FileNotFoundError:
		c.Output = str(target + '/' + username + '_followers.txt')
		print()
		print('FOLLOWERS')
		twint.run.Followers(c)
	input(str(target + '/' + username + '_followers.txt'), username, 'followers')
	try:
		os.stat(str(target + '/' + username + '_following.txt'))
	except FileNotFoundError:
		c.Output = str(target + '/' + username + '_following.txt')
		print()
		print('FOLLOWING')
		twint.run.Following(c)
	input(str(target + '/' + username + '_following.txt'), username, 'following')

#Esta función toma un archivo de scan() y lo agrega al .csv de todo el análisis
#Toma 3 parámetros, el nombre del archivo a agregar, el nombre de usuario y el tipo (followers/following)
#A partir de esos 3 parámetros puede completar el .csv según corresponda: poniendo el perfil seguidor en el primer espacio y el seguido en el segundo
def input(file, username, type):
	try:
		data=open(file, "r")
	except FileNotFoundError:
		return
	for line in data:
		if type == 'following':
			result.write(str(username + ',' + line))
		elif type == 'followers':
			result.write(str(line.strip() + ',' + username + "\n"))

#El programa comienza creando un directorio con el nombre del objetivo
try:
	os.stat(target)
except:
	os.mkdir(target)

#Después crea un archivo .csv para poner en él el resultado del análisis
#El .csv contiene líneas del tipo "A,B"; las cuales se interpretan como "A sigue a B" para constuir una matriz o grafo
result=open(str(target + "/" + target + "_network.csv"), "w")

#Primer grado de análisis: analiza el objetivo en cuestión
scan(target)

#Segundo grado de análisis: analiza cada perfil relacionado al objetivo,
#tomando las listas y haciendo un análisis en cada entrada.
for line in open(target + '/' + target + '_followers.txt',"r").readlines():
	scan(line.strip())
for line in open(target + '/' + target + '_following.txt',"r").readlines():
	scan(line.strip())

#Al final del proceso, escribe el tiempo que tardó en completar el análisis
end_time=time.time()
print(str(end_time - start_time, 'seconds'))
