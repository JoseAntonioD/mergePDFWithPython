# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:30:21 2018

@author: JoseL
"""

2
3
	
from tkinter import filedialog, Tk, Button, Label, messagebox, Listbox, Scrollbar, ttk, Frame
from tkinter.font import Font
from PyPDF2 import PdfFileMerger
import os
import shutil


class AddToPdf:

    
    
    #Variabeis globais.
    pdfsMerge=[]
    directory = ''
    
      
    
    #constructor
    def __init__(self, parent, findFiles,  pdfsMerge):
        
        self.parent = parent
        self.findFiles = findFiles
        #self.directory = directory
        self.pdfsMerge = pdfsMerge
        
        parent.resizable(1,1)
       
           
    def giveMeSecondaryFiles(self, event=None):
        

        global pdfsMerge, directoryMerge, pdfsMergeCopy, pdfsMergeII, filesnameMerge
        pdfsMerge =[]
        pdfsMergeII= []
        pdfsMergeCopy=[]
                
        if len(filename) > 0:
            #print('Filename: ',filename)
            filenamesMerge =  filedialog.askopenfilenames(initialdir = "/",title = "Seleccionar Archivo Maestro",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
        else:
            messagebox.showinfo("Información","Debe seleccionar el archivo maestro antes. Gracias.")
            return
            
        if len(filenamesMerge) == 0:
            return
                   
            
        directoryMerge = os.path.dirname(
                os.path.realpath(filenamesMerge[0]))
        
      
        for pdf in filenamesMerge:
            if pdf.endswith('.pdf'):
                pdfsMerge.append(pdf)
             
        pdfsMergeII = pdfsMerge[:]
        
        
       
        return pdfsMergeII
    
    
    def clickButton(self, event=None):
        
        global filename, directory
       
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Seleccionar Archivo Maestro",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
        directory = os.path.split(filename)[0]
        filename = os.path.split(filename)[1]
        
         #Concateno a / para a función shutil.copy
        directory = directory + '/'

        
    
    def findFiles( pdfsMerge):
        
        global nombre_archivo_salida
        
        
        #print(len(pdfsMergeII), directory)
        
        if len(pdfsMergeII) == 0:
            messagebox.showinfo("Información","No se han seleccionado archivos..")
            #print('Non existen rexistros')
            return
        
        try:
                
            #directory = os.path.split(filename)[0]
            #print(directory)
            #pdfs = [os.path.join(directory + '/',archivo) for archivo in os.listdir(directory) if archivo.endswith('.pdf')]
            str_ruta = ['backup__',filename]
            nombre_archivo_salida = ''.join(str_ruta)
             
            pdfsMerge.sort(key=os.path.basename)                   
                   
            #Copiamos o archivo que contén todo o contido.
            shutil.copy(os.path.join(directory,filename), os.path.join(directory,nombre_archivo_salida))
            shutil.copy(os.path.join(directory,filename), os.path.join(directory,'backup_'+nombre_archivo_salida))
            shutil.copy(os.path.join(directory,filename), os.path.join(directory,'copyfile.pdf'))
            deleteFile = [directory, filename]
            deleteFile = ''.join(deleteFile) 
            #print('Borrado:' , deleteFile)
            os.remove(deleteFile)
            
            #print('pdfmerge: ', pdfsMergeII)
            for pdf in pdfsMergeII:
               #Copiamos os archivos de un directorio a outro.
               newPdfFile = os.path.split(pdf)[1]
               newPdfOrigin = ''.join(newPdfFile)
               
               pdfsMergeCopy.append(directory+newPdfOrigin)
               if directory != (os.path.split(pdf)[0]+'/'):
                   shutil.copy(os.path.join(directoryMerge,pdf), os.path.join(directory,newPdfFile))
               
            pdfsMergeCopy.append(directory+'copyfile.pdf')
            #print('pdfsMergeCopy ---->>> ',pdfsMergeCopy)
            AddToPdf.operationsFiles(directory, filename, nombre_archivo_salida)
                    
            #Eliminar elementos de la lista.
            del pdfsMergeII[:]
            #print(pdfsMergeII)
    
    
        except:
                    
            #print('Non existe o arquivo!!!.')
            del pdfsMergeII[:]
            messagebox.showinfo("Información","Se ha producido un error en la operación.")
                           
                    
     
    def openFiles():
        #fps = [open(os.path.join(directory,f), 'rb') for f in pdfs]
        fps = [open(f, 'rb') for f in pdfsMergeCopy]

        return fps
    
    
    def operationsFiles( directory, filename, nombre_archivo_salida):
        global ficheros
        
        ficheros = AddToPdf.openFiles()
        AddToPdf.fusionarFiles(directory, filename,  ficheros, nombre_archivo_salida)
        AddToPdf.removeFiles(directory, nombre_archivo_salida, ficheros)
        AddToPdf.renameFile(nombre_archivo_salida, filename, directory)
        
        messagebox.showinfo("Información","Proceso terminado correctamente.")    
      
     #Unir/fusionar arquivos.
    def fusionarFiles( directory, filename,  ficheros, nombre_archivo_salida):
        global fusionador
        
        #print('Ficheros: ', ficheros)      
        #print(type(pdfsMergeCopy))
        fusionador = PdfFileMerger()    
        
        for f in ficheros:
            #print('FUSIONADOR: ',f)
            fusionador.append(f)         
        
        with open(os.path.join(directory,nombre_archivo_salida), 'wb') as salida:
            fusionador.write(salida)
            #print(salida)
        
        [fp.close() for fp in ficheros]

        
     #Borrar arquivos xa engadidos.
    def removeFiles( directory, nombre_archivo_salida, ficheros):   
        
        for arch in pdfsMergeCopy:
            if arch != (os.path.join(directory, nombre_archivo_salida)):
                deleteFile = [directory, os.path.split(arch)[1]]
                deleteFile = ''.join(deleteFile) 
                os.remove(deleteFile)
                 
            
     #Renomear arquivo orixinal.       
    def renameFile( nombre_archivo_salida, filename, directory):
        os.rename(os.path.join(directory,nombre_archivo_salida), os.path.join(directory,filename))
        
    def callback(self, event):
        self.findFiles( self.pdfsMerge)
        

def main():
    

    window = Tk()
       
    frame = Frame(window, width=580, height=420)
    frame.pack(fill='both', expand=1)
    frame.config(cursor="pirate")
    frame.config(bg="lightblue")
    frame.config(bd=25)
    frame.config(relief="sunken")
    frame.config()
    window.config(cursor="arrow")
#    window.config(bg="blue")
#    window.config(bd=15)
#    window.config(relief="ridge")
    

    window.title('Welcome to the Jungle')
     
    window.geometry('800x450+600+420')
   
    
    btnMasterFile = Button(window, text="SELECCIONE EL ARCHIVO MAESTRO", fg="black", bg="#FAAC58", height = 2, width = 85)
    btnMasterFile.pack()
    btnMasterFile.place(x=100, y=110)
    btnMasterFile.bind('<Button-1>', AddToPdf.clickButton)
                  

    btnSecondaryFiles=Button(window, text="SELECCIONE LOS ARCHIVOS SECUNDARIOS", fg="black", bg="#FAAC58", height = 2, width = 85)
    btnSecondaryFiles.pack()
    btnSecondaryFiles.place(x=100, y=150)
    btnSecondaryFiles.bind('<Button-1>',AddToPdf.giveMeSecondaryFiles)
    
#    listFiles = Listbox(window, selectmode=ttk.tkinter.MULTIPLE,  borderwidth=0, bg="#D8D8D8", font=Font(family="Courier New", size=10))
#    listFiles.pack()
#    listFiles.place(y = 157, x = 80, width = 605)
#    
#    Label(window, text="Arquivos a procesar.", bg="#04B4AE", fg="white", font=Font(family="Courier New", size=10)).place(x=80, y=135)

    Button(window, text="SALIR", fg="black", bg="#FAAC58", height = 2, width = 85, command= window.destroy).place(x=100, y=241)
        
    btnMerge = Button(window, text="UNIR ARCHIVOS", fg="black", bg="#FAAC58",  height = 2, width = 85)
    btnMerge.pack()
    btnMerge.place(x=100, y=200)
    obj2= AddToPdf(window,AddToPdf.findFiles, AddToPdf.pdfsMerge)
    btnMerge.bind('<Button-1>', obj2.callback)
    
#    label = Button( window, text="Click me",height = 1, width = 85 )    
#    label.pack()
#    label.place(x=80, y=210)
#    label.bind("<Button>", AddToPdf.mouseClick)
    

    
    #AddToPdf(window,AddToPdf.findFiles, directory, AddToPdf.pdfsMerge)
    window.mainloop() 

    
 
if __name__ == '__main__':
    main()     
         