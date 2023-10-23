from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import customtkinter
import json
import os
import sys
from data.config import *
from sympy import symbols, Eq, solve






class Table:
     
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
                        relief="flat",
                        font=fontTablaEncabezado)
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
        self.tabla.column(self.encabezado[0], width=280, anchor="center")
        self.tabla.column(self.encabezado[1], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[2], width=anchos, anchor="center")
        self.tabla.column(self.encabezado[3], width=120, anchor="center")
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
        
        # Crear una barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=xx+800,y=yy,height=768)
        
        
        #self.root.geometry(f"{ancho}x{100+(10*(len(productos)-1))}")    

        self.tabla.place(x=xx,y=yy)

    

F = customtkinter.CTk()
rutaClientes = "data/datos/clientes.json"
rutaProductos = "data/datos/productos.json"

t = Table(F)
t.generarTabla(670,20)

def reiniciar():
    os.execl(sys.executable, sys.executable, * sys.argv) 


def leerJson(ruta):
    with open(ruta) as file:
        data = json.load(file)
    return data




def obtenerFamilias():
    
    data = leerJson(rutaProductos)
    return data["familias"]

def actualizarFamilias(event):
    pass



def crearFamilia():
    familiaScreen = customtkinter.CTk()
    
    
    familiaEntry = customtkinter.CTkEntry(familiaScreen,border_width=3, font=fontCompra)
    familiaEntry.grid(row=0,column=0)
    
    
    def crearFamiliaProducto():
        data = leerJson(rutaProductos)
        
        data["familias"].append(familiaEntry.get())
        
        with open(rutaProductos, 'w') as file:
            json.dump(data, file, indent=4)
        
        familiasModif.configure(values=obtenerFamilias())
        familiasModif.set(familiaEntry.get())
        familiaScreen.destroy()
        
    crearFamiliaButton = customtkinter.CTkButton(familiaScreen, text="crear familia",command=crearFamiliaProducto)
    crearFamiliaButton.grid(row=1,column=0)
    
    familiaScreen.title("Crear familia")
    familiaScreen.mainloop()



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
        precioEntry.insert(0, str(round(solucion[0],2)))
    
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
  
    #print(round(pvResultado))
def obtenerProductos():
    with open(rutaProductos) as file:
        # Read the contents of the file into a string
        data = json.load(file)
    
    dataProductos = data
    
    productos = [('Nombre', 'Referencia', "Familia",'Precio compra', 'Margen', 'PV')]
    
    for element in dataProductos.items():
        producto = []
        if list(element)[0] != "familias":
            diccionario = list(element)[1]
            producto.append(list(element)[0])
            for apartados in diccionario.values():
                producto.append(apartados)
        
        #print(list(element))
                
        productos.append(tuple(producto))
    return productos

def obtenerListaProductos():
    data = leerJson(rutaProductos)
    productos = []
    for element in data.items():
        if element[0] != "familias":
            productos.append(element[0])
    return tuple(productos)

def crearProducto():
    data = leerJson(rutaProductos)
    
    data[nombreEntry.get()] = {}
    
    try:
        producto = {
            "referencia": referenciaEntry.get(),
            "familia": familiasModif.get(),
            "precioCompra": str(int(round(float(precioEntry.get())))),
            "margen": margenEntry.get(),
            "precioMargen": str(int(round(float(pvEntry.get()))))
            
        }
    except ValueError:
        producto = {
            "referencia": referenciaEntry.get(),
            "familia": familiasModif.get(),
            "precioCompra": "",
            "margen": margenEntry.get(),
            "precioMargen": ""
            
        }
    
    
    valido = True
    
    for element in producto.items():
        if element[0] in ["precioCompra","margen","precioMargen"]:
            if element[1] == "":
                valido = False
    if nombreEntry.get() == "":
        valido = False
    
    if valido == True:
        
        data[nombreEntry.get()] = producto
        
        with open(rutaProductos, 'w') as file:
                json.dump(data, file, indent=4)
        print(producto)
        #t.actualizarTabla(producto,450,20)
        
        reiniciar()
    else:
        
        campos = []
        
        if nombreEntry.get() == "":
            campos.append("Nombre")
        if precioEntry.get() == "":
            campos.append("Precio de compra")
        if margenEntry.get() == "":
            campos.append("Margen")
        if precioEntry.get() == "":
            campos.append("Precio venta")
        
        
        
        warn.configure(text="Falta por rellenar los campos:\n "+", ".join(campos))
        
        warn.grid(row=9,column=0,columnspan=3,pady=10)












def eliminarProducto():
    seleccion =t.tabla.index(t.tabla.selection())  # Obtiene la selección actual como una lista de identificadores
    data = t.data
    dataResult = {}
    i = 0
    for elementos in data.items():
    
        if i != seleccion+1:
            dataResult[elementos[0]] = elementos[1]
        i += 1
        
    print(seleccion,data)
    
    
    
    
    #print(data)
    with open(rutaProductos, 'w') as file:
        json.dump(dataResult, file, indent=4)
    
    reiniciar()






nombre = StringVar(F)
nombreEntry = customtkinter.CTkEntry(F,border_width=3,placeholder_text="Nombre",font=fontCompra)
nombreEntry.grid(row=2,column=0,padx=10)


referencia = StringVar(F)
referenciaEntry = customtkinter.CTkEntry(F,border_width=3,placeholder_text="Referencia",font=fontCompra)
referenciaEntry.grid(row=2,column=1,pady=10,padx=10)


#lista de productos
familias = obtenerFamilias()
familiasModif = customtkinter.CTkComboBox(F, values=familias, state="readonly",justify="center")
try:
    familiasModif.set("Familia")
except IndexError:
    familiasModif.set("")
familiasModif.grid(row=2,column=2,padx=10)
familiasModif.bind("<<ComboboxSelected>>", actualizarFamilias)







precio = StringVar(F)
precioEntry = customtkinter.CTkEntry(F,border_width=3,placeholder_text="Precio compra",font=fontCompra)
precioEntry.grid(row=4,column=0,padx=10)

margenEntry = customtkinter.CTkEntry(F,border_width=3,placeholder_text="Margen",font=fontCompra)
margenEntry.grid(row=4,column=1,padx=10)

pvEntry = customtkinter.CTkEntry(F,border_width=3,placeholder_text="Precio venta",font=fontCompra)
pvEntry.grid(row=4,column=2,padx=10)

buttonCalcular = customtkinter.CTkButton(F,text="calcular",command=precioIva,width=17,font=fontCompra)
buttonCalcular.grid(row=6,column=0,columnspan=2,sticky="EWNS",padx=10,pady=10)

buttonCrear = customtkinter.CTkButton(F,text="crear material",command=crearProducto,width=17,font=fontCompra)
buttonCrear.grid(row=6,column=2,pady=10,sticky="EW")

buttonEliminar = customtkinter.CTkButton(F,text="borrar material",command=eliminarProducto,width=17,font=fontCompra)
buttonEliminar.grid(row=7,column=0,columnspan=2,sticky="EWNS",pady=10,padx=10)

buttonCrearFamilia = customtkinter.CTkButton(F, text="crear familia",command=crearFamilia,width=17,font=fontCompra)
buttonCrearFamilia.grid(row=7,column=2,sticky="EW")

pvIvaLabel = customtkinter.CTkLabel(F,text="Precio con IVA: ",font=fontTitulos)
pvIvaLabel.grid(row=8,column=0,columnspan=3)

warn = customtkinter.CTkLabel(F, text="", text_color="red", font=fontWarns)



F.title("Albaran de compra")
F.geometry("1300x650")
F.mainloop()
