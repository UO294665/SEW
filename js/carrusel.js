class Carrusel{
    constructor(){
        this.busqueda = [];
        this.actual = 0;
        this.maximo = 5;
        this.getFotografias();
    }

    getFotografias(){

        $.ajax({
            dataType:"json",
            url: "https://api.flickr.com/services/feeds/photos_public.gne?format=json&tags=motoGP&jsoncallback=?",
            method: "GET",
            success: (datos) => {
                this.procesarJSONFotografias(datos);
            }

        });
    }

    procesarJSONFotografias(datos){
        for(let i = 0; i < this.maximo; i++){
            let fotografia = datos.items[i];
            fotografia = fotografia.media.m.replace("_m.","_z.");
            this.busqueda.push(fotografia);
        }
        this.mostrarFotografias();
    }

    mostrarFotografias(){
        const $articulo = $("<article></article>");
        const $titulo = $("<h2>Imágenes del circuito de Sepang</h2>");
        const $imagen = $(`<img src="${this.busqueda[0]}" alt="Imagen del circuito Sepang">`);

        $articulo.append($titulo);
        $titulo.after($imagen);
        $('body > main').append($articulo);

        setInterval(this.cambiarFotografia.bind(this), 3000);
        
        var n = new Noticias();
        n.buscar();
    }

    cambiarFotografia(){
        this.actual++;
        if(this.actual >= this.maximo){
            this.actual = 0;
        }
        $("article img").attr("src", this.busqueda[this.actual]);
    }

}