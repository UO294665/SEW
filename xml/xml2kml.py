import xml.etree.ElementTree as ET

class Kml(object):
    """
    Genera archivo KML con puntos y líneas
    @version 1.1 19/Octumbre/2024
    @author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
    """
    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz,'Document')

    def addPlacemark(self,nombre,descripcion,long,lat,alt, modoAltitud):
        """
        Añade un elemento <Placemark> con puntos <Point>
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud

    def addLineString(self,nombre,extrude,tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement (linea, 'color').text = color
        ET.SubElement (linea, 'width').text = ancho

    def escribir(self,nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)
    
    def ver(self):
        """
        Muestra el archivo KML. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text != None:
            print("Contenido = "    , self.raiz.text.strip('\n'))
        else:
            print("Contenido = "    , self.raiz.text)
        
        print("Atributos = "    , self.raiz.attrib)

        for hijo in self.raiz.findall('.//'):
            print("\nElemento = " , hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n'))
            else:
                print("Contenido = ", hijo.text)    
            print("Atributos = ", hijo.attrib)


def main():
    """
    Programa principal que lee circuitoEsquema.xml y genera circuito.kml
    """
    # Leer el archivo XML y generar el árbol DOM
    arbol = ET.parse('xml/circuitoEsquema.xml')
    raiz = arbol.getroot()
    
    # Definir el namespace del XML
    namespaces = {'ns': 'http://www.uniovi.es'}

    # Crear lista de coordenadas para la línea del circuito
    listaCoordenadas = []
    
    # Crear objeto KML
    kml = Kml()

    # Guardar las coordenadas del origen (primer punto)
    origen = raiz.find('.//ns:origen', namespaces)
    longitud_origen = origen.find('.//ns:longitud', namespaces).text
    latitud_origen = origen.find('.//ns:latitud', namespaces).text
    altitud_origen = origen.find('.//ns:altitud', namespaces).text

    kml.addPlacemark(
        nombre='Origen',
        descripcion='Punto de inicio del circuito',
        long=longitud_origen,
        lat=latitud_origen,
        alt=altitud_origen,
        modoAltitud='relativeToGround'
    )

    listaCoordenadas.append(f"{longitud_origen},{latitud_origen},{altitud_origen}")
    
    # Extraer coordenadas usando XPath
    # Obtener todos los tramos del circuito
    tramos = raiz.findall('.//ns:tramos/ns:tramo', namespaces)

    # Procesar cada tramo usando expresiones XPath
    for i, tramo in enumerate(tramos, 1):
        # Usar XPath para extraer las coordenadas
        longitud = tramo.find('.//ns:coordenadas/ns:longitud', namespaces).text
        latitud = tramo.find('.//ns:coordenadas/ns:latitud', namespaces).text
        altitud = tramo.find('.//ns:coordenadas/ns:altitud', namespaces).text
        distancia = tramo.find('.//ns:distancia', namespaces).text
        sector = tramo.find('.//ns:sector', namespaces).text
        
        # Añadir un Placemark (punto) para cada tramo
        nombre = f"Tramo {i}"
        descripcion = f"Sector {sector}, Distancia: {distancia}m"
        kml.addPlacemark(nombre, descripcion, longitud, latitud, altitud, 'relativeToGround')
        
        # Añadir coordenadas a la lista para el LineString
        listaCoordenadas.append(f"{longitud},{latitud},{altitud}")
    
    # Cerrar el circuito añadiendo de nuevo el punto de origen al final
    listaCoordenadas.append(f"{longitud_origen},{latitud_origen},{altitud_origen}")

    # Crear el LineString con todas las coordenadas del circuito
    coordenadasLinea = ' '.join(listaCoordenadas)
    kml.addLineString(
        nombre='Circuito',
        extrude='1',
        tesela='1',
        listaCoordenadas=coordenadasLinea,
        modoAltitud='relativeToGround',
        color='ff0000ff',  # Rojo en formato ABGR
        ancho='5'
    )
    
    # Escribir el archivo KML en la carpeta xml
    kml.escribir('xml/circuito.kml')
    
    print("Archivo xml/circuito.kml generado correctamente")
    
    # Opcional: mostrar el contenido para depuración
    # kml.ver()


if __name__ == "__main__":
    main()