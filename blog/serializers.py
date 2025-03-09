from .models import Article
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','titre', 'resume', 'contenu', 'auteur_id', 'categorie_id', 'created_at', 'last_updated_at']
        depth=5
