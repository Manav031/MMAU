from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('', views.createUser, name="index"),
    path('registerUser/', views.registerUser, name="register"),
    path('loginUser/', obtain_auth_token, name="login"),
    path('userProfile/', views.userProfile, name="userProfile"),
    path('userProfileCreate/', views.userProfileCreate, name="userProfileCreate"),
    path('createBloodRequest/', views.createBloodRequest, name="createBloodRequest"),
    path('getBloodDetail/<id>/', views.getBloodDetail, name="getBloodDetail"),
    path('editBloodDetail/<id>/', views.editBloodDetail, name="editBloodDetail"),
    path('deleteBloodDetail/<id>/', views.deleteBloodDetail, name="deleteBloodDetail"),
    path('getBloodDetail/<id>/transferPoint/', views.transferPoint, name="transferPoint"),
]