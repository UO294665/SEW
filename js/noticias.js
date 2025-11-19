class Noticias{
    constructor(){
        this.busqueda;
        this.url = "https://api.thenewsapi.com/v1/news/all";
        this.api_token = "7qpLZAPWFn1fxEAlAMHBQM7sNnN31iJ29XJtMm2g";
    }

    procesarInformacion(){
        for(let i=0; i< this.busqueda.length; i++){
            this.titulo = this.busqueda[i].title;
            this.description = this.busqueda[i].description;
            this.urlNoticia = this.busqueda[i].url;
            this.source = this.busqueda[i].source;
            this.mostrarNoticia();
        }
    }

    mostrarNoticia(){
        const $section = $("<section></section>");
        const $titulo = $("<h3></h3>").text(this.titulo);
        const $descripcion = $("<p></p>").text(this.description);
        const $source = $("<p></p>").text("Fuente: " + this.source);
        const $enlace = $("<a></a>").attr("href", this.urlNoticia).text("Leer más");

        $section.append($titulo);
        $titulo.after($descripcion);
        $descripcion.after($source);
        $source.after($enlace);
        $("body > main").append($section);
    }

    async buscar() {

        const url = `${this.url}?api_token=${this.api_token}&search=MotoGP&language=es`;

        try {
            const respuesta = await fetch(url);
            if (!respuesta.ok) throw new Error('Error en el proceso de consulta de noticias');
            const datos = await respuesta.json();
            this.busqueda = datos.data;
            this.procesarInformacion();
        } catch (error) {
        }
    }
}
