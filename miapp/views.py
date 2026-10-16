from django.http import HttpResponse
from django.shortcuts import render, redirect
from miapp.models import Article, Category
from miapp.forms import FormArticle
from django.contrib import messages

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
    articulo.save() #para guardar el articulo en la base de datos
    return HttpResponse(f"Artículo creado: <strong>{articulo.title} - {articulo.content}</strong>")

def save_article(request):  #No pasamos parametros por url y lo vamos a pasar por formulario
    if request.method == 'GET':
        title = request.GET['title']
        content = request.GET['content']
        public = request.GET['public']
        articulo = Article(
            title= title,
            content= content,
            public= public
        )
        articulo.save() #para guardar el articulo en la base de datos
        return HttpResponse(f"Artículo creado: <strong>{articulo.title} - {articulo.content}</strong>")
    else:
        return HttpResponse("<h2>No se ha podido crear el artículo</h2>")


def create_article(request):    #Soporte para plantilla para visualizar el formulario 
    return render(request, 'create_article.html')

def create_full_article(request):
    #Realizamos la comprobacion del metodo (POST-GET)
    if request.method == 'POST':
        #si llega datos por POST se debe:
        formulario = FormArticle(request.POST)
        #aqui podemos validar el formulario con un metodo is_valid
        if formulario.is_valid():
            #generamos una variable para recoger los datos del formulario
            data_form = formulario.cleaned_data #que son los datos limpios que nos llegan
            title = data_form.get('title') #lo puedo hacer asi ó
            content = data_form['content'] # lo puedo hacer asi
            public = data_form['public']

            articulo = Article(
                title = title, #title(nombre del modelo) = title(nombre de la variable)
                content = content,
                public = public
            )
            #Para guardar este articulo en la BD
            articulo.save()
            #Crear mensaje flash(Sesion que solo se muestra 1 vez)
            messages.success(request, f'Ha creado correctamente el articulo {articulo.id}')

            #rediccionar la pagina a ariculos despues de guardado
            return redirect('articulos')
            #return HttpResponse(articulo.title + ' -- ' + articulo.content + ' -- ' + str(articulo.public))

    else:
        #si nos llegan datos por POST debemos generar un formulario vacio
        formulario = FormArticle() #creamos una variable llamada formulario para instanciar el objeto
        #se carga la vista en html
    return render(request, 'create_full_article.html', {
        'form' : formulario
    })

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

# Mostrar articulos de la base de datos
def articulos(request): # Creacion de la vista de articulos
    #Creamos una template para listar varos articulos
    #1. hacemos la peticion a la base de datos
    #Creamos la variable articulos y LLamamos al modelo Article, usamos objects para porder hacer una consulta
    articulos = Article.objects.filter(public=True).order_by('-id') #En este caso no usamos el metodo get si no el metodo all()
    #para sacar toda la información
    #dentro de articulos tenemos una lista de objetos un array de objetos
    """
    articulos = Article.objects.all()

    articulos = Article.objects.filter(title__contains="articulo")

    articulos = Article.objects.filter(title="Articulo", public=False)

    articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title='Articulo' AND public=0")
    """
    return render(request, 'articulos.html', {
        'articulos': articulos
    })


def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()

    return redirect('articulos')