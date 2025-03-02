from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Article,Commentaire, Tag, Categorie
from django.contrib import messages

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

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model

def recovery_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
            
            # Send email
            subject = "Réinitialisation de votre mot de passe"
            message = f"""
            Bonjour,
            
            Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte.
            
            Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant:
            {reset_link}
            
            Si vous n'avez pas demandé de réinitialisation de mot de passe, vous pouvez ignorer cet e-mail.
            
            Cordialement,
            L'équipe du site
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "Un e-mail de réinitialisation a été envoyé à l'adresse indiquée.")
            return redirect('index')
            
        except User.DoesNotExist:
            # Still show success message for security reasons
            messages.success(request, "Un e-mail de réinitialisation a été envoyé à l'adresse indiquée.")
            return redirect('index')
    
    return render(request, 'recovery-password.html')

def blog_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST' and request.user.is_authenticated:
        contenu = request.POST.get('contenu')
        if contenu:
            commentaire = Commentaire.objects.create(
                auteur_id=request.user,
                article_id=article,
                contenu=contenu
            )
            
            return redirect('blog-details', slug=slug)
    
    return render(request, 'blog-single.html', {'article': article})

def add_article(request):
    categories = Categorie.objects.filter(statut=True)
    tags = Tag.objects.filter(statut=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        # Get form data
        titre = request.POST.get('titre')
        resume = request.POST.get('resume')
        contenu = request.POST.get('contenu')
        categorie_id = request.POST.get('categorie_id')
        est_publie = request.POST.get('est_publie') == 'on'
        
        # Handle file upload
        couverture = request.FILES.get('couverture')
        
        # Create article
        article = Article(
            titre=titre,
            resume=resume,
            contenu=contenu,
            couverture=couverture,
            auteur_id=request.user,
            categorie_id=Categorie.objects.get(id=categorie_id),
            est_publie=est_publie
        )
        
        # Save article to get an ID
        article.save()
        
        # Handle existing tags (multi-selection)
        tag_ids = request.POST.getlist('tag_ids')
        if tag_ids:
            for tag_id in tag_ids:
                tag = Tag.objects.get(id=tag_id)
                article.tag_ids.add(tag)
        
        # Handle new tags
        new_tags = request.POST.get('new_tags', '').strip()
        if new_tags:
            # Split by comma and process each tag
            tag_names = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                # Check if tag already exists to avoid duplicates
                tag, created = Tag.objects.get_or_create(
                    nom=tag_name,
                    defaults={'statut': True}
                )
                article.tag_ids.add(tag)
        
        messages.success(request, "Article créé avec succès!")
        return redirect('dashboard')
    
    datas = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'add-article.html', datas)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

def reset_password(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password and password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return redirect('sign-in')
            else:
                messages.error(request, "Les mots de passe ne correspondent pas.")
        
        return render(request, 'reset-password.html')
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return redirect('recovery-password')
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, auteur_id=request.user)
    categories = Categorie.objects.filter(statut=True)
    tags = Tag.objects.filter(statut=True)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.POST.get('titre')
        resume = request.POST.get('resume')
        contenu = request.POST.get('contenu')
        categorie_id = request.POST.get('categorie_id')
        est_publie = request.POST.get('est_publie') == 'on'
        
        # Gérer l'upload de fichier
        couverture = request.FILES.get('couverture')
        
        # Mettre à jour l'article
        article.titre = titre
        article.resume = resume
        article.contenu = contenu
        article.categorie_id = Categorie.objects.get(id=categorie_id)
        article.est_publie = est_publie
        
        if couverture:
            article.couverture = couverture
        
        # Sauvegarder les modifications
        article.save()
        
        # Gérer les tags
        article.tag_ids.clear()  # Supprimer les anciens tags
        
        # Gérer les tags existants
        tag_ids = request.POST.getlist('tag_ids')
        if tag_ids:
            for tag_id in tag_ids:
                tag = Tag.objects.get(id=tag_id)
                article.tag_ids.add(tag)
        
        # Gérer les nouveaux tags
        new_tags = request.POST.get('new_tags', '').strip()
        if new_tags:
            tag_names = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    nom=tag_name,
                    defaults={'statut': True}
                )
                article.tag_ids.add(tag)
        
        messages.success(request, "Article mis à jour avec succès!")
        return redirect('dashboard')
    
    # Préparer les tags actuels de l'article pour l'affichage
    current_tags = ', '.join([tag.nom for tag in article.tag_ids.all()])
    
    datas = {
        'article': article,
        'categories': categories,
        'tags': tags,
        'current_tags': current_tags,
    }
    return render(request, 'edit-article.html', datas)

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, auteur_id=request.user)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article supprimé avec succès!")
        return redirect('dashboard')
    
    return render(request, 'delete-article-confirm.html', {'article': article})