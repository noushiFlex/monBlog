from django.urls import path
from blog import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("login", views.login, name="login"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>", views.blog_details, name="blog-details"),
]
