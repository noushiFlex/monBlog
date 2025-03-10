from rest_framework import serializers
from .models import Article, Categorie, Tag, Commentaire
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializer pour Categorie
class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description']

# Serializer pour Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nom']

# Serializer pour Auteur
class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer pour les commentaires
class CommentaireSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(source="auteur_id", read_only=True)
    
    class Meta:
        model = Commentaire
        fields = ['id', 'auteur', 'contenu', 'created_at']

# Serializer principal pour Article
class ArticleSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(source="auteur_id", read_only=True)
    categorie = CategorieSerializer(source="categorie_id", read_only=True)
    tags = TagSerializer(source="tag_ids", many=True, read_only=True)
    commentaires = CommentaireSerializer(source="article_commentaire_ids", many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'

        read_only_fields = ['id']