from django.urls import path 
from . import views

urlpatterns = [
    
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    path("register", views.registerPage, name="register"),

    path("" , views.home, name="home"),
    path("service", views.service, name="service"),
    path("gallery", views.gallery, name="gallery"),
    path("post/<str:pk>/", views.post, name="post"),
    path("create-post", views.createPost, name="create-post"),
    path("update-post/<str:pk>/", views.updatePost, name="update-post"),
    path("delete-post/<str:pk>/", views.deletePost, name="delete-post"),

    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),


    path("mailbox", views.mailbox, name="mailbox"),
    path("convo/<str:pk>/" , views.convo, name="convo"),


]
