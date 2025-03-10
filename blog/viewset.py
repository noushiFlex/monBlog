from rest_framework import viewsets
from .models import Article, Categorie, Tag, Commentaire
from .serializers import ArticleSerializer, CategorieSerializer, TagSerializer, CommentaireSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie_id', 'auteur_id']  
    search_fields = ['titre', 'contenu']  # Recherche textuelle
    ordering_fields = ['date_creation', 'titre'] 
    
    def create(self, request, *args, **kwargs):
        # Assurez-vous que l'ID n'est pas dans les données
        if 'id' in request.data:
            request.data.pop('id')
        return super().create(request, *args, **kwargs)

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer