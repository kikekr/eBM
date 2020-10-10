#!/usr/bin/python
from gi.repository import GLib, Gtk, GObject
from os.path import abspath, dirname, join
import gettext, locale

APP = 'View'
WHERE_AM_I = abspath(dirname(__file__))
LOCALE_DIR = join(WHERE_AM_I, 'locale')

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
locale.bindtextdomain(APP, LOCALE_DIR)
locale.textdomain(APP)


class View:
	def __init__(self, builder):
		self.currentPage = 0 
		self.builder = builder
		self.checkwin = builder.get_object("windowcheck")
		self.win = self.builder.get_object("window")
		self.windowEdit = self.builder.get_object("windowEdit")
		self.entryAutor = self.builder.get_object("entryAutor")	
		self.entryTitulo = self.builder.get_object("entryTitulo")	
		self.entryGenero = self.builder.get_object("entryGenero")	
		self.entryEditorial= self.builder.get_object("entryEditorial")	
		self.editAuthor = self.builder.get_object('entry1')
		self.editTitle = self.builder.get_object('entry2')
		self.editGenre = self.builder.get_object('entry3')
		self.editEditorial = self.builder.get_object('entry4')

		self.win.show()
		
	def getProgressBar(self):
		return self.builder.get_object('progressbar2')	
		
	def getConf(self):
		return self.builder.get_object('windowConf')
	
	def getRefeed(self):
		return self.checkwin
	
	def load_books(self):
		self.myBooks = self.builder.get_object("but_buscar_avanzado")
		self.myBooks.clicked()
	
	def get_Notebook(self):
		return self.builder.get_object('notebook1')
		
	def get_model(self):
		return self.builder.get_object('liststore1')
    
	def get_AuthorLabel(self):
		return self.builder.get_object('label6').get_text()
		
	def get_TitleLabel(self):
		return self.builder.get_object('label7').get_text()
		
	def get_GenreLabel(self):
		return self.builder.get_object('label8').get_text()
		
	def get_EditorialLabel(self):
		return self.builder.get_object('label9').get_text()
		
	def get_EntryAutor(self):
		return self.entryAutor
		
	def get_EntryTitulo(self):
		return self.entryTitulo
		
	def get_EntryGenero(self):
		return self.entryGenero
		
	def get_EntryEditorial(self):
		return self.entryEditorial
	
	
	def get_currentPage(self):
		return self.currentPage
	
	def set_nextPageDataModel(self, searchedData, moreItems):
		self.currentPage = self.currentPage+1
		self.set_DataModelTreeView(searchedData, moreItems)
		self.set_currentPage()
	
	def set_previousPageDataModel(self, searchedData):
		self.set_PreviousButtons()
		self.nextButton = self.builder.get_object('button4')
		self.nextButton.show()
		self.currentPage = self.currentPage-1
		self.set_DataModelTreeView(searchedData,True)
		self.set_currentPage()
		
	def set_DataModelTreeView(self,searchedData, moreItems):
		self.model  = self.builder.get_object('liststore1')
		self.moreItems = moreItems
		self.model.clear()
		self.set_PreviousButtons()
		self.set_NextButtons(moreItems)
		index = 0	
		while index < len(searchedData):
			self.model.append([searchedData[index]['title'], searchedData[index]['author'], searchedData[index]['editorial'], searchedData[index]['genero'], False])
			index = index + 1
		self.set_currentPage()
		
	def set_PreviousButtons(self):
		if self.model == [] or self.currentPage<=0:
			self.previousButton = self.builder.get_object('button3')
			self.previousButton.hide()
		else:
			self.previousButton = self.builder.get_object('button3')
			self.previousButton.show()	
		
	def set_NextButtons(self,moreItems):	
		if not moreItems or self.model == []:
			self.nextButton = self.builder.get_object('button4')
			self.nextButton.hide()
		else:
			self.nextButton = self.builder.get_object('button4')
			self.nextButton.show()	
				
		
	def show_editBook(self, old_author, old_title, old_genre, old_editorial):
		self.editAuthor.set_text(old_author)
		self.editTitle.set_text(old_title)
		self.editGenre.set_text(old_genre)
		self.editEditorial.set_text(old_editorial)
		self.windowEdit.show()
		print ''
		
	def get_newAuthor(self):
		return self.editAuthor.get_text()
		
	def get_newTitle(self):
		return self.editTitle.get_text()
	
	def get_newGenre(self):
		return self.editGenre.get_text()
		
	def get_newEditorial(self):
		return self.editEditorial.get_text()
		
	def closeWindowEdit(self):
		self.windowEdit.hide()
	
		
	def set_currentPage(self):
		if not self.model.get_iter_first() == None:
			label = self.builder.get_object('label10')
			label.set_text(str(self.currentPage))

	

