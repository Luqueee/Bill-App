from tkinter import *
from tkinter import ttk, filedialog
import customtkinter

import json
import os
import sys
import datetime
from pdfgenerator import pdfPresupuestoInterno
from data.config import *
from sympy import symbols, Eq, solve


F = customtkinter.CTk()
rutaClientes = "data/datos/clientes.json"
rutaProductos = "data/datos/productos.json"
rutaPresupuestosInternos = "data/datos/presupuestosInternos.json"
rutaTablaPresupuestosInternos = "data/datos/tablaPresupuestoInterno.json"
rutaRegistros = "data/datos/registros.json"



class Table:
     
    def __init__(self,f):
         # find total number of rows and
        # columns in list
        self.root = f
        self.productosLista = [('Nombre', 'Cantidad', 'Referencia', "Familia",'Precio compra', 'Margen', 'PV', 'PV total')]
        
        self.style = ttk.Style()
    
        self.style.theme_use("default")

        self.style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        font=fontTabla,
                        borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])

        self.style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        font=fontTablaEncabezado,
                        relief="flat")
        self.style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])
        
        self.tabla=ttk.Treeview(self.root,height=len(self.productosLista)-1 ,columns=self.productosLista[0])
        self.tabla.config(show='headings')
        self.tabla.config(style="Treeview")
        
        
        
        
    def actualizarTabla(self,productos,xx,yy,ancho=1260):
        
        self.productosLista.append(tuple(productos))
        
        self.productosLista = self.calcPvTotal(self.productosLista)
        
        
        
       
        # Insertar datos de ejemplo
        encabezado = list(self.productosLista[0])
        # Definir el ancho de las columnas
        anchos = 133
        
        self.tabla=ttk.Treeview(self.root,height=30 ,columns=self.productosLista[0],selectmode="browse")
        self.tabla.config(show='headings')
        self.tabla.config(style="Treeview")
        self.tabla.column(encabezado[0], width=anchos)
        self.tabla.column(encabezado[1], width=anchos)
        self.tabla.column(encabezado[2], width=anchos)
        self.tabla.column(encabezado[3], width=anchos)
        self.tabla.column(encabezado[4], width=anchos)
        self.tabla.column(encabezado[5], width=anchos)
        self.tabla.column(encabezado[6], width=anchos)
        self.tabla.column(encabezado[7], width=anchos)
        
        
        self.tabla.heading(encabezado[0], text=encabezado[0], anchor=CENTER)
        self.tabla.heading(encabezado[1], text=encabezado[1], anchor=CENTER)
        self.tabla.heading(encabezado[2], text=encabezado[2], anchor=CENTER)
        self.tabla.heading(encabezado[3], text=encabezado[3], anchor=CENTER)
        self.tabla.heading(encabezado[4], text=encabezado[4], anchor=CENTER)
        self.tabla.heading(encabezado[5], text=encabezado[5], anchor=CENTER)
        self.tabla.heading(encabezado[6], text=encabezado[6], anchor=CENTER)
        self.tabla.heading(encabezado[7], text=encabezado[7], anchor=CENTER)
        
        for element in range(len(self.productosLista)-1):
            elementos = list(self.productosLista[element+1])
            
            self.tabla.insert("",END, values=tuple(elementos))
        
        #self.root.geometry(f"{ancho}x{110+(20*(len(self.productosLista)))}")    
        # Crear una barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=anchos*8,y=yy,height=625
                        )
        self.root.geometry(f"1260x1080")    

        self.tabla.place(x=xx,y=yy)
    def generarTabla(self,xx,yy,ancho=1260):
        
        with open(rutaTablaPresupuestosInternos) as file:
            
            data = json.load(file)
        self.productosLista = data
       
        # Insertar datos de ejemplo
        encabezado = self.productosLista[0]
        # Definir el ancho de las columnas
        anchos = 155
        
        dimAncho = round((self.root.winfo_screenheight())/6)+10

        self.tabla=ttk.Treeview(self.root,height=30 ,columns=self.productosLista[0],selectmode="browse")
        
        
        self.tabla.config(show='headings')
        self.tabla.config(style="Treeview")
        self.tabla.column(encabezado[0], width=201)
        self.tabla.column(encabezado[1], width=dimAncho)
        self.tabla.column(encabezado[2], width=dimAncho)
        self.tabla.column(encabezado[3], width=dimAncho)
        self.tabla.column(encabezado[4], width=dimAncho)
        self.tabla.column(encabezado[5], width=dimAncho)
        self.tabla.column(encabezado[6], width=dimAncho)
        self.tabla.column(encabezado[7], width=dimAncho)
        
        
        self.tabla.heading(encabezado[0], text=encabezado[0], anchor=CENTER)
        self.tabla.heading(encabezado[1], text=encabezado[1], anchor=CENTER)
        self.tabla.heading(encabezado[2], text=encabezado[2], anchor=CENTER)
        self.tabla.heading(encabezado[3], text=encabezado[3], anchor=CENTER)
        self.tabla.heading(encabezado[4], text=encabezado[4], anchor=CENTER)
        self.tabla.heading(encabezado[5], text=encabezado[5], anchor=CENTER)
        self.tabla.heading(encabezado[6], text=encabezado[6], anchor=CENTER)
        self.tabla.heading(encabezado[7], text=encabezado[7], anchor=CENTER)
        
        for element in range(len(self.productosLista)-1):
            elementos = list(self.productosLista[element+1])
            
            self.tabla.insert("",END, values=tuple(elementos))
        
        # Crear una barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=(dimAncho*8)+50,y=yy,height=767)
        self.root.geometry(f"1260x1080")    

        self.tabla.place(x=xx,y=yy)
    
    def calcPvTotal(self,lista):
        listaPV = lista
        for i in range(len(listaPV)):
            if i != 0 and len(listaPV[i]) <= 7:
                #print(listaPV[i])
                pvTotal = str(int(listaPV[i][1])*int(listaPV[i][6]))
                listPv = list(listaPV[i])
                listPv.insert(7,pvTotal)
                listaPV[i] = tuple(listPv)
        return listaPV




class TableProducts:
     
    def __init__(self,f):
         # find total number of rows and
        # columns in list
        rutaProductos = "data/datos/productos.json"
        with open(rutaProductos) as file:
            self.data = json.load(file)
        
        self.style = ttk.Style()
    
        self.style.theme_use("default")
        self.style.configure("Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            font=fontTabla,
            borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])

        self.style.configure("Treeview.Heading",
            background="#565b5e",
            foreground="white",
            font=fontTablaEncabezado,
            relief="flat")
        self.style.map("Treeview.Heading",
            background=[('active', '#3484F0')])
                
        self.encabezado = ['Nombre', 'Referencia', "Familia",'Precio compra', 'Margen', 'PV']
        self.productosNombres = self.data
        self.root = f
        self.tabla=ttk.Treeview(self.root,height=len(self.productosNombres),columns=self.encabezado)
        self.tabla.config(show='headings',height=30)
        self.tabla.config(style="Treeview")
    
    
    def generarTabla(self,xx,yy,ancho=1260):
        
        
        
        self.tabla=ttk.Treeview(self.root,height=len(self.productosNombres),columns=self.encabezado)
        self.tabla.config(show='headings',height=30)
        self.tabla.config(style="Treeview")

        # Definir el ancho de las columnas

        anchos = 100
        self.tabla.column(self.encabezado[0], width=300, anchor="center")
        self.tabla.column(self.encabezado[1], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[2], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[3], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[4], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[5], width=anchos, anchor="center")
        
        self.tabla.heading(self.encabezado[0], text=self.encabezado[0], anchor=CENTER)
        self.tabla.heading(self.encabezado[1], text=self.encabezado[1], anchor=CENTER)
        self.tabla.heading(self.encabezado[2], text=self.encabezado[2], anchor=CENTER)
        self.tabla.heading(self.encabezado[3], text=self.encabezado[3], anchor=CENTER)
        self.tabla.heading(self.encabezado[4], text=self.encabezado[4], anchor=CENTER)
        self.tabla.heading(self.encabezado[5], text=self.encabezado[5], anchor=CENTER)
        #print(tabla.get_children())
        
      
        # Insertar datos de ejemplo
       
        for element in self.productosNombres.items():
            
            if element[0] != "familias":
                elementos = []
                elementos.append(element[0])
                apartados = element[1]
                print(apartados)
                for apartado in apartados.items():
                    elementos.append(apartado[1])
                #print(elementos)
                self.tabla.insert("",END, values=tuple(elementos))
        
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=(anchos*6)+200,y=yy,height=630)
        
        #self.root.geometry(f"{ancho}x{100+(10*(len(productos)-1))}")    

        self.tabla.place(x=xx,y=yy)




t = Table(F)
t.generarTabla(10,75)

def reiniciar():
    os.execl(sys.executable, sys.executable, * sys.argv) 




def obtenerProductos():
    nombres = []
    with open(rutaProductos) as file:
        data = json.load(file)
    for element in data.items():
        if element[0] != "familias":
            nombres.append(element[0])
    return nombres
    
def obtenerClientes():
    clientes = []
    with open(rutaClientes) as file:
        data = json.load(file)
    dataClientes = data["clientes"]
    for element in dataClientes:
            clientes.append(element["nombre"])
    return clientes




def add():
    
    ventanaAdd = customtkinter.CTk()
    
    
    table = TableProducts(ventanaAdd)
    
    def añadir(personalizado = False, info=[]):
        
        
        with open(rutaTablaPresupuestosInternos) as file:
            tablaPresupuestosInternos = json.load(file)
            
        if personalizado == False:
            
            with open(rutaProductos) as file:
            # Read the contents of the file into a string
                productos = json.load(file)
            
            seleccion = table.tabla.selection()  # Obtiene la selección actual como una lista de identificadores
            if seleccion:
                elemento_seleccionado = seleccion[0]  # Obtén el primer elemento seleccionado si hay alguno
                #print(elemento_seleccionado)
                posicion = table.tabla.index(elemento_seleccionado)
                nombreProudcto = list(table.productosNombres)[posicion+1]
                
            
            
            producto = []
            infoProducto = productos[nombreProudcto]
            producto.append(nombreProudcto)
            cantidad = cantidadEntry.get()
            if cantidadEntry.get() == "":
                cantidad = "1"
            
            producto.append(cantidad)
            
            for element in infoProducto.items():
                
                producto.append(element[1])
            
            producto.append(str(round(float(infoProducto["precioMargen"])*int(cantidad))))
            
            
            tablaPresupuestosInternos.append(producto)
        else:
            producto = []
            producto.append(info["nombre"])
            cantidad = info["cantidad"]
            if cantidad == "":
                cantidad = "1"
            
            producto.append(cantidad)
            
            for element in info["info"]:
                
                producto.append(element)
            
            producto.append(str(round(float(info["precioMargen"])*int(cantidad))))
            
            
            tablaPresupuestosInternos.append(producto)
            
        with open(rutaTablaPresupuestosInternos, 'w') as file:
            json.dump(tablaPresupuestosInternos, file, indent=4)
    
        
        
        #t.actualizarTabla(tuple(productos),10,75)
        ventanaAdd.destroy()
        reiniciar()
    
    
    def añadirPersonalizado():
        
        
        def precioIva():
            #Precio de Venta = Precio del Producto / (1 - Margen de Ganancia)
            precioValue = precioEntry.get()
            margenValue = margenEntry.get()
            pvValue = pvEntry.get()
            if margenValue == "":
                margen_porcentaje = round(((float(pvValue) - float(precioValue)) / float(pvValue)) * 100,2)
                margenEntry.delete(0, END)  # Borrar el contenido actual del Entry
                margenEntry.insert(0, str(margen_porcentaje))
                margenValue = margenEntry.get()
            
            elif pvValue == "":
                pvResultado = round((float(precioValue)) / (1-(float(margenValue)/100)),2)
                pvEntry.delete(0, END)  # Borrar el contenido actual del Entry
                pvEntry.insert(0, str(pvResultado))
                
                
            elif precioValue == "":
                # Definir la variable simbólica a
                a = symbols('x')

                # Definir la ecuación
                ecuacion = Eq(float(pvValue), a / (1 - float(margenValue)/100))

                
                # Resolver la ecuación
                solucion = solve(ecuacion, a)

                precioEntry.delete(0, END)  # Borrar el contenido actual del Entry
                precioEntry.insert(0, str(round(solucion[0])))
            
            else:
                if precioValue != "" and margenValue != "" and pvValue != "":
                    margen_porcentaje = round(((float(pvValue) - float(precioValue)) / float(pvValue)) * 100,2)
                    pvResultado = round((float(precioValue)) / (1-(float(margenValue)/100)),2)

                    a = symbols('x')

                    # Definir la ecuación
                    ecuacion = Eq(float(pvValue), a / (1 - float(margenValue)/100))

                    
                    # Resolver la ecuación
                    solucion = round(float(solve(ecuacion, a)[0]),2)
                    
                #    if margen_porcentaje != margenValue:
                    
                    if pvResultado != pvValue:
                        pvEntry.delete(0, END)  # Borrar el contenido actual del Entry
                        pvEntry.insert(0, str(pvResultado))
                    
                    if precioValue != solucion:
                        pvEntry.delete(0, END)  # Borrar el contenido actual del Entry
                        pvEntry.insert(0, str(pvResultado))
                    
                    if margenValue != margen_porcentaje and pvResultado == pvValue and solucion == precioValue:
                        pvEntry.delete(0, END)  # Borrar el contenido actual del Entry
                        pvEntry.insert(0, str(pvResultado))
            
            
            
            
            
            
            precioFinal = float(pvEntry.get())
            precioConIva = round(precioFinal+(precioFinal*0.21),2)
            
            pvIvaLabel.configure(text=f"Precio con IVA: {str(precioConIva)}")
        
        def obtenerInfo():
            info = {"nombre":nombreEntry.get(),"cantidad":cantidadEntryP.get(),"precioMargen":pvEntry.get(),"info": [referenciaEntry.get(),familiaEntry.get(),precioEntry.get(),margenEntry.get(),pvEntry.get()]}
            return info
        
        ventanaP = customtkinter.CTk()
        
        nombreEntry = customtkinter.CTkEntry(ventanaP,border_width=3,placeholder_text="Nombre",font=fontCompra)
        nombreEntry.grid(row=2,column=0,padx=10)


        referenciaEntry = customtkinter.CTkEntry(ventanaP,border_width=3,placeholder_text="Referencia",font=fontCompra)
        referenciaEntry.grid(row=2,column=1,pady=10,padx=10)


        #lista de productos
        familiaEntry = customtkinter.CTkEntry(ventanaP, placeholder_text="Familia", font=fontCompra)
        familiaEntry.grid(row=2,column=2,padx=10)
        
        
        precioEntry = customtkinter.CTkEntry(ventanaP,border_width=3,placeholder_text="Precio compra",font=fontCompra)
        precioEntry.grid(row=4,column=0,padx=10)


        pvEntry = customtkinter.CTkEntry(ventanaP,border_width=3,placeholder_text="Precio venta",font=fontCompra)
        pvEntry.grid(row=4,column=2,padx=10)

        margenEntry = customtkinter.CTkEntry(ventanaP,border_width=3,placeholder_text="Margen",font=fontCompra)
        margenEntry.grid(row=4,column=1,padx=10)

        cantidadEntryP = customtkinter.CTkEntry(ventanaP, border_width=3,placeholder_text="Cantidad", font=fontCompra)
        cantidadEntryP.grid(row=6,column=0)
        
        buttonCalcular = customtkinter.CTkButton(ventanaP,text="calcular",command=precioIva,width=17,font=fontCompra)
        buttonCalcular.grid(row=6,column=1,sticky="EW",padx=10,pady=10)




        buttonCrear = customtkinter.CTkButton(ventanaP,text="añadir material",command=lambda:añadir(True, obtenerInfo()) ,width=17,font=fontCompra)
        buttonCrear.grid(row=6,column=2,pady=10,padx=10,sticky="EW")



        pvIvaLabel = customtkinter.CTkLabel(ventanaP,text="Precio con IVA: ",font=fontTitulos)
        pvIvaLabel.grid(row=7,column=0,columnspan=3)
        ventanaP.title("Albaran de compra")


        
        ventanaP.mainloop()
    
        añadir(True)


    
    
    table.generarTabla(0,100)
    
    ventanaAdd.title("Añadir producto")
    
    #  Obtenemos el largo y  ancho de la pantalla
    wtotal = ventanaAdd.winfo_screenwidth()
    htotal = ventanaAdd.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 700
    hventana = 600

    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)

    #  Se lo aplicamos a la geometría de la ventana
    ventanaAdd.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

    cantidadEntry = customtkinter.CTkEntry(ventanaAdd,placeholder_text="Indica la cantidad",font=fontPresupuestoInterno)
    cantidadEntry.grid(row=0,column=0)
    
    añadirButton = customtkinter.CTkButton(ventanaAdd, text="AÑADIR PRODUCTO", command=añadir)
    añadirButton.grid(row=0,column=1,padx=10)
    
    añadirButtonPersonalizado = customtkinter.CTkButton(ventanaAdd, text="AÑADIR PRODUCTO PERSONALIZADO", command=añadirPersonalizado)
    añadirButtonPersonalizado.grid(row=0,column=2,padx=10)
    
    
    
    
    ventanaAdd.mainloop()
    

def modif():
    ventanaModif = customtkinter.CTk()
    
    ventanaModif.title("Modificar producto")
    
    
    def precioIva(precioEntry,margenEntry,pvEntry = ""):
        #Precio de Venta = Precio del Producto / (1 - Margen de Ganancia)
        precioValue = precioEntry
        margenValue = margenEntry
        pvValue = pvEntry
        if pvEntry != "":
            resultado = round(((float(pvValue) - float(precioValue)) / float(pvValue)) * 100,2)
        else:
            resultado = round(float((float(precioValue)) / (1-(float(margenValue)/100))))

        return resultado
    
    apartados = [
        "Nombre",
        "Cantidad",
        "Referencia",
        "Familia",
        "Precio compra",
        "Margen",
        "PV",
    ]
    
    seleccion = t.tabla.selection()  # Obtiene la selección actual como una lista de identificadores
    if seleccion:
        elemento_seleccionado = seleccion[0]  # Obtén el primer elemento seleccionado si hay alguno
        #print(elemento_seleccionado)
        posicion = t.tabla.index(elemento_seleccionado)+1
    else:
        ventanaModif.destroy()
        
    def canviar():
        with open(rutaTablaPresupuestosInternos) as file:
            tablaPresupuestosInternos = json.load(file)
        
        producto = tablaPresupuestosInternos[posicion]
        producto[apartados.index(apartadosModif.get())] = modifEntry.get()
        if apartadosModif.get() == "Cantidad":
            
            num = float(producto[-2])
            producto[-1] = str(num*int(modifEntry.get()))
        
        if apartadosModif.get() == "Precio compra" or apartadosModif.get() == "Margen" or apartadosModif.get() == "PV":

            
            
            if apartadosModif.get() == "Precio compra":
                
                resultado = precioIva(producto[-4],producto[-3])
                producto[-2] = str(resultado)
                
            if apartadosModif.get() == "Margen":
                resultado = precioIva(producto[-4],producto[-3],producto[-2])
                producto[-2] = str(round(float((float(producto[-2])) / (1-(float(producto[-3])/100)))))
            
            if apartadosModif.get() == "PV":
                resultado = precioIva(producto[-4],producto[-3])
                producto[-3] = str(resultado)
                # Definir la variable simbólica a
                a = symbols('x')

                # Definir la ecuación
                ecuacion = Eq(int(producto[-2]), a / (1 - 33.3/100))

                # Resolver la ecuación
                solucion = solve(ecuacion, a)
                print(solucion)
                producto[-4] = str(round(float(solucion[0]),2))
                producto[-3] = "33.3"

                
            producto[-1] = str(int(producto[-2])*int(producto[1]))
        
        
        
        
        #tablaPresupuestosInternos[posicion][apartados.index(apartadosModif.get())] = modifEntry.get()
        tablaPresupuestosInternos[posicion] = producto

        with open(rutaTablaPresupuestosInternos, 'w') as file:
            json.dump(tablaPresupuestosInternos, file, indent=4)
    
        ventanaModif.destroy()
        reiniciar()
    
    
    
        
    
    
        
    apartadosModif = customtkinter.CTkComboBox(ventanaModif, values=apartados, state="readonly",justify="center",height=10)
    try:
        apartadosModif.set(apartados[0])
    except IndexError:
        apartadosModif.set("")    
    
    apartadosModif.grid(row=0,column=0)
    
    
    modifEntry = customtkinter.CTkEntry(ventanaModif, border_width=3, font=fontPresupuestoInterno)
    modifEntry.grid(row=1,column=0)
    
    modifButton = customtkinter.CTkButton(ventanaModif, text="GENERAR CANVIO",command=canviar)
    modifButton.grid(row=2,column=0)
            
    ventanaModif.mainloop()
    
     
    

def remove():
    seleccion = t.tabla.selection()  # Obtiene la selección actual como una lista de identificadores
    if seleccion:
        elemento_seleccionado = seleccion[0]  # Obtén el primer elemento seleccionado si hay alguno
        #print(elemento_seleccionado)
        posicion = t.tabla.index(elemento_seleccionado)
        t.productosLista.pop(posicion+1)
    #print("removido")
    with open(rutaTablaPresupuestosInternos) as file:
        data = file
    
    data = t.productosLista
    #print(data)
    with open(rutaTablaPresupuestosInternos, 'w') as file:
        json.dump(data, file, indent=4)
    
    reiniciar()


def guardarArchivo():
    pantalla = customtkinter.CTk()
    
    def guardar():
        # Diálogo para guardar archivo.
        ruta = filedialog.asksaveasfilename(
            filetypes=(
            ("Archivo pdf", "*.pdf"),))
        print(ruta)
        
        rutaSplit = ruta.split("/")
        presupuestoInternoPdf = pdfPresupuestoInterno(clientesModif.get(),t.productosLista,ruta)
        
        with open("data/datos/registros.json") as file:
            data = json.load(file)
        
        with open("data/datos/presupuestosInternos.json") as file:
            dataInterno = json.load(file)
        
        
        fecha = datetime.datetime.now()
        facturas = data["presupuestosInternos"]
        nombreArchivo = ruta.split("/")
        facturas[f"{numero.get()}"] = {"cliente": clientesModif.get(),"nombreArchivo": nombreArchivo[len(nombreArchivo)-1],"numeroPresupuestoInterno": numero.get(),"fecha":f"{fecha.day}:{fecha.month}:{fecha.year}"  ,"productos": t.productosLista}

        dataInterno[f"{numero.get()}"] = {f"{clientesModif.get()}": t.productosLista}
        
        data["presupuestosInternos"] = facturas
        
        with open("data/datos/registros.json", 'w') as file:
            json.dump(data, file, indent=4)
        
        with open("data/datos/presupuestosInternos.json", 'w') as file:
            json.dump(dataInterno, file, indent=4)
        
        
        pantalla.destroy()
    numero = customtkinter.CTkEntry(pantalla,placeholder_text="numero del presupuesto")
    numero.grid(row=0,column=0)
    
    boton = customtkinter.CTkButton(pantalla,text="Guardar",command=guardar)
    boton.grid(row=1,column=0)
    
    pantalla.title("Guardar archivo")
    pantalla.mainloop()


def descargarArchivo():
    pantalla = customtkinter.CTk()
    
    def guardar():
        # Diálogo para guardar archivo.
        ruta = filedialog.asksaveasfilename(
            filetypes=(
            ("Archivo pdf", "*.pdf"),))
        print(ruta)
        
        presupuestoInternoPdf = pdfPresupuestoInterno("",t.productosLista,ruta)
        
        
        
        pantalla.destroy()
    numero = customtkinter.CTkEntry(pantalla,placeholder_text="numero del presupuesto")
    numero.grid(row=0,column=0)
    
    boton = customtkinter.CTkButton(pantalla,text="Guardar",command=guardar)
    boton.grid(row=1,column=0)
    
    pantalla.title("Guardar archivo")
    pantalla.mainloop()



def generar():
    with open(rutaPresupuestosInternos) as file:
        data = json.load(file)
    
    with open(rutaTablaPresupuestosInternos) as file:
        dataTabla = json.load(file)
    
    
    productosLista = t.calcPvTotal(t.productosLista)
    #print(productosLista)
    
    fecha = datetime.datetime.now()
    fechaActual = f"{fecha.day}:{fecha.month}:{fecha.year}"
    diccionario = {}
    diccionario[clientesModif.get()] = productosLista


    
    
    with open(rutaPresupuestosInternos, 'w') as file:
        json.dump(data, file, indent=4)
    
    
    with open(rutaTablaPresupuestosInternos, 'w') as file:
        json.dump(productosLista, file, indent=4)
    
    
    guardarArchivo()

def descargarPresupuesto():
    
    with open(rutaTablaPresupuestosInternos) as file:
        dataTabla = json.load(file)
    
    
    productosLista = t.calcPvTotal(t.productosLista)
    #print(productosLista)
    
    fecha = datetime.datetime.now()
    fechaActual = f"{fecha.day}:{fecha.month}:{fecha.year}"
    diccionario = {}
    diccionario[clientesModif.get()] = productosLista


    
    
    
    
    with open(rutaTablaPresupuestosInternos, 'w') as file:
        json.dump(productosLista, file, indent=4)
    
    
    descargarArchivo()

def importarPresupuesto():
    ventanaImp = customtkinter.CTk()
    
    with open(rutaRegistros) as file:
        data = json.load(file)
    registros = data["presupuestosInternos"]
    
    
    def importar():
        with open(rutaTablaPresupuestosInternos) as file:
            dataTabla = file
        
        presupuesto = registros[presupuestosModif.get()]

        productos = presupuesto["productos"]
        
        dataTabla = productos[:len(productos)-3]
        
        with open(rutaTablaPresupuestosInternos, 'w') as file:
            json.dump(dataTabla, file, indent=4)
            
        ventanaImp.destroy()
        reiniciar()
    
        

        
    
    registrosList = list(registros)
    
    
    
    presupuestosModif = customtkinter.CTkComboBox(ventanaImp, values=registrosList, state="readonly",justify="center",height=10)
    try:
        presupuestosModif.set(registrosList[0])
    except IndexError:
        presupuestosModif.set("")

    presupuestosModif.grid(row=0,column=0)
    
    buttonImportar = customtkinter.CTkButton(ventanaImp,text="Importar presupuesto",command=importar)
    buttonImportar.grid(row=1,column=0)
    ventanaImp.title("Importar presupuesto")
    ventanaImp.mainloop()
    
    
    
    

def obtenerPresupuestosInternos():
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    
    facturas = data["presupuestosInternos"]
    
    numeros = []
    for element in facturas.keys():
        numeros.append(element)
    
    return tuple(numeros)

def nuevoPresupuesto():
    with open(rutaTablaPresupuestosInternos) as file:
        data = json.load(file)
    
    with open(rutaTablaPresupuestosInternos, 'w') as file:
        json.dump([data[0]], file, indent=4)
    
    reiniciar()

def eliminarPresupuesto():
    
    ventanaEliminar = customtkinter.CTk()
    
    
    def Eliminar():
        
        with open("data/datos/registros.json") as file:
                data = json.load(file)
    
        presupuestos = data["presupuestosInternos"]
        
        
        
        del presupuestos[presupuestosModif.get()]
        
        with open(rutaRegistros, 'w') as file:
            json.dump(data, file, indent=4)
    
        
        ventanaEliminar.destroy()
        reiniciar()
    
    presupuestos = obtenerPresupuestosInternos()
    presupuestosModif = customtkinter.CTkComboBox(ventanaEliminar, values=presupuestos, state="readonly",justify="center",height=10)
    try:
        presupuestosModif.set(presupuestos[0])
    except IndexError:
        presupuestosModif.set("")

    presupuestosModif.grid(row=0,column=0,sticky="EW",padx=2)

    eliminarButton = customtkinter.CTkButton(ventanaEliminar, text="Eliminar presupuesto", command=Eliminar)
    eliminarButton.grid(row=1,column=0)

    ventanaEliminar.title("Eliminar presupuesto")
    
    ventanaEliminar.mainloop()





    
l = customtkinter.CTkLabel(F,text=" ")
l.grid(row=2,column=0)

#lista de clientes
clientes = obtenerClientes()
clientesModif = customtkinter.CTkComboBox(F, values=clientes[1:], state="readonly",justify="center",height=10)
try:
    clientesModif.set(clientes[1])
except IndexError:
    clientesModif.set(clientes[0])

clientesModif.grid(row=3,column=1,sticky="EW",padx=2)



buttonAdd = customtkinter.CTkButton(F,text="Añadir",command=add,width=17,font=fontPresupuestoInterno)
buttonAdd.grid(row=3,column=4,sticky="EW",padx=2)

buttonRemove = customtkinter.CTkButton(F,text="Eliminar",command=remove,width=17,font=fontPresupuestoInterno)
buttonRemove.grid(row=3,column=5,padx=2,sticky="EW")

buttonModif = customtkinter.CTkButton(F,text="Modificar",command=modif,width=17,font=fontPresupuestoInterno)
buttonModif.grid(row=3,column=6,padx=2,sticky="EW")


buttonGenerar = customtkinter.CTkButton(F,text="Nuevo presupuesto",command=nuevoPresupuesto,width=17,font=fontPresupuestoInterno)
buttonGenerar.grid(row=3,column=7,sticky="EW",padx=2)

ButtonEliminar = customtkinter.CTkButton(F,text="eliminar presupuesto",command=eliminarPresupuesto,width=17,font=fontPresupuestoInterno)
ButtonEliminar.grid(row=3,column=8,sticky="EW",padx=2)

buttonimportar = customtkinter.CTkButton(F,text="Importar presupuesto",command=importarPresupuesto,width=17,font=fontPresupuestoInterno)
buttonimportar.grid(row=3,column=9,sticky="EW",padx=2)

buttonGenerar = customtkinter.CTkButton(F,text="Generar presupuesto",command=generar,width=17,font=fontPresupuestoInterno)
buttonGenerar.grid(row=3,column=10,padx=2,sticky="EW")

Buttondescargar = customtkinter.CTkButton(F,text="descargar presupuesto",command=descargarPresupuesto,width=17,font=fontPresupuestoInterno)
Buttondescargar.grid(row=3,column=11,sticky="EW",padx=2)




F.title("Presupuesto interno")


#  Obtenemos el largo y  ancho de la pantalla
wtotal = F.winfo_screenwidth()
htotal = F.winfo_screenheight()
#  Guardamos el largo y alto de la ventana
wventana = 1260
hventana = 700

#  Aplicamos la siguiente formula para calcular donde debería posicionarse
pwidth = round(wtotal/2-wventana/2)
pheight = round(htotal/2-hventana/2)

#  Se lo aplicamos a la geometría de la ventana
F.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

F.mainloop()