from django.urls import path
from.import views 


urlpatterns = [ 
    path("", views.home, name="home"), 
    path("creer_annonce/", views.creer_annonce, name="creer_annonce"),
    path("categorie/<str:categorie_id>/", views.annonces_par_categorie, name='annonces_par_categorie'),
    path('souscategorie/<int:souscategorie_id>/', views.annonces_par_souscategorie, name='annonces_par_souscategorie'),
    path('get_sous_categories/', views.get_sous_categories, name='get_sous_categories')
]