from tkinter import *
from tkinter import ttk, filedialog
from tkinter.font import Font
import customtkinter 
import json
import datetime
import os
import sys
from pdfgenerator import pdfFactura
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
    print(precio)
    return float(precioListado)
def generarFactura():
    if presupuestoCheckbox.get() == 1:
        precio = obtenerPrecio(numerosModif.get())
        datos = {"nfactura": nfactura.get(),"nif":dni.get(),"termino":termino.get(),"nombre":nombre.get(),"direccion":direccion.get(),"postal":postal.get(),"text":textbox.get("1.0",END)}
    else:
        with open("data/datos/clientes.json") as file:
            datos = json.load(file)
        
        datosCliente = datos["clientes"]
        
        cliente = {}
        
        for elementos in datosCliente:
            if elementos["nombre"] == fechasModif.get():
                cliente = elementos  
        
        precio = float(baseImponibleEntry.get())
        datos = {"nfactura": nfactura.get(),"nif":cliente["nombre"],"termino":termino.get(),"nombre":cliente["nombre"],"direccion":cliente["direccion"],"postal":cliente["postal"]+" "+cliente["ciudad"],"text":textbox.get("1.0",END)}

    # Diálogo para guardar archivo.
    ruta = filedialog.asksaveasfilename(
        filetypes=(
        ("Archivo pdf", "*.pdf"),))
    #print(str(ruta))
    
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    
    presupuestos = data["presupuestosInternos"]
    
    presupuesto = presupuestos[numerosModif.get()]
    
    factura = pdfFactura(fechasModif.get(),ruta,datos,precio)

    
    facturas = data["facturas"]
    nombreArchivo = ruta.split("/")
    if presupuestoCheckbox.get() == 1:
        precio = obtenerPrecio(numerosModif.get())
    else:
        precio = float(baseImponibleEntry.get())
    facturas[nfactura.get()] = {"nombreArchivo":nombreArchivo[len(nombreArchivo)-1],"nfactura": nfactura.get(),"nif":dni.get(),"termino":termino.get(),"nombre":nombre.get(),"direccion":direccion.get(),"postal":postal.get(),"text":textbox.get("1.0",END)}

    
    data["facturas"] = facturas
    

    
   
    with open("data/datos/registros.json", 'w') as file:
        json.dump(data, file, indent=4)
        
    with open("data/datos/nfactura.json") as file:
        data = json.load(file)
    
    data["numero"] += 1
    
    with open("data/datos/nfactura.json","w") as file:
        json.dump(data,file,indent=4) 

def obtenerFechas():
    with open("data/datos/clientes.json") as file:
        data = json.load(file)
    
    fechas = []
    
    clientes = data["clientes"]
    for fecha in clientes:
        datos = fecha["nombre"]
        nombre = list(datos)
        fechas.append("".join(nombre))
    return tuple(fechas)

def actualizarPresupuestos():
    with open("data/datos/registros.json") as file:
        data = json.load(file)
    presupuetosList = []
    presupuetos = data["presupuestosInternos"]
    for presupuesto in presupuetos.items():
        presupuetosList.append(presupuesto[1]["numeroPresupuestoInterno"])
    return tuple(presupuetosList)

def obtenerPresupuesto(choice):
    print(numerosModif.get())

def obtenerFacturas():
    with open("data/datos/presupuestosInternos.json") as file:
        data = json.load(file)
    
    
    if presupuestoCheckbox.get() == 1:
        facturasList = data[numerosModif.get()]
    else:
        facturasList = []
    #print(facturasList)

    return tuple(facturasList)
def actualizarFacturas(choice):
    print(fechasModif.get())
    clientes = obtenerFacturas()

def checkbox():
    print(presupuestoCheckbox.get(),type(presupuestoCheckbox.get()))
    if presupuestoCheckbox.get() == 1:
        fechasModif.grid_forget()
        dni.grid(row=4,column=1)
        nombre.grid(row=6,column=1)
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

        

def ponerNum():
    with open("data/datos/nfactura.json") as file:
        data = json.load(file)
    date = datetime.datetime.now()
    numero = data["numero"]
    year = str(date.year)[-2:]
    ceros = "0"*(4-len(str(numero)))
    num = f"F{year}{ceros}{numero}"
    nfactura.delete(0, END)  # Borrar el contenido actual del Entry
    nfactura.insert(0, str(num))
        

baseImponibleEntry = customtkinter.CTkEntry(F,placeholder_text="Base imponible: ",width=200,font=fontFactura)
baseImponibleEntry.grid(row=2,column=1,padx=120,pady=10)

numerosPresupuestos = actualizarPresupuestos()
numerosModif = customtkinter.CTkComboBox(F, values=numerosPresupuestos, state="readonly",justify="center",command=obtenerPresupuesto,width=200)
try:
    numerosModif.set(numerosPresupuestos[0])
except IndexError:
    numerosModif.set("")
#numerosModif.grid(row=2,column=1,padx=120,pady=10)

presupuestoCheckbox = customtkinter.CTkCheckBox(F, text='Usar presupuesto',command=checkbox)

presupuestoCheckbox.grid(row=0,column=1,pady=10)    
    
#lista de productos
fechas = obtenerFechas()
fechasModif = customtkinter.CTkComboBox(F, values=fechas, state="readonly",justify="center",command=actualizarFacturas,width=200)
try:
    fechasModif.set(fechas[0])
except IndexError:
    fechasModif.set("")

fechasModif.grid(row=1,column=1,pady=10)

nfactura = customtkinter.CTkEntry(F,placeholder_text="Nº factura",width=200,font=fontFactura)
nfactura.grid(row=3,column=1,padx=20,pady=10,columnspan=2)

dni = customtkinter.CTkEntry(F,placeholder_text="NIF",width=200,font=fontFactura)

termino = customtkinter.CTkEntry(F,placeholder_text="Término",width=200,font=fontFactura)
termino.grid(row=5,column=1,padx=20,pady=10,columnspan=2)

nombre = customtkinter.CTkEntry(F,placeholder_text="Nombre facturado",width=200,font=fontFactura)


direccion = customtkinter.CTkEntry(F,placeholder_text="Direccion facturado",width=200,font=fontFactura)

postal = customtkinter.CTkEntry(F,placeholder_text="Codigo postal facturado",width=200,font=fontFactura)


textbox = customtkinter.CTkTextbox(F,width=400,height=100)
textbox.grid(row=9,column=1,padx=20,columnspan=2)

button = customtkinter.CTkButton(F,text="Generar factura", command=generarFactura,width=200,font=fontFactura)
button.grid(row=10,column=1,pady=10,columnspan=2)
#textbox.grid(row=0,column=0)
#button.grid(row=1,column=0)

#textbox.insert("0.0",text)
#textbox.configure(state="normal")
ponerNum()

F.title("Factura")
F.mainloop()