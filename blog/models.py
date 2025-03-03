from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import slugify
from datetime import datetime


User = get_user_model()

# Create your models here.

class Categorie(models.Model):

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    nom = models.CharField(verbose_name="Nom", max_length=255)
    description = models.TextField()
    

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    

class Tag(models.Model):

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    nom = models.CharField(verbose_name="Nom", max_length=255)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Article(models.Model):

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    titre = models.CharField(max_length=256)
    couverture = models.ImageField(upload_to="articles")
    resume = models.TextField()
    contenu = CKEditor5Field('Text', config_name='extends')

    auteur_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="auteur_article_ids")
    categorie_id = models.ForeignKey('blog.Categorie', on_delete=models.SET_NULL, null=True, related_name="categorie_article_ids", verbose_name="Catégorie")
    tag_ids = models.ManyToManyField('blog.Tag', related_name="tag_article_ids", verbose_name="Tags")
    # Removed the comments_ids field as it creates a circular dependency
    
    est_publie = models.BooleanField(default=False)
    date_de_publication = models.DateField(auto_now_add=True)
    
    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(default="", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Pour un nouvel article, on sauvegarde d'abord pour avoir une date
            super(Article, self).save(*args, **kwargs)
            # Puis on met à jour le slug avec la date maintenant disponible
            self.slug = slugify(self.titre) + "-" + str(self.date_de_publication.year)
            # On sauvegarde à nouveau avec le slug mis à jour
            super(Article, self).save(*args, **kwargs)
        else:
            # Pour un article existant
            self.slug = slugify(self.titre) + "-" + str(self.date_de_publication.year) + str(self.date_de_publication.month) + str(self.date_de_publication.day) + str(self.date_de_publication.hour) + str(self.date_de_publication.minute) + str(self.date_de_publication.second)
 
            super(Article, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']  # Sort by newest first by default

    auteur_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="auteur_commentaire_ids")
    article_id = models.ForeignKey('blog.Article', on_delete=models.CASCADE, related_name="article_commentaire_ids")
    contenu = models.TextField(blank=True, null=True)  # Changed to make it optional in admin
    
    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.auteur_id.username} on {self.article_id.titre}"
    
    
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    est_actif = models.BooleanField(default=False)
    token_activation = models.CharField(max_length=100, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = str(uuid.uuid4())
        Profil.objects.create(user=instance, token_activation=token)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()