from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Article

from django.contrib.auth import logout as auth_logout 
from django.shortcuts import redirect

def index(request):
    articles = Article.objects.filter(est_publie=True).order_by('id')[:3]
    datas = {
        'active_index': 'active',
        'articles': articles,
        'user_authenticated': request.user.is_authenticated,  # Vérifie si l'utilisateur est connecté
        'user': request.user  # Envoie l'utilisateur au template
    }
    return render(request, 'index.html', datas)

def contact(request):
    datas = {
        'active_contact' : 'active'

    }

    return render(request, 'contact.html', datas)

def about(request):
    datas = {
        'active_about' : 'active',
    }

    return render(request, 'about.html', datas)

def blog(request):
    articles_list = Article.objects.filter(est_publie=True).order_by('id') 
    paginator = Paginator(articles_list, 3)  
    page_number = request.GET.get('page')  
    articles = paginator.get_page(page_number)  
    datas = {
        'active_blog' : 'active',
        'articles': articles
        
    }
    return render(request, 'blog.html', datas)

def blog_details(request, slug):
    
    article =Article.objects.get(slug=slug)
    datas = {
        'active_blog' : 'active',
        'article':article,
    }
    
    return render(request, 'blog-single.html', datas)

def sign_in(request):
    datas = {
    }
    return render(request, 'sign-in.html', datas)

def sign_up(request):
    datas = {
    }
    return render(request, 'sign-up.html', datas)

def logout_view(request):
    auth_logout(request)
    return redirect('index')

def recovery_password(request):
    datas = {
    }
    return render(request, 'recovery-password.html', datas)