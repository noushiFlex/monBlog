from rest_framework import permissions
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .viewset import ArticleViewSet, CategorieViewSet, TagViewSet, CommentaireViewSet
from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Documentation de l'API du blog",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

# Configuration du routeur DRF
router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet, basename="article")
router.register(r'tags', TagViewSet, basename="tag")
router.register(r'categories', CategorieViewSet, basename="categorie")
router.register(r'commentaires', CommentaireViewSet, basename="commentaire")

urlpatterns = [
    # Vues classiques Django
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Authentification
    path("sign-in/", views.sign_in, name="sign-in"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("logout/", views.logout_view, name="logout"),
    path("recovery-password/", views.recovery_password, name="recovery-password"),
    path("reset-password/<str:uidb64>/<str:token>/", views.reset_password, name="reset-password"),
    path("activate-account/<str:token>/", views.activate_account, name="activate-account"),
    path("resend-activation/", views.resend_activation, name="resend-activation"),

    # Gestion des articles
    path("edit-article/<int:article_id>/", views.edit_article, name="edit-article"),
    path("delete-article/<int:article_id>/", views.delete_article, name="delete-article"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_details, name="blog-details"),
    path("add-article/", views.add_article, name="add-article"),

    # API Rest Framework
    path("api/", include(router.urls)),  # 🔥 API DRF
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # Documentation Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]