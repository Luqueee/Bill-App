from tkinter import *
from tkinter import ttk, filedialog
from tkinter.font import Font
import customtkinter 
import json
import os
import sys
from pdfgenerator import pdfPresupuesto
from data.config import *


datos = {}
F = customtkinter.CTk()

def obtenerPrecio(numero):
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    dataPresupuestos = data["presupuestosInternos"]
    
    dataCliente = dataPresupuestos[numero]
    #dicFecha = data[fecha]
    productos = dataCliente["productos"]
    #productosDic = dicFecha[cliente]

    print(productos)
    precio = productos[-3][-1]
    precioListado = precio[:-2]
    return float(precioListado)
def generarPresupuesto():

    if presupuestoCheckbox.get() == 1:
        precio = obtenerPrecio(numerosModif.get())
        datos = {"npresupuesto": nfactura.get(),"nif":dni.get(),"nombre":nombre.get(),"direccion":direccion.get(),"postal":cliente["postal"]+" "+cliente["ciudad"],"text":textbox.get("1.0",END)}
    else:
        with open("data/datos/clientes.json") as file:
            datos = json.load(file)
        
        datosCliente = datos["clientes"]
        
        cliente = {}
        
        for elementos in datosCliente:
            if elementos["nombre"] == fechasModif.get():
                cliente = elementos  
        
        precio = float(baseImponibleEntry.get())
        datos = {"npresupuesto": nfactura.get(),"nif":cliente["nombre"],"nombre":cliente["nombre"],"direccion":cliente["direccion"],"postal":cliente["postal"]+" "+cliente["ciudad"],"text":textbox.get("1.0",END)}

    # Diálogo para guardar archivo.
    ruta = filedialog.asksaveasfilename(
        filetypes=(
        ("Archivo pdf", "*.pdf"),))
    #print(str(ruta))
    
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    
    presupuestosInternos = data["presupuestosInternos"]
    
    presupuesto = presupuestosInternos[numerosModif.get()]
    
    factura = pdfPresupuesto(numerosModif.get(),ruta,datos,precio)

    
    presupuestos = data["presupuestos"]
    nombreArchivo = ruta.split("/")
    if presupuestoCheckbox.get() == 1:
        precio = obtenerPrecio(numerosModif.get())
    else:
        precio = float(baseImponibleEntry.get())
    presupuestos[nfactura.get()] = {"nombreArchivo":nombreArchivo[len(nombreArchivo)-1],"npresupuesto": nfactura.get(),"nombre":nombre.get(),"direccion":direccion.get(),"postal":postal.get(),"text":textbox.get("1.0",END)}

    
    #data["presupuesto"] = facturas
    

    
   
    with open("data/datos/registros.json", 'w') as file:
        json.dump(data, file, indent=4)
        

def obtenerFechas():
    with open("data/datos/clientes.json") as file:
        data = json.load(file)
    
    clientes = data["clientes"]
    fechas = []
    for fecha in clientes:
        datos = fecha["nombre"]
        nombre = list(datos)
        fechas.append("".join(nombre))
    return tuple(fechas)

def obtenerPresupuestos():
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    
    presupuestosInternos = data["presupuestosInternos"]
    
    facturasList = []
    for elemento in presupuestosInternos.items():
        facturasList.append(elemento[0])
    #print(facturasList)
    return tuple(facturasList)

def obtenerPresupuesto(choice):
    print(numerosModif.get())

def actualizarPresupuestos():
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    presupuetosList = []
    presupuetos = data["presupuestosInternos"]
    for presupuesto in presupuetos.items():
        presupuetosList.append(presupuesto[1]["numeroPresupuestoInterno"])
    return tuple(presupuetosList)

def checkbox():
    print(presupuestoCheckbox.get(),type(presupuestoCheckbox.get()))
    if presupuestoCheckbox.get() == 1:
        fechasModif.grid_forget()
        dni.grid(row=4,column=1)
        nombre.grid(row=6,column=1,pady=10)
        direccion.grid(row=7,column=1,padx=20,pady=10,columnspan=2)
        postal.grid(row=8,column=1,padx=20,pady=10,columnspan=2)
        
        numerosModif.grid(row=2,column=1,padx=120,pady=10)
    else:
        fechasModif.grid(row=1,column=1,pady=10)
        numerosModif.grid_forget()
        
        dni.grid_forget()
        nombre.grid_info()
        direccion.grid_forget()
        nombre.grid_forget()
        postal.grid_forget()
#lista de productos
fechas = obtenerFechas()
fechasModif = customtkinter.CTkComboBox(F, values=fechas, state="readonly",justify="center",command=actualizarPresupuestos,width=200)
try:
    fechasModif.set(fechas[0])
except IndexError:
    fechasModif.set("")
#fechasModif.grid(row=1,column=1,padx=120,pady=10)


baseImponibleEntry = customtkinter.CTkEntry(F,placeholder_text="Base imponible: ",width=200,font=fontFactura)
baseImponibleEntry.grid(row=2,column=1,padx=120,pady=10)

numerosPresupuestos = obtenerPresupuestos()
numerosModif = customtkinter.CTkComboBox(F, values=numerosPresupuestos, state="readonly",justify="center",command=obtenerPresupuesto,width=200)
try:
    numerosModif.set(numerosPresupuestos[0])
except IndexError:
    numerosModif.set("")
#numerosModif.grid(row=2,column=1,padx=120,pady=10)

presupuestoCheckbox = customtkinter.CTkCheckBox(F, text='Usar presupuesto',command=checkbox)

presupuestoCheckbox.grid(row=0,column=1,pady=10)    

#lista de productos
facturas = obtenerFechas()
clienteModif = customtkinter.CTkComboBox(F, values=facturas, state="readonly",justify="center",width=200)
try:
    clienteModif.set(facturas[0])
except IndexError:
    clienteModif.set("")
clienteModif.grid(row=1,column=1,padx=120,pady=10)

nfactura = customtkinter.CTkEntry(F,placeholder_text="Nº presupuesto",width=200)
nfactura.grid(row=3,column=1,padx=20,pady=10,columnspan=2)

dni = customtkinter.CTkEntry(F,placeholder_text="NIF",width=200,font=fontFactura)

nombre = customtkinter.CTkEntry(F,placeholder_text="Nombre cliente",width=200)


direccion = customtkinter.CTkEntry(F,placeholder_text="Direccion cliente",width=200)

postal = customtkinter.CTkEntry(F,placeholder_text="Codigo postal cliente",width=200)

textbox = customtkinter.CTkTextbox(F,width=400,height=100)
textbox.grid(row=7,column=1,padx=20,columnspan=2)

button = customtkinter.CTkButton(F,text="Generar presupuesto", command=generarPresupuesto,width=200)
button.grid(row=8,column=1,pady=10,columnspan=2)
#textbox.grid(row=0,column=0)
#button.grid(row=1,column=0)

#textbox.insert("0.0",text)
#textbox.configure(state="normal")




F.title("Presupuesto")
F.mainloop()