from django.urls import path
from blog import views


urlpatterns = [
    path("", views.index, name="index"),
    
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    
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
    
    path('dashboard', views.dashboard, name='dashboard'),
    
]
