from django.urls import path
from blog import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    
    path("sign-in", views.sign_in, name="sign-in"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("recovery-password", views.recovery_password, name="recovery-password"),
    
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>", views.blog_details, name="blog-details"),
    path('logout/', views.logout_view, name='logout'),
]
