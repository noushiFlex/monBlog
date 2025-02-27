from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Article,Commentaire

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
    paginator = Paginator(articles_list, 6)  
    page_number = request.GET.get('page')  
    articles = paginator.get_page(page_number)  
    datas = {
        'active_blog' : 'active',
        'articles': articles
        
    }
    return render(request, 'blog.html', datas)

def dashboard(request):
    articles_list = Article.objects.filter(auteur_id=request.user)
    commentaires_list = Commentaire.objects.filter(auteur_id=request.user)
    datas = {
        'active_dashboard' : 'active',
        'articles': articles_list,
        'commentaires': commentaires_list,
    }

    return render(request, 'dashboard.html', datas)

def blog_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST' and request.user.is_authenticated:
        contenu = request.POST.get('contenu')
        if contenu:
            # Créer le commentaire sans essayer d'ajouter à article.comments_ids
            commentaire = Commentaire.objects.create(
                auteur_id=request.user,
                article_id=article,
                contenu=contenu
            )
            # Pas besoin d'ajouter à article.comments_ids car la relation est déjà établie
            # via article_id dans le modèle Commentaire
            
            return redirect('blog-details', slug=slug)
    
    return render(request, 'blog-single.html', {'article': article})

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
            try:
                user = form.save(commit=False)
                user.is_staff = False 
                user.is_superuser = False  
                user.save()
                login(request, user)
                return redirect('index')
            except Exception as e:
                print(f"Une erreur est survenue : {e}")
                form = RegistrationForm()
        else:
            print(form.errors)
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
