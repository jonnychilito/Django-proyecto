from pages.models import Page

def get_pages(request): #es una vista que se puede utilizar en varios sitios

    pages = Page.objects.filter(visible=True).order_by('order').values_list('id', 'title', 'slug')
    

    return{
        'pages': pages
    }