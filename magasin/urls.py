from django.urls import path,include
from . import views
from .views import CategoryAPIView , ProduitAPIView

urlpatterns = [
path('', views.index , name='index'),
path('nouvFournisseur/',views.nouveauFournisseur,name='nouveauFour'),
path('nouvCde/',views.nouveauCommande,name='nouveauCde'),
path('register/',views.register, name = 'register'),
path('logout/',views.logout, name = 'logout'),
path('api/category/', CategoryAPIView.as_view()),
path('api/produits/', ProduitAPIView.as_view()),
]