from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_req, name = "loginPage"),
    path('register', register_req, name = "registerPage"),
    path('logout', logout_req, name = "logoutPage"),
    path('profile/<slug:slug>', profilePage, name = "profilePage"),
    path('profile/<slug:slug>/change-infos', userChangeInfos, name = "userChangeInfos"),
    path('profile/<slug:slug>/change-password', userChangePassword, name = "userChangePassword"),
    path('profile/<slug:slug>/change-images', userChangeImages, name = "userChangeImages"),
    path('activate<uidb64>/<token>', activate, name='activate'),
]