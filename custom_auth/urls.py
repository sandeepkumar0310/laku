
from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('', SignIn.as_view(),name='sign-in'),
    path('sign-up/', SignUp.as_view(),name='sign-up'),
    path('dashboard/', Dashboard.as_view(),name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('all-blog/', BlogList.as_view(),name='all-blog'),
    path('save-comment/', save_comment),
    path('save-like/', save_like),
    path('share-blog/', share_blog,name="share-blog"),

    


    


    

]

