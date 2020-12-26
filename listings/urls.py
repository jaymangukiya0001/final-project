from django.contrib import admin
from django.urls import path,include
from listings import views
urlpatterns = [
    path('',views.listings,name="listings"),
    path('<int:pk>/',views.listing,name="listing"),
    path('search/',views.search,name="search"),
    path('create/',views.create,name="create"),
    path('update/<int:pk>/',views.update,name="update"),
    path('delete/<int:pk>',views.delete_listing,name="delete"),

]
