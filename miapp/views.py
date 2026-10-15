from django.http import HttpResponse
from django.shortcuts import render, redirect
from miapp.models import Article, Category

# Create your views here.
# MVC = Modelo  Vista   Controlador -> Acciones (metodos)
# MVT = Modelo  Vista   Template    -> Acciones (metodos)

layout = """
<h1>Sitio WEB con Django    |   ADSO SENA</h1>
<hr>
<ul>
    <li>
        <a href="/inicio">Inicio</a>
    </li>
    <li>
        <a href="/hola_mundo">Hola Mundo</a>
    </li>
    <li>
        <a href="/pagina">Pagina de pruebas</a>
    </li>
    <li>
        <a href="/contacto">Contacto</a>
    </li>
</ul>
<hr>
"""

def index(request):

    html = """
    <h1>Inicio</h1>
    <p>Años hasta el 2050: </p>
    <ul>
    """
    year = 2026
    while year <= 2050:
        if year % 2 == 0:
            html += f"<li>{year}</li>"
        year += 1

    html += "</ul>"
    nombre = 'Jonny Chilito'
    lenguajes = ['Python', 'JavaScript', 'C#', 'Java', 'PHP']

    return render(request, 'index.html', {
        'title': 'Inicio',
        'mi_variable': "Soy un dato que esta en la vista",
        'nombre': nombre,
        'lenguajes': lenguajes,
    })

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

def pagina(request, redirigir=0):

    if redirigir == 1:
        return redirect('/inicio/')


    return render(request, 'pagina.html')

def contacto(request, nombre="", apellido=""):

    html = ""
    if nombre and apellido:
        html += "<p>El nombre completo es:</p>"
        html += f"<h3>{nombre} {apellido}</h3>"

    return HttpResponse(layout + f"<h2>Contacto</h2>" + html)

def crear_articulo(request, title, content, public):
    articulo = Article(
        title= title,
        content= content,
        public= public
    )
    articulo.save()
    return HttpResponse(f"Artículo creado: <strong>{articulo.title} - {articulo.content}</strong>")

def articulo(request):
    try:
        articulo = Article.objects.get(id=4)
        response = (f"Artículo: {articulo.title} - {articulo.content}")
    except:
        response = ("Artículo no encontrado o no es público")
    return HttpResponse(response)

def editar_articulo(request, id):
    articulo = Article.objects.get(pk=id)

    articulo.title = "Batman"
    articulo.content = "Pelicula del 2017"
    articulo.public = True

    articulo.save()

    return HttpResponse(f"Artículo editado: <strong>{articulo.title} - {articulo.content}</strong>")

def articulos(request):
    articulos = Article.objects.all()

    articulos = Article.objects.filter(title__contains="articulo")

    articulos = Article.objects.filter(title="Articulo", public=False)

    articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title='Articulo' AND public=0")

    return render(request, 'articulos.html', {
        'articulos': articulos
    })

def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()

    return redirect('articulos')