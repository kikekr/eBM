#!/usr/bin/python
import json
#import ConfigParser

#config = ConfigParser.ConfigParser()
#config.read('database.cfg')
#f = open(config.get('path')

#Implementacion del acceso a los datos

database = "newdb_books.json"

class FileLibroDao:
	
	def __init__ (self):
		print "Init"
		try :
			f = open(database)
		except IOError :
			print "Error : File not found"	
		print ""
	

	def create(self, autor, titulo, genero, editorial):
		try:		
			f = open(database)
			data = json.loads(f.read())	
			new_data = {"title": titulo,"author": autor, "genero": genero, "editorial": editorial}
			data.append(new_data);
			with open(database, 'w') as outfile:
				json.dump(data, outfile)
		except IOError:
			print 'File not found'
		
		
	def find(self, titulo):
		try:		
			f = open(database)
			data = json.loads(f.read())
			data = [index for index in data if index['title'] == titulo]
			return data
		except IOError:
			print 'File not found'
		
		
	def update(self, old_author, new_author, old_title, new_title, old_genre, new_genre, old_editorial, new_editorial):
		try:
			f = open(database)
			data = json.loads(f.read())
			data = [{"title": new_title,"author": new_author, "genero": new_genre, "editorial": new_editorial} if index['title'] == old_title and index['author'] == old_author and index['genero'] == old_genre and index['editorial'] == old_editorial else index for index in data]	
			with open(database,'w') as outfile:
				json.dump(data,outfile)
			print ""		
		except IOError:
			print 'File Not Found'
								
		
	def remove(self, titulo):	
		try:
			f = open(database)
			data = json.loads(f.read())		
			data = [index for index in data if not index['title'] == titulo]
			with open(database,'w') as outfile:
				json.dump(data,outfile)
		except IOError:
			print "File not found"
		
	
	def advanced_search(self,autor, titulo, genero, editorial):
		try:
			f = open(database)
			data = json.loads(f.read())		
					
			if titulo:
				data = [index for index in data if index['title'] == titulo]		
			if autor:
				data = [index for index in data if index['author'] == autor]
			if genero:
				data = [index for index in data if index['genero'] == genero]			
			if editorial:
				data = [index for index in data if index['editorial'] == editorial]
			return data
		
		except IOError:
			print "File not found"

	
