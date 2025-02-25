from django import forms
from blog.models import Article, Commentaire

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', "couverture", "resume", "contenu", "categorie_id", "tag_ids"]

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['auteur_id', "article_id", "contenu"]