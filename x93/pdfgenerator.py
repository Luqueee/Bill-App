import datetime
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


class pdfPresupuestoInterno:
    def __init__(self, cliente,datos,ruta):

        self.datosSuma = datos
        self.suma = self.precioTotal()
        import json
        rutaPrecio = "data/datos/precio.json"
        with open(rutaPrecio) as file:
            data = json.load(file)
        print(data)
        data["suma"] = float(self.suma)
        
        with open(rutaPrecio, 'w') as file:
            json.dump(data, file, indent=4)
        datos.append(["","","","","","","Precio total",f"{self.suma}€"])
        datos.append(["","","","","","","21% IVA",f"{round(self.suma*0.21,2)}€"])
        datos.append(["","","","","","","suma total",f"{round(self.suma+(self.suma*0.21),2)}€"])
        
        
        self.generarPdf(cliente,ruta,datos)
        
        rutaSplit = ruta.split("/")
        #print(rutaSplit)
        #print(f"data/presupuesto_interno/{rutaSplit[len(rutaSplit)-1]}-{cliente}")
        fecha = datetime.datetime.now()
        self.generarPdf(cliente,f"data/presupuesto_interno/{rutaSplit[len(rutaSplit)-1]}-{cliente}_{fecha.day}-{fecha.month}-{fecha.year}",datos)
        # Crear un objeto de estilo de párrafo para las celdas
        # Crear el documento PDF
    
    def generarPdf(self,cliente,ruta,datos):
        
    
        rutaClientes = "data/datos/clientes.json"
        doc = SimpleDocTemplate(f"{ruta}.pdf", pagesize=letter)
        
        
        styles = getSampleStyleSheet()
        estilosParagrapho = styles["Normal"]

        # Crear un estilo de párrafo personalizado con la fuente deseada
        
        
        fecha = datetime.datetime.now()

        
        
        


        # Definir anchos personalizados para las columnas (en puntos)
        column_widths_percentages_table = [11,11,11,11,11,11,11]  # La primera columna tiene 100 puntos de ancho, la segunda 50 puntos
        column_widths_percentages_info = [11,11,11,11,11,11,11]  # La primera columna tiene 100 puntos de ancho, la segunda 50 puntos


        # Calcular los anchos en puntos a partir de los porcentajes
        page_width, page_height = letter
        column_widths_points_table = [(width_percent * page_width) / 100 for width_percent in column_widths_percentages_table]





        with open(rutaClientes) as file:
            data = json.load(file)
            
        dataCliente = data["clientes"]
        
        
        infoCliente = {}
        for clientes in dataCliente:
            if clientes["nombre"] == cliente:
                infoCliente = clientes
        

        
        datosInfoCliente = []
        for datosCliente in infoCliente.items():
            datosInfoCliente.append(datosCliente[1])
            
        infoDatos = [[f"Nombre: {datosInfoCliente[0]}","","","","","",""],
                     [f"Apellidos: {datosInfoCliente[1]}","","","","","",""],
                     [f"Telefono: {datosInfoCliente[2]}","","","","","",""],
                     [f"Dni: {datosInfoCliente[3]}","","","","","",""],
                     [f"Fecha: {fecha.day}-{fecha.month}-{fecha.year}","","","","","",""],
                     [f"Direccion: {datosInfoCliente[4]}","","","","","",""]]
        
        
        
        
        print(cliente)
        # Crear la tabla y establecer los anchos de las columnas
        info = Table(infoDatos, colWidths=column_widths_points_table)

        espacio = [[" "," "," "," "," "," "," "]]

        espacioTable = Table(espacio,colWidths=column_widths_percentages_table)

        info.setStyle(TableStyle([#('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 8),
                                    #('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                                    #('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                                    #('GRID', (0, 0), (4, 1), 2, colors.black)
                                    ]))

        # Crear la tabla y establecer los anchos de las columnas
        
        table = Table(datos, colWidths=column_widths_points_table)

        #print(datos)

        table.setStyle(TableStyle([#('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 8),
                                    #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                                    #('GRID', (0, 0), (-1, len(datos)-4), 2, colors.black)
                                    ]))

        
        
        
        # Agregar un párrafo de texto        espacio = Spacer(1, 12)  
        
        story = []
        story.append(info)
        story.append(espacioTable)
        story.append(table)
        
       
        
        
        doc.build(story)

    def precioTotal(self):
        suma = 0
        for i in range(len(self.datosSuma)):
            if i != 0:
                datos = list(self.datosSuma[i])
                suma += int(datos[len(self.datosSuma[i])-1])
        return round(float(suma),2)


class pdfFactura:
    def __init__(self, cliente,ruta,datos,precioPresupuesto):
        
        fecha = datetime.datetime.now()

        nfactura = datos["nfactura"]
        nif = datos["nif"]
        termino = datos["termino"]
        nombre = datos["nombre"]
        direccion = datos["direccion"]
        postal = datos["postal"]
        text = datos["text"]
        
        rutaPrecio = "data/datos/precio.json"
        
        with open(rutaPrecio) as file:
            data = json.load(file)
        
        #cabezera
        datos = []
        datos2 = []
        datos.append(["----------------","","","","","","FACTURA"])
        datos.append(["-----","","","","","","",""])
        datos.append(["--------------","","","","","","",""])
        datos.append(["Teléfono:------","","","","","","N.º DE \n FACTURA","FECHA"])
        datos.append(["NIF ------","","","","","",f"{nfactura}",f"{fecha.day}/{fecha.month}/{fecha.year}"])
        datos.append(["----------@gmail.com","","","","","","",""])
        datos.append(["FACTURAR A","","","","","","NIF","TÉRMINOS"])
        datos.append([f"{nombre}","","","","","",f"{nif}",f"{termino}"])
        datos.append([f"{direccion}","","","","","","",""])
        datos.append([f"{postal}","","","","","","",""])
        
        
        datos2.append([f"{text}","","","","","","",""])
        
        
        
      
        precioFactura = []
        precio = precioPresupuesto
        precioIva = precio*0.21
        sumaPrecio = precio+precioIva
        
        
        precioFactura.append(["","BASE IMPONIBLE","","21% IVA","","SUMA TOTAL","",""])
        precioFactura.append(["",f"{precio}€","",f"{precioIva}€","",f"{round(float(sumaPrecio),2)}€","",""])
        rutaSplit = ruta.split("/")
        print(rutaSplit[len(rutaSplit)-1])
        self.generarPdf(cliente,ruta,datos,datos2,precioFactura)
        self.generarPdf(cliente,f"data/factura/{rutaSplit[len(rutaSplit)-1]}-{cliente}_{nfactura}",datos,datos2,precioFactura)
        #self.generarPdf(cliente,f"output/presupuesto_interno/{rutaSplit[4]}-{cliente}",datos)
        # Crear un objeto de estilo de párrafo para las celdas
        # Crear el documento PDF
    
    def generarPdf(self,cliente,ruta,datos,datos2,precioFactura):
        import reportlab.rl_config
        reportlab.rl_config.warnOnMissingFontGlyphs = 0

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfbase.ttfonts import TTFont
        
        from reportlab.pdfbase import pdfmetrics
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        import json
        rutaClientes = "data/datos/clientes.json"
        pdfmetrics.registerFont(TTFont('SwitzeraRegular', 'data/fuentes/SwitzeraADF-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraBold', 'data/fuentes/SwitzeraADF-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraLight', 'data/fuentes/SwitzeraADF-Light.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraMedium', 'data/fuentes/SwitzeraADF-Medium.ttf'))

        
        
        doc = SimpleDocTemplate(f"{ruta}.pdf", pagesize=letter)
        
        

        # Crear un estilo de párrafo personalizado con la fuente deseada
        
        
        

        
        
        


        # Definir anchos personalizados para las columnas (en puntos)
        column_widths_percentages_table = [39,1,1,1,1,12,15]  # La primera columna tiene 100 puntos de ancho, la segunda 50 puntos

        column_widths_percentages_precio = [8.75,8.75,8.75,8.75,8.75,8.75,8.75,8.75]

        # Calcular los anchos en puntos a partir de los porcentajes
        page_width, page_height = letter
        page_width2, page_height2 = letter
        column_widths_points_table = [(width_percent * page_width) / 100 for width_percent in column_widths_percentages_table]
        column_widths_points_precio =[(width_percent * page_width2) / 100 for width_percent in column_widths_percentages_precio]
        




        with open(rutaClientes) as file:
            data = json.load(file)
            
        dataCliente = data["clientes"]
        
        
        infoCliente = {}
        for clientes in dataCliente:
            if clientes["nombre"] == cliente:
                infoCliente = clientes
        

        
        datosInfoCliente = []
        for datosCliente in infoCliente.items():
            datosInfoCliente.append(datosCliente[1])
            
        
        
        print(cliente)
        # Crear la tabla y establecer los anchos de las columnas
        
        espacio = [[" "," "," "," "," "," "," "]]

        espacioTable = Table(espacio,colWidths=column_widths_percentages_table)

        # Crear la tabla y establecer los anchos de las columnas
        
        table = Table(datos, colWidths=column_widths_points_table)
        table2 = Table(datos2, colWidths=column_widths_points_table)
        
        tabalFactura = Table(precioFactura, colWidths=column_widths_points_precio)


        #print(datos)

        table.setStyle(TableStyle([#('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 1), (0, 5), colors.black),
                                    ('TEXTCOLOR', (0, 5), (7, 5), colors.black),
                                    ('TEXTCOLOR', (6, 3), (7, 3), colors.white),
                                    ('TEXTCOLOR', (0, 0), (7, 0), "#3b5fa1"),
                                    ('BACKGROUND', (6, 3), (7, 3), "#3b5fa1"),
                                    ('BACKGROUND', (6, 6), (7, 6), "#3b5fa1"),
                                    ('BACKGROUND', (0, 6), (4, 6), "#3b5fa1"),
                                    ('TEXTCOLOR', (0, 6), (7, 6), colors.white),
                                    ('ALIGN', (0, 0), (0, 5), 'LEFT'),
                                    ('ALIGN', (4, 3), (7, 4), 'CENTER'),
                                    ('ALIGN', (6,6), (7, 7), 'CENTER'),
                                    ('VALIGN', (0, 3), (7, 3), 'MIDDLE'),
                                    ('FONT', (0, 1), (-1, -1), 'SwitzeraMedium', 8),
                                    ('FONT', (6, 0), (6, 0), 'SwitzeraLight', 24),
                                    ('FONT', (0, 0), (0, 0), 'SwitzeraLight', 18),
                                    #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    #('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                                    #('GRID', (0, 0), (-1, len(datos)-4), 2, colors.black)
                                    ]))
        
        table2.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('FONT', (0, 0), (-1, -1), 'SwitzeraLight', 8),
                                    ('ALIGN',(0,0),(-1,-1), "LEFT")
                                    ]))
        
        tabalFactura.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('FONT', (0, 0), (-1, -1), 'SwitzeraMedium', 8),
                                    ('ALIGN',(0,0),(-1,-1), "CENTER")
                                    ]))
        
        
            
        
        story = []
        story.append(table)
        for i in range(3):
            story.append(espacioTable)
        
        
        story.append(table2)
        for i in range(3):
            story.append(espacioTable)
        
        story.append(tabalFactura)
        
        doc.build(story)




class pdfPresupuesto:
    def __init__(self, cliente,ruta,datos,precioPresupuesto):
        import datetime
        import json
        fecha = datetime.datetime.now()

        nfactura = datos["npresupuesto"]
        nombre = datos["nombre"]
        direccion = datos["direccion"]
        postal = datos["postal"]
        text = datos["text"]
        
        rutaPrecio = "data/datos/precio.json"
        
        with open(rutaPrecio) as file:
            data = json.load(file)
        
        #cabezera
        datos = []
        datos2 = []
        datos.append(["-----------------","","","","","","Presupuesto"])
        datos.append(["---------","","","","","","",""])
        datos.append(["------------------","","","","","","",""])
        datos.append(["Teléfono: ----------","","","","","","N.º DE \n PRESUPUESTO","FECHA"])
        datos.append(["NIF --------","","","","","",f"{nfactura}",f"{fecha.day}/{fecha.month}/{fecha.year}"])
        datos.append(["---------0@gmail.com","","","","","","",""])
        datos.append(["FACTURAR A","","","","","","",""])
        datos.append([f"{nombre}","","","","","","",""])
        datos.append([f"{direccion}","","","","","","",""])
        datos.append([f"{postal}","","","","","","",""])
        
        
        datos2.append([f"{text}","","","","","","",""])
        
        
        
      
        precioFactura = []
        precio = precioPresupuesto
        precioIva = precio*0.21
        sumaPrecio = precio+precioIva
        
        
        precioFactura.append([f"MANO DE OBRA MAS MATERIALES.................{precio}€","","","","","","",""])
        precioFactura.append(["","","","","","","",""])
        precioFactura.append(["","","","","","","",""])
        precioFactura.append(["","","","","","","",""])
        precioFactura.append(["","","","","","","",""])
        precioFactura.append([f"21% IVA NO INCLUIDO EN ESTE PRESUPUESTO","","","","","","",""])
        rutaSplit = ruta.split("/")
        print(rutaSplit[len(rutaSplit)-1])
        self.generarPdf(cliente,ruta,datos,datos2,precioFactura)
        self.generarPdf(cliente,f"data/presupuesto/{rutaSplit[len(rutaSplit)-1]}-{cliente}_{fecha.day}-{fecha.month}-{fecha.year}",datos,datos2,precioFactura)
        #self.generarPdf(cliente,f"output/presupuesto_interno/{rutaSplit[4]}-{cliente}",datos)
        # Crear un objeto de estilo de párrafo para las celdas
        # Crear el documento PDF
    
    def generarPdf(self,cliente,ruta,datos,datos2,precioFactura):
        import reportlab.rl_config
        reportlab.rl_config.warnOnMissingFontGlyphs = 0

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfbase.ttfonts import TTFont
        
        from reportlab.pdfbase import pdfmetrics
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        import json
        rutaClientes = "data/datos/clientes.json"
        pdfmetrics.registerFont(TTFont('SwitzeraRegular', 'data/fuentes/SwitzeraADF-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraBold', 'data/fuentes/SwitzeraADF-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraLight', 'data/fuentes/SwitzeraADF-Light.ttf'))
        pdfmetrics.registerFont(TTFont('SwitzeraMedium', 'data/fuentes/SwitzeraADF-Medium.ttf'))

        
        
        doc = SimpleDocTemplate(f"{ruta}.pdf", pagesize=letter)
        
        

        # Crear un estilo de párrafo personalizado con la fuente deseada
        
        
        

        
        
        


        # Definir anchos personalizados para las columnas (en puntos)
        column_widths_percentages_table = [39,1,1,1,1,12,15]  # La primera columna tiene 100 puntos de ancho, la segunda 50 puntos

        column_widths_percentages_precio = [8.75,8.75,8.75,8.75,8.75,8.75,8.75,8.75]

        # Calcular los anchos en puntos a partir de los porcentajes
        page_width, page_height = letter
        page_width2, page_height2 = letter
        column_widths_points_table = [(width_percent * page_width) / 100 for width_percent in column_widths_percentages_table]
        column_widths_points_precio =[(width_percent * page_width2) / 100 for width_percent in column_widths_percentages_precio]
        




        with open(rutaClientes) as file:
            data = json.load(file)
            
        dataCliente = data["clientes"]
        
        
        infoCliente = {}
        for clientes in dataCliente:
            if clientes["nombre"] == cliente:
                infoCliente = clientes
        

        
        datosInfoCliente = []
        for datosCliente in infoCliente.items():
            datosInfoCliente.append(datosCliente[1])
            
        
        
        print(cliente)
        # Crear la tabla y establecer los anchos de las columnas
        
        espacio = [[" "," "," "," "," "," "," "]]

        espacioTable = Table(espacio,colWidths=column_widths_percentages_table)

        # Crear la tabla y establecer los anchos de las columnas
        
        table = Table(datos, colWidths=column_widths_points_table)
        table2 = Table(datos2, colWidths=column_widths_points_table)
        
        tabalFactura = Table(precioFactura, colWidths=column_widths_points_table)


        #print(datos)

        table.setStyle(TableStyle([#('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 1), (0, 5), colors.black),
                                    ('TEXTCOLOR', (0, 5), (7, 5), colors.black),
                                    ('TEXTCOLOR', (6, 3), (7, 3), colors.white),
                                    ('TEXTCOLOR', (0, 0), (7, 0), "#3b5fa1"),
                                    ('BACKGROUND', (6, 3), (7, 3), "#3b5fa1"),
                                    
                                    ('BACKGROUND', (0, 6), (4, 6), "#3b5fa1"),
                                    ('TEXTCOLOR', (0, 6), (7, 6), colors.white),
                                    ('ALIGN', (0, 0), (0, 5), 'LEFT'),
                                    ('ALIGN', (4, 3), (7, 4), 'CENTER'),
                                    ('ALIGN', (6,6), (7, 7), 'CENTER'),
                                    ('VALIGN', (0, 3), (7, 3), 'MIDDLE'),
                                    ('FONT', (0, 1), (-1, -1), 'SwitzeraMedium', 8),
                                    ('FONT', (6, 0), (6, 0), 'SwitzeraLight', 24),
                                    ('FONT', (0, 0), (0, 0), 'SwitzeraLight', 18),
                                    #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    #('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                                    #('GRID', (0, 0), (-1, len(datos)-4), 2, colors.black)
                                    ]))
        
        table2.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('FONT', (0, 0), (-1, -1), 'SwitzeraLight', 8),
                                    ('ALIGN',(0,0),(-1,-1), "LEFT")
                                    ]))
        
        tabalFactura.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                    ('FONT', (0, 0), (-1, -1), 'SwitzeraMedium', 8),
                                    ('ALIGN',(0,0),(-1,-1), "CENTER")
                                    ]))
        
        
            
        
        story = []
        story.append(table)
        for i in range(3):
            story.append(espacioTable)
        
        
        story.append(table2)
        for i in range(3):
            story.append(espacioTable)
        
        story.append(tabalFactura)
        
        doc.build(story)



