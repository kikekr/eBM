#!/usr/bin/python
from gi.repository import Gtk
from FileLibroDao import FileLibroDao
from View import View
from gi.repository import GLib, Gtk, GObject
import threading, gettext, locale
from os.path import abspath, dirname, join
from operator import itemgetter
import time
import timeit

class Controlador:	
	
	
	
	def __init__(self):
		self.N = 8
		self.conexion = FileLibroDao()
		self.builder = Gtk.Builder()
		self.glade_file = "Interfaz.glade"
		self.builder.add_from_file(self.glade_file)
		self.builder.connect_signals(self)
		self.searchedData = []
		self.ordenAscendente = True
		self.ordenGenreAsc = True
		self.ordenTitleAsc = True
		self.ordenEditAsc = True
		self.selected = 0
		self.daoLibro = FileLibroDao()
		self.view = View(self.builder)
		self.view.load_books()
		Gtk.main()
	
	#----------------------- WINDOW ---------------------#
	
	def on_window_destroy(self, widget, data = None):
		Gtk.main_quit()
		
	def on_searchentry1_search_changed(self, widget, data = None):
		    print "Searching..", widget.get_text()
		    self.searchedData = self.daoLibro.find(widget.get_text())
		    self.view.set_DataModelTreeView(self.searchedData[0:9], self.get_moreItems(self.searchedData))
		    
	def on_myCheckBut_toggled(self, widget, data):
		
		self.progressbar = self.view.getProgressBar()
		if (self.progressbar.get_fraction() >= 1):
			self.progressbar.set_fraction(0)
		
		self.model = self.view.get_model()
		self.model[data][4] = not self.model[data][4]
		
		if self.model[data][4]:
			self.selected += 1
		else:
			self.selected -= 1
		

		   
	
	#-------------------- MIS LIBROS --------------------#
		    
	def on_but_subir_clicked(self, widget, data = None):
		if self.selected != 0:
			self.view.getRefeed().show()
		
	def on_windowcheck_destroy(self, widget, data = None):
		self.view.getRefeed().hide()
	
	def on_confirm_clicked(self, widget, data=None):
				self.view.getConf().hide()
		
	
	def sleep(self,t, msg):
		GObject.threads_init()
		self.progressbar = self.view.getProgressBar()
		while (self.progressbar.get_fraction() < 1):
			print self.progressbar.get_fraction()*100, " %"
			time.sleep(t/10)
			new_value = self.progressbar.get_fraction() + 0.1
			self.progressbar.set_fraction(new_value)
		print msg
		
		
	def on_toolbuttonYES_clicked(self, widget, data = None):
		print "Subiendo archivos seleccinados.."
		self.view.getRefeed().hide()
		
		thread_sleep = threading.Thread(target=self.sleep, args=(10,"Terminado"))
		thread_sleep.start()
		
		
	def on_toolbuttonNO_clicked(self, widget, data = None):
		print "Deshaciedo cambios.."
		self.view.getRefeed().hide()
	
	def on_edit_row(self, path, column, data= None):
		self.rowToEdit= column
		self.liststore = self.view.get_model()
		self.treeiter = self.liststore.get_iter(column)
		self.oldData = [self.liststore.get_value(self.treeiter, 1),self.liststore.get_value(self.treeiter, 0),self.liststore.get_value(self.treeiter, 3),self.liststore.get_value(self.treeiter, 2)]
		self.view.show_editBook(self.liststore[column][1], self.liststore[column][0], self.liststore[column][3], self.liststore[column][2])
	
	
	def on_authorcolumn_clicked(self, widget, data= None):
		if self.ordenAscendente and not self.searchedData == []:
			self.ordenAscendente = False
			self.searchedData = sorted(self.searchedData, key=lambda k: k['author'])
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
		else:
			self.ordenAscendente = True
			self.searchedData = self.searchedData[::-1]
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
			
			
	def on_genrecolumn_clicked(self, widget, data= None):
		if  self.ordenGenreAsc and not self.searchedData == []:
			self.ordenGenreAsc = False
			self.searchedData = sorted(self.searchedData, key=lambda k: k['genero'])
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
		else:
			self.ordenGenreAsc = True
			self.searchedData = self.searchedData[::-1]
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
			
	def on_titlecolumn_clicked(self, widget, data= None):
		if  self.ordenTitleAsc and not self.searchedData == []:
			self.ordenTitleAsc = False
			self.searchedData = sorted(self.searchedData, key=lambda k: k['title'])
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
		else:
			self.ordenTitleAsc = True
			self.searchedData = self.searchedData[::-1]
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
		
	def on_editorialcolumn_clicked(self, widget, data= None):
		if  self.ordenEditAsc and not self.searchedData == []:
			self.ordenEditAsc = False
			self.searchedData = sorted(self.searchedData, key=lambda k: k['editorial'])
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
		else:
			self.ordenEditeAsc = True
			self.searchedData = self.searchedData[::-1]
			self.page = self.view.get_currentPage()
			self.newOrder = self.searchedData[self.page*self.N:(self.page+1)*self.N+1]
			self.view.set_DataModelTreeView(self.newOrder, self.get_moreItems(self.newOrder))
			
	#---------------- BUSQUEDA AVANZADA -----------------#
	
	def on_but_buscar_avanzado_clicked(self, widget, data =None):	
		self.notebook = self.view.get_Notebook()
		self.page = self.view.get_currentPage()
		self.notebook.set_current_page(0)
		self.searchedData = self.daoLibro.advanced_search(self.view.get_EntryAutor().get_text(), self.view.get_EntryTitulo().get_text(), self.view.get_EntryGenero().get_text(), self.view.get_EntryEditorial().get_text())
		self.view.set_DataModelTreeView(self.searchedData[0:self.N], self.get_moreItems(self.searchedData[0:self.N+1]))
		

	def on_siguiente_activate(self,widget, data=None):
		self.page = self.view.get_currentPage()
		self.nextData = self.searchedData[(self.page+1)*self.N:(self.page+2)*self.N+1]	
		self.view.set_nextPageDataModel(self.nextData[0:self.N], self.get_moreItems(self.nextData))
		
	def on_anterior_activate(self, widget, data=None):		
		self.page = self.view.get_currentPage()
		self.previousData = self.searchedData[(self.page-1)*self.N:self.page*self.N]
		self.view.set_previousPageDataModel(self.previousData)
		
	def get_moreItems(self,currentData):
			if  len(currentData)>self.N:
				return True
			else:
				return False
		
	def on_accept_edit(self, widget, data=None):
		self.oldAuthor = self.oldData[0]
		print self.oldAuthor
		self.newAuthor = self.view.get_newAuthor()
		self.oldTitle = self.oldData[1]
		self.newTitle = self.view.get_newTitle()
		self.oldGenre = self.oldData[2]
		self.newGenre = self.view.get_newGenre()
		self.oldEditorial = self.oldData[3]
		self.newEditorial = self.view.get_newEditorial()

		print "Eliminando: 	", self.oldTitle
		self.daoLibro.remove(self.oldTitle)
		self.daoLibro.create(self.newAuthor, self.newTitle, self.newGenre, self.newEditorial)
		
		self.liststore.set_value(self.treeiter,1,self.newAuthor)
		self.liststore.set_value(self.treeiter,0,self.newTitle)
		self.liststore.set_value(self.treeiter,3,self.newGenre)
		self.liststore.set_value(self.treeiter,2,self.newEditorial)
		self.view.closeWindowEdit()

	def on_cancel_edit(self, widget, data=None):
		self.view.closeWindowEdit()
		


c = Controlador()
