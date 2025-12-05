import xml.etree.ElementTree as ET

class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    @version 1.0 18/Octubre/2024
    @author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
    """
    def __init__(self):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")

    
    def addRect(self,x,y,width,height,fill, strokeWidth,stroke):
        """
        Añade un elemento rect
        """
        ET.SubElement(self.raiz,'rect',
                      x=x,
                      y=y,
                      width=width,
                      height=height,
                      fill=fill, 
                      strokeWidth=strokeWidth,
                      stroke=stroke)
        
    def addCircle(self,cx,cy,r,fill):
        """
        Añade un elemento circle
        """
        ET.SubElement(self.raiz,'circle',
                      cx=cx,
                      cy=cy,
                      r=r,
                      fill=fill)
        
    def addLine(self,x1,y1,x2,y2,stroke,strokeWith):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz,'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      strokeWith=strokeWith)

    def addPolyline(self,points,stroke,strokeWith,fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz,'polyline',
                      points=points,
                      stroke=stroke,
                      strokeWith=strokeWith,
                      fill=fill)
        
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz,'text',
                      x=x,
                      y=y,
                      fontFamily=fontFamily,
                      fontSize=fontSize,
                      style=style).text=texto

    def escribir(self,nombreArchivoSVG):
        """
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        
        arbol.write(nombreArchivoSVG, 
                    encoding='utf-8', 
                    xml_declaration=True
                    )
    
    def ver(self):
        """
        Muestra el archivo SVG. Se utiliza para depurar
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

    print("Generación de SVG: Perfil Altimétrico del Circuito")

    # Leer archivo XML
    arbol = ET.parse('xml/circuitoEsquema.xml')
    raiz = arbol.getroot()
    namespaces = {'ns': 'http://www.uniovi.es'}

    # Crear objeto SVG
    svg = Svg()

    # Obtener altitud origen
    origen = raiz.find('.//ns:origen', namespaces)
    altitud_origen = float(origen.find('.//ns:altitud', namespaces).text)

    # Obtener tramos
    tramos = raiz.findall('.//ns:tramos/ns:tramo', namespaces)

    # Listas de distancias y altitudes
    distancias = [0]
    altitudes = [altitud_origen]
    distancia_acumulada = 0

    for tramo in tramos:
        distancia = float(tramo.find('.//ns:distancia', namespaces).text)
        altitud = float(tramo.find('.//ns:coordenadas/ns:altitud', namespaces).text)
        distancia_acumulada += distancia
        distancias.append(distancia_acumulada)
        altitudes.append(altitud)


    # Dimensiones del SVG
    margen = 50
    ancho_grafico = 1000
    alto_grafico = 400
    ancho_total = ancho_grafico + 2 * margen
    alto_total = alto_grafico + 2 * margen

    # Atributo width y height para el SVG
    svg.raiz.set('width', str(ancho_total))
    svg.raiz.set('height', str(alto_total))

    # Fondo blanco
    svg.addRect('0', '0', str(ancho_total), str(alto_total), 'white', '0', 'none')

    # Rectángulo del área del gráfico (borde negro)
    svg.addRect(str(margen), str(margen), str(ancho_grafico), str(alto_grafico), 
                'lightblue', '2', 'black')

    # Escalas
    escala_x = ancho_grafico / max(distancias)
    rango_altitud = max(altitudes) - min(altitudes)
    if rango_altitud == 0:
        rango_altitud = 1
    escala_y = alto_grafico / rango_altitud

    # Crear puntos polilínea
    puntos = []
    for i in range(len(distancias)):
        x = margen + distancias[i] * escala_x
        y = margen + alto_grafico - (altitudes[i] - min(altitudes)) * escala_y
        puntos.append(f"{x},{y}")
    puntos_str = ' '.join(puntos)

    # Añadir polilínea roja sin relleno
    svg.addPolyline(puntos_str, 'red', '3', 'none')

    # Añadir título
    svg.addText('Perfil Altimétrico del Circuito', 
                str(ancho_total // 2), '30', 
                'Arial', '20', 'text-anchor:middle;font-weight:bold')

    # Añadir etiquetas de ejes
    svg.addText('Distancia (m)', 
                str(ancho_total // 2), str(alto_total - 10), 
                'Arial', '14', 'text-anchor:middle')
    
    svg.addText('Altitud (m)', 
                '15', str(alto_total // 2), 
                'Arial', '14', 'text-anchor:middle;writing-mode:tb')

    # Añadir valores en las esquinas del gráfico
    svg.addText('0', str(margen - 5), str(margen + alto_grafico + 15), 
                'Arial', '12', 'text-anchor:end')
    
    svg.addText(f'{int(max(distancias))}', 
                str(margen + ancho_grafico + 5), str(margen + alto_grafico + 15), 
                'Arial', '12', 'text-anchor:start')
    
    svg.addText(f'{int(min(altitudes))}', 
                str(margen - 5), str(margen + alto_grafico + 5), 
                'Arial', '12', 'text-anchor:end')
    
    svg.addText(f'{int(max(altitudes))}', 
                str(margen - 5), str(margen + 5), 
                'Arial', '12', 'text-anchor:end')

    # Escribir SVG
    nombreSVG = 'xml/altimetria.svg'
    svg.escribir(nombreSVG)

    print(f"Archivo {nombreSVG} generado correctamente")
    print(f"Distancia total: {int(max(distancias))}m")
    print(f"Altitud máxima: {int(max(altitudes))}m")
    print(f"Altitud mínima: {int(min(altitudes))}m")
    print(f"Número de tramos: {len(tramos)}")

if __name__ == "__main__":
    main()