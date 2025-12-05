import xml.etree.ElementTree as ET

class Html(object):
    """
    Genera archivo HTML a partir de un archivo XML de circuito
    @version 1.0 28/Noviembre/2024
    @author: Conversión XML a HTML para MotoGP
    """
    
    def __init__(self, xml_file):
        """
        Constructor de la clase Html
        Lee y parsea el archivo XML del circuito
        """
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.ns = {'ns': 'http://www.uniovi.es'}
        self.html = ET.Element('html', lang='es')
        self.head = ET.SubElement(self.html, 'head')
        self.body = ET.SubElement(self.html, 'body')
        
    def addMetaData(self, titulo, css_file='estilo.css'):
        """
        Añade metadatos, título y enlace CSS al head
        """
        ET.SubElement(self.head, 'meta', charset='UTF-8')
        ET.SubElement(self.head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
        nombre = self.root.find('.//ns:circuito/ns:nombre', self.ns).text
        ET.SubElement(self.head, 'meta', name='description', content=f'Información del circuito {nombre}')
        ET.SubElement(self.head, 'meta', name='keywords', content='MotoGP, circuito, carreras')
        ET.SubElement(self.head, 'meta', name='author', content='xml2html.py')
        ET.SubElement(self.head, 'title').text = titulo
        ET.SubElement(self.head, 'link', rel='stylesheet', href=css_file)
    
    def addHeader(self, titulo):
        """
        Añade un header con título h1
        """
        header = ET.SubElement(self.body, 'header')
        ET.SubElement(header, 'h1').text = titulo
    
    def addArticle(self):
        """
        Crea y añade todas las secciones del circuito
        """
        main = ET.SubElement(self.body, 'main')
        article = ET.SubElement(main, 'article')
        
        nombre = self.root.find('.//ns:circuito/ns:nombre', self.ns).text
        ET.SubElement(article, 'h2').text = nombre
        
        self._addDatosGenerales(article)
        self._addResultados(article)
        self._addClasificacion(article)
        self._addReferencias(article)
        self._addFotografias(article)
        self._addVideos(article)
    
    def _addDatosGenerales(self, article):
        """Añade sección de datos generales"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Datos Generales'
        dl = ET.SubElement(section, 'dl')
        
        datos = [
            ('Nombre:', './/ns:circuito/ns:nombre'),
            ('Localidad:', './/ns:circuito/ns:localidad'),
            ('País:', './/ns:circuito/ns:pais'),
            ('Patrocinador:', './/ns:circuito/ns:patrocinador'),
            ('Número de Vueltas:', './/ns:circuito/ns:vueltas'),
            ('Fecha:', './/ns:circuito/ns:fecha'),
            ('Hora:', './/ns:circuito/ns:hora')
        ]
        
        for etiqueta, xpath in datos:
            ET.SubElement(dl, 'dt').text = etiqueta
            ET.SubElement(dl, 'dd').text = self.root.find(xpath, self.ns).text
        
        # Longitud y anchura con unidades
        ET.SubElement(dl, 'dt').text = 'Longitud del Circuito:'
        long_elem = self.root.find('.//ns:circuito/ns:longitud_circuito', self.ns)
        ET.SubElement(dl, 'dd').text = f'{long_elem.text} {long_elem.get("unidad")}'
        
        ET.SubElement(dl, 'dt').text = 'Anchura:'
        anch_elem = self.root.find('.//ns:circuito/ns:anchura', self.ns)
        ET.SubElement(dl, 'dd').text = f'{anch_elem.text} {anch_elem.get("unidad")}'
    
    def _addResultados(self, article):
        """Añade sección de resultados"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Resultados de la Carrera'
        dl = ET.SubElement(section, 'dl')
        
        ET.SubElement(dl, 'dt').text = 'Vencedor:'
        ET.SubElement(dl, 'dd').text = self.root.find('.//ns:circuito/ns:vencedor', self.ns).text
        
        ET.SubElement(dl, 'dt').text = 'Tiempo de Carrera:'
        ET.SubElement(dl, 'dd').text = self.root.find('.//ns:circuito/ns:tiempo_carrera', self.ns).text
    
    def _addClasificacion(self, article):
        """Añade sección de clasificación"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Clasificación'
        ol = ET.SubElement(section, 'ol')
        
        pilotos = self.root.findall('.//ns:circuito/ns:clasificacion/ns:piloto', self.ns)
        for piloto in pilotos:
            li = ET.SubElement(ol, 'li', value=piloto.get('posicion'))
            li.text = piloto.text
    
    def _addReferencias(self, article):
        """Añade sección de referencias"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Referencias'
        ul = ET.SubElement(section, 'ul')
        
        referencias = self.root.findall('.//ns:circuito/ns:referencias/ns:referencia', self.ns)
        for ref in referencias:
            li = ET.SubElement(ul, 'li')
            a = ET.SubElement(li, 'a', href=ref.text, target='_blank', rel='noopener noreferrer')
            a.text = ref.text
    
    def _addFotografias(self, article):
        """Añade sección de fotografías"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Fotografías'
        ul = ET.SubElement(section, 'ul')
        
        fotos = self.root.findall('.//ns:circuito/ns:fotografias/ns:fotografia', self.ns)
        for foto in fotos:
            ET.SubElement(ul, 'li').text = foto.text
    
    def _addVideos(self, article):
        """Añade sección de videos"""
        section = ET.SubElement(article, 'section')
        ET.SubElement(section, 'h3').text = 'Videos'
        ul = ET.SubElement(section, 'ul')
        
        videos = self.root.findall('.//ns:circuito/ns:videos/ns:video', self.ns)
        for video in videos:
            ET.SubElement(ul, 'li').text = video.text
    
    def addFooter(self, texto):
        """Añade footer al body"""
        footer = ET.SubElement(self.body, 'footer')
        ET.SubElement(footer, 'p').text = texto
    
    def escribir(self, nombreArchivoHTML):
        """Escribe el archivo HTML con DOCTYPE y codificación UTF-8"""
        arbol = ET.ElementTree(self.html)
        ET.indent(arbol, space='    ')
        arbol.write(nombreArchivoHTML, encoding='utf-8', xml_declaration=False)
        
        with open(nombreArchivoHTML, 'r', encoding='utf-8') as f:
            contenido = f.read()
        with open(nombreArchivoHTML, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n' + contenido)
        
        print(f"Archivo {nombreArchivoHTML} generado correctamente")
    
    def ver(self):
        """Muestra el archivo HTML para depuración"""
        print("\nElemento raiz =", self.html.tag)
        print("Contenido =", self.html.text.strip('\n') if self.html.text else self.html.text)
        print("Atributos =", self.html.attrib)
        
        for hijo in self.html.findall('.//'):
            print("\nElemento =", hijo.tag)
            print("Contenido =", hijo.text.strip('\n') if hijo.text else hijo.text)
            print("Atributos =", hijo.attrib)


def main():
    """
    Función principal - Genera InfoCircuito.html desde circuitoEsquema.xml
    """
    try:
        miHtml = Html('xml/circuitoEsquema.xml')
        
        nombre = miHtml.root.find('.//ns:circuito/ns:nombre', miHtml.ns).text
        miHtml.addMetaData(f'Información del Circuito - {nombre}')
        miHtml.addHeader('Información del Circuito')
        miHtml.addArticle()
        miHtml.addFooter('Generado automáticamente desde circuitoEsquema.xml')
        miHtml.escribir('xml/InfoCircuito.html')
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo circuitoEsquema.xml")
    except ET.ParseError:
        print("Error: El archivo XML no tiene un formato válido")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")


if __name__ == "__main__":
    main()