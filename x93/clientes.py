from tkinter import *
from tkinter import ttk
import customtkinter
import json
import sys
import os
from data.config import *


F = customtkinter.CTk()
rutaClientes = "data/datos/clientes.json"
rutaProductos = "data/datos/productos.json"
clienteSeleccionado = 0



def reiniciar():
    os.execl(sys.executable, sys.executable, * sys.argv) 


def obtenerClientes():
    with open(rutaClientes) as file:
        data = json.load(file)
    
    
    nombres = ()
    for elementos in data["clientes"]:
        nombres = nombres + (elementos["nombre"] ,)
    return nombres
        

def crearCliente():
    global clientes
    with open(rutaClientes) as file:
        data = json.load(file)
    
    with open(rutaProductos) as file:
        dataProductos = json.load(file)
    
    
    valores = {"nombresClientes": nombreEdit.get(), 
            "apellidosCliente": apellidoEdit.get(), 
            "telefonoCliente": telefonoEdit.get(),
            "dniCliente":dniEdit.get(),
            "direccionCliente": direccionEdit.get(),
            "postalCliente": postalEdit.get(),
            "ciudadCliente": ciudadEdit.get()}
    
    crearClienteBool = True
    
    for elementos in valores.values():
        if elementos == "":
            crearClienteBool = False
    
    if crearClienteBool == True:    
        data["clientes"].append({
        'nombre': valores["nombresClientes"],
        'apellidos':  valores["apellidosCliente"],
        'telefono': valores["telefonoCliente"],
        "dni":valores["dniCliente"],
        "direccion":valores["direccionCliente"],
        "postal":valores["postalCliente"],
        "ciudad":valores["ciudadCliente"]})
        
        with open(rutaClientes, 'w') as file:
            json.dump(data, file, indent=4)
        
        #dataProductos[valores["nombresClientes"]] = {}
        
        with open(rutaProductos, 'w') as file:
            json.dump(dataProductos, file, indent=4)
        
        
        nombresClientes.insert("end",valores["nombresClientes"])
        
    reiniciar()
    

def borrarCliente():
    global clientes
    
    with open(rutaClientes) as file:
        data = json.load(file)
    
    
    data["clientes"].pop(clientes.index(nombresClientes.get()))
    
    with open(rutaClientes, 'w') as file:
            json.dump(data, file, indent=4)

    reiniciar()
    

clientes = obtenerClientes()

def cambiarTextInfo():
    with open(rutaClientes) as file:
        elemento = json.load(file)
    cliente = elemento["clientes"]
    clienteInfo = cliente[clientes.index(nombresClientes.get())]
    ClienteNombreText.configure(text="Nombre: "+clienteInfo["nombre"])
    ClienteApellidoText.configure(text="Apellidos: "+clienteInfo["apellidos"])
    ClienteTelefonoText.configure(text="Telefono: "+clienteInfo["telefono"])
    ClienteDniText.configure(text="Dni: "+clienteInfo["dni"])
    ClienteDireccionText.configure(text="Direccion: "+clienteInfo["direccion"])
    clientePostalText.configure(text="Postal: "+clienteInfo["postal"])
    clienteCiudadText.configure(text="Ciudad: "+clienteInfo["ciudad"])





def cambiarApartado():
    with open(rutaClientes) as file:
        data = json.load(file)
    
    clientesModificar = data["clientes"]
    if cambioEdit.get() != "":
        for cliente in clientesModificar:
            if cliente["nombre"] == nombresClientes.get():
                cliente[modificarApartado.get()] = cambioEdit.get()
                if modificarApartado.get() == "nombre":
                    # Obtén la lista actual de valores del Combobox y modifícala
                    valores_actuales = nombresClientes["values"]
                    if nombresClientes.get() in valores_actuales:
                        index = valores_actuales.index(nombresClientes.get())
                        valores_actuales = valores_actuales[:index] + (cambioEdit.get(),) + valores_actuales[index + 1:]

                        # Actualiza los valores del Combobox con la nueva lista
                        nombresClientes["values"] = valores_actuales
                        nombresClientes.set(cambioEdit.get())  # Establece el nuevo valor seleccionado en el Combobox

                
    print(clientesModificar)
    data["clientes"] = clientesModificar
    with open(rutaClientes, 'w') as file:
            json.dump(data, file, indent=4)
    cambiarTextInfo()
    



nombreText = customtkinter.CTkLabel(F, text="Nombre",font=fontCliente)
nombreText.grid(row=1,column=0)

nombreEdit = Entry(F, width=30)
nombreEdit.grid(row=2,column=0,padx=10)


apellidoText = customtkinter.CTkLabel(F, text="Apellidos",font=fontCliente)
apellidoText.grid(row=1,column=1)

apellidoEdit = Entry(F, width=30)
apellidoEdit.grid(row=2,column=1,padx=10)

telefonoText = customtkinter.CTkLabel(F, text="Telefono",font=fontCliente)
telefonoText.grid(row=1,column=2)

telefonoEdit = Entry(F)
telefonoEdit.grid(row=2,column=2,padx=10)

dniText = customtkinter.CTkLabel(F, text="Dni",font=fontCliente)
dniText.grid(row=1,column=3)

dniEdit = Entry(F)
dniEdit.grid(row=2,column=3,padx=10)

direccionText = customtkinter.CTkLabel(F, text="Direccion",font=fontCliente)
direccionText.grid(row=1,column=4)

direccionEdit = Entry(F, width=30)
direccionEdit.grid(row=2,column=4,padx=10,sticky="EW")

clientePostalText = customtkinter.CTkLabel(F, text="Postal: ",font=fontCliente)
clientePostalText.grid(row=1,column=5)

postalEdit = Entry(F)
postalEdit.grid(row=2,column=5,padx=10)

clienteCiudadText = customtkinter.CTkLabel(F, text="Ciudad: ",font=fontCliente)
clienteCiudadText.grid(row=1,column=6)

ciudadEdit = Entry(F)
ciudadEdit.grid(row=2,column=6,padx=10)

crearClienteButton = Button(F, text="Crear cliente", command=crearCliente, width=15,bg="white",font=fontCliente)
crearClienteButton.grid(row=1,column=7,rowspan=2,sticky="EWNS",padx=10)




separaccionInfoText = 2
paddingInfoText = 10
stikyInfoText = "W"



InfoClienteLabel = customtkinter.CTkLabel(F,text="INFORMACIÓN",font=fontCliente)
InfoClienteLabel.grid(row=4,column=0,columnspan = separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteNombreText = customtkinter.CTkLabel(F, text="Nombre: ",font=fontCliente)
ClienteNombreText.grid(row=5,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteApellidoText = customtkinter.CTkLabel(F, text="Apellido: ",font=fontCliente)
ClienteApellidoText.grid(row=6,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteTelefonoText = customtkinter.CTkLabel(F, text="Telefono: ",font=fontCliente)
ClienteTelefonoText.grid(row=7,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteDniText = customtkinter.CTkLabel(F, text="Dni: ",font=fontCliente)
ClienteDniText.grid(row=8,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteDireccionText = customtkinter.CTkLabel(F, text="Direccion: ",font=fontCliente)
ClienteDireccionText.grid(row=9,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClientePostalText = customtkinter.CTkLabel(F, text="Postal: ",font=fontCliente)
ClientePostalText.grid(row=10,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)

ClienteCiudadText = customtkinter.CTkLabel(F, text="Ciudad: ",font=fontCliente)
ClienteCiudadText.grid(row=11,column=0,columnspan= separaccionInfoText, sticky="W", padx=paddingInfoText)



opciones = ("nombre","apellidos","telefono","dni","direccion")
modificarApartado = ttk.Combobox(F, values=opciones, state="readonly",justify="center")
modificarApartado.set("nombre")
modificarApartado.grid(row=5,column=3,padx=10)

cambioEdit = Entry(F, width=20)
cambioEdit.grid(row=5,column=2,padx=7,sticky="EW")

cambioTextLabel = customtkinter.CTkLabel(F,text="Escribe el cambio",font=fontCliente)
cambioTextLabel.grid(row=4,column=2)

cambioApartadoLabel = customtkinter.CTkLabel(F,text="Selecciona el apartado",font=fontCliente)
cambioApartadoLabel.grid(row=4,column=3)

cambioApartadoLabel = customtkinter.CTkLabel(F,text="Selecciona el cliente",font=fontCliente)
cambioApartadoLabel.grid(row=4,column=4)

nombresClientes = ttk.Combobox(F, values=clientes, state="readonly",justify="center")
try:
    nombresClientes.set(clientes[0])
except IndexError:
    nombresClientes.set("")
nombresClientes.grid(row=5,column=4,sticky="EW")

generarCambioButton = customtkinter.CTkButton(F, text="Modificar", command=cambiarApartado,font=fontCliente)
generarCambioButton.grid(row=6,column=2,columnspan=2,sticky="EWNS",pady=2,padx=2)

listarInfoClienteButton = customtkinter.CTkButton(F, text="Listar información", command=cambiarTextInfo,font=fontCliente)
listarInfoClienteButton.grid(row=6,column=4,columnspan=1,sticky="EWNS",pady=2)

borrarClienteButton = customtkinter.CTkButton(F, text="Eliminar Cliente", command=borrarCliente, width=15,font=fontCliente)
borrarClienteButton.grid(row=7,column=2,columnspan=3,sticky="EWNS",pady=2)

L = customtkinter.CTkLabel(F,text="")
L.grid(row=3,column=0)

L2 = customtkinter.CTkLabel(F,text="")
L2.grid(row=11,column=0)

F.title("Clientes")
F.mainloop()

