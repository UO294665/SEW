class Cronometro {
    constructor() {
        this.tiempo = 0;
        this.mostrar();
    }

    arrancar() {
        try {
            this.inicio = Temporal.Now.instant();
        } catch (error) {
            this.inicio = new Date();
        }

        this.corriendo = setInterval(this.actualizar.bind(this), 100);
    }

    actualizar() {
        let actual;
        try {
            actual = Temporal.Now.instant();
            this.tiempo = actual.epochMilliseconds - this.inicio.epochMilliseconds;
        } catch (error) {
            actual = new Date();
            this.tiempo = actual.getTime() - this.inicio.getTime();
        }
        this.mostrar();
    }

    mostrar(){
        const parrafo = document.querySelector("main p");

        const minutos = parseInt(this.tiempo / 60000);
        const segundos = parseInt((this.tiempo % 60000) / 1000);
        const decimas = parseInt((this.tiempo % 1000) / 100);

        const minutosTexto = String(minutos).padStart(2, "0");
        const segundosTexto = String(segundos).padStart(2, "0");

        parrafo.textContent = minutosTexto + ":" + segundosTexto + "." + decimas;
    }

    parar() {
        clearInterval(this.corriendo);
    }

    reiniciar() {
        clearInterval(this.corriendo);
        this.tiempo = 0;
        this.mostrar();
    }
    
}