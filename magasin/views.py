from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import Produit
from .models import Fournisseur
from .forms import ProduitForm
from .forms import Commande
from .forms import CommandeForm
from django.shortcuts import redirect
from .forms import  FournisseurForm
from django.contrib.auth.decorators import login_required
from .forms import ProduitForm, FournisseurForm,UserRegistrationForm
from django.contrib.auth import login, authenticate  , logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout 
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.models import Categorie , Produit
from rest_framework import viewsets
from magasin.serializers import CategorySerializer , ProduitSerializer
# Create your views here.
def index(request):
    if (request.method == "POST") :
        form = ProduitForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else :
        form = ProduitForm() #créer formulaire vide
    list= Produit.objects.all()
    return render(request,'magasin/vitrine.html',{'list':list})
        # context={'products':products}
        # return render( request,'magasin/mesProduits.html ',context )
# return render(request,'vitrine.html',{'list':list})

class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    def get_queryset(self):
        queryset = Produit.objects.filter()
        category_id = self.request.GET.get('Catégorie')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset
def nouveauFournisseur(request):
    form = FournisseurForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    fournisseurs = Fournisseur.objects.all()
    context = {'form': form, 'fournisseurs': fournisseurs}
    return render(request, 'magasin/fournisseur.html', context)        
def nouveauCommande(request):
    form = CommandeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    commandes = Commande.objects.all()
    context = {'form': form, 'commandes': commandes}
    return render(request, 'magasin/Commande.html', context) 
class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        produit = Produit.objects.all()
        serializer = ProduitSerializer(produit, many=True)
        return Response(serializer.data)
# def nouvelleCommande(request):
#     if request.method == "POST" :   
#         form=CommandeForm(request.POST,request.FILES)  
#         if form.is_valid():          
#             cde=form.save()
#             #return redirect('/magasin')
#     else:
#         form=CommandeForm() #créer formulaire vide
#         cde=form       
#     liste=Commande.objects.all()
#     context={'form':form,'lesCdes':liste,'cd':cde}
#     return render(request,'magasin/nouvelleCommande.html',context)
def logout_view(request): 
    logout(request)
@login_required
def home(request):
    context={'val':"Menu Acceuil"}     
    return render(request,'vitrine.html',context) 
def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password) 
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a étécréé avec succès !')
            return redirect('/magasin')
    else :
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form' : form})