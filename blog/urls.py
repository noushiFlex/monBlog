from django.urls import path, include
from blog import views
from rest_framework import routers
from .viewset import ArticleViewSet
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')



router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path(r"api-doc/", schema_view),
    
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path('dashboard', views.dashboard, name='dashboard'),
    
    path("sign-in", views.sign_in, name="sign-in"),
    path("sign-up", views.sign_up, name="sign-up"),
    path('logout/', views.logout_view, name='logout'),
    path("recovery-password", views.recovery_password, name="recovery-password"),
    path("reset-password/<str:uidb64>/<str:token>/", views.reset_password, name="reset-password"),
    path("activate-account/<str:token>/", views.activate_account, name="activate-account"),
    path("resend-activation/", views.resend_activation, name="resend-activation"),
    
    
    path("edit-article/<int:article_id>/", views.edit_article, name="edit-article"),
    path("delete-article/<int:article_id>/", views.delete_article, name="delete-article"),
    
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>", views.blog_details, name="blog-details"),
    path("add-article/", views.add_article, name="add-article"),
    
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
