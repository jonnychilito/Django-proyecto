from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Category, Article
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def list(request):
    articles = Article.objects.all()

    #paginar los articulos
    paginator = Paginator(articles, 2)

    #recoger numero de pagina
    page = request.GET.get('page')
    page_articles = paginator.get_page(page)


    return render(request, 'articles/list.html', {
        'title' : 'Articulos',
        'articles' :page_articles
    })
@login_required(login_url="login")
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    #articles = Article.objects.filter(categories=category_id)  ESTA ES OTRA MANERA DE FILTRAR LOS ARTICULOS POR CATEGORIA

    return render(request, 'categories/category.html', {
        'category' : category,
        #'articles' : articles  ESTA ES OTRA MANERA DE FILTRAR LOS ARTICULOS POR CATEGORIA
    })
@login_required(login_url="login")
def article(request, article_id):

    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/detail.html', {
        'article' : article
    })