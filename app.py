from pathlib import Path

from flask import Flask, abort, render_template

app = Flask(__name__)


SERVICIOS = {
    "levantamientos-topograficos": {
        "titulo": "Levantamientos topográficos",
        "descripcion": (
            "Realizamos levantamientos precisos de terrenos, predios, "
            "construcciones y superficies utilizando equipo topográfico."
        ),
        "carpeta": "levantamientos",
    },
    "proyectos-arquitectonicos": {
        "titulo": "Proyectos arquitectónicos",
        "descripcion": (
            "Diseñamos viviendas, departamentos, ampliaciones, "
            "remodelaciones y espacios funcionales."
        ),
        "carpeta": "proyectos-arquitectonicos",
    },
    "replanteos": {
        "titulo": "Replanteos",
        "descripcion": (
            "Replanteo de parcelas ejidales ligadas a la Red Geodésica "
            "Nacional Pasiva."
        ),
        "carpeta": "replanteos",
    },
    "consultoria-de-proyectos": {
        "titulo": "Consultoría de proyectos",
        "descripcion": (
            "Brindamos asesoría para la planeación e integración de "
            "expedientes técnicos, así como para su validación ante "
            "distintas áreas y dependencias."
        ),
        "carpeta": "consultoria",
    },
    "manifiestos-de-impacto-ambiental": {
        "titulo": "Manifiestos de impacto ambiental",
        "descripcion": (
            "Elaboramos estudios y manifiestos de impacto ambiental "
            "para proyectos públicos y privados."
        ),
        "carpeta": "impacto-ambiental",
    },
    "obras-publicas": {
        "titulo": "Obras públicas",
        "descripcion": (
            "Participamos en trabajos de pavimentación, drenaje, banquetas, "
            "infraestructura y mejoramiento urbano."
        ),
        "carpeta": "obras-publicas",
    },
}


EXTENSIONES_PERMITIDAS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".jfif",
    ".avif",
}


def obtener_imagenes(carpeta_servicio):
    """
    Busca automáticamente las imágenes dentro de:

    static/img/trabajos/NOMBRE_DE_LA_CARPETA/

    También muestra información en la terminal para detectar
    problemas con rutas, nombres o extensiones.
    """

    ruta_carpeta = (
        Path(app.root_path)
        / "static"
        / "img"
        / "trabajos"
        / carpeta_servicio
    )

    print("\n========================================")
    print("SERVICIO:", carpeta_servicio)
    print("RUTA BUSCADA:", ruta_carpeta)
    print("¿EXISTE LA CARPETA?:", ruta_carpeta.exists())

    if not ruta_carpeta.exists():
        print("ERROR: La carpeta no existe.")
        print("Revisa que esté escrita y ubicada correctamente.")
        print("========================================\n")
        return []

    imagenes = []

    for archivo in ruta_carpeta.iterdir():
        print(
            "ARCHIVO ENCONTRADO:",
            archivo.name,
            "| EXTENSIÓN:",
            archivo.suffix.lower(),
            "| ¿ES ARCHIVO?:",
            archivo.is_file(),
        )

        if not archivo.is_file():
            continue

        if archivo.suffix.lower() not in EXTENSIONES_PERMITIDAS:
            print(
                "ARCHIVO IGNORADO POR EXTENSIÓN NO PERMITIDA:",
                archivo.name,
            )
            continue

        ruta_relativa = (
            Path("img")
            / "trabajos"
            / carpeta_servicio
            / archivo.name
        )

        imagenes.append(ruta_relativa.as_posix())

    imagenes = sorted(
        imagenes,
        key=lambda imagen: imagen.lower(),
    )

    print("IMÁGENES ACEPTADAS:", imagenes)
    print("TOTAL DE IMÁGENES:", len(imagenes))
    print("========================================\n")

    return imagenes


@app.route("/")
def inicio():
    return render_template(
        "index.html",
        servicios=SERVICIOS,
    )


@app.route("/empresa")
def empresa():
    return render_template("empresa.html")


@app.route("/servicio/<slug>")
def servicio(slug):
    datos = SERVICIOS.get(slug)

    if datos is None:
        abort(404)

    imagenes = obtener_imagenes(datos["carpeta"])

    return render_template(
        "servicio.html",
        servicio=datos,
        imagenes=imagenes,
        slug=slug,
    )


if __name__ == "__main__":
    app.run(debug=True)