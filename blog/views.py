from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Article

from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

from .forms import LoginForm,RegistrationForm

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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")
    
    else:
        form = LoginForm()

    return render(request, 'sign-in.html', {'form': form})




def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_staff = False 
            user.is_superuser = False  
            user.save()
    else:
        form = RegistrationForm()
    return render(request, 'sign-up.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('index')

def recovery_password(request):
    datas = {
    }
    return render(request, 'recovery-password.html', datas)