from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import slugify


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
    
    est_publie = models.BooleanField(default=False)
    date_de_publication = models.DateField(auto_now_add=True)
    
    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(default="", null=True, blank=True)
    
    def  save(self, *args, **kwargs):
        self.slug = slugify(self.titre) + str(self.date_de_publication.year)
        super(Article, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.titre
    

class Commentaire(models.Model):

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    auteur_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="auteur_commentaire_ids")
    article_id = models.ForeignKey('blog.Article', on_delete=models.CASCADE, related_name="article_commentaire_ids")
    contenu = models.TextField()

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.auteur_id.username


