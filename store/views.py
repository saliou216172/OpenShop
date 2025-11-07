from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import AnnonceForm
from .models import Annonce, Categorie, SousCategorie

@login_required(login_url='authentication:login')
def creer_annonce(request):
    form = AnnonceForm()
    categories = Categorie.objects.all()

    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user
            annonce.save()
            return redirect('store:home')

    return render(request, 'store/creer_annonce.html', {
        'form': form,
        'categories': categories,
    })

def home(request):
    categories = Categorie.objects.all()
    return render(request, 'store/home.html', {'categories': categories})

def annonces_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    sous_categories = categorie.sous_categories.all()
    annonces = Annonce.objects.filter(categorie=categorie).order_by('-date_pub')

    return render(request, 'store/annonces.html', {
        'categorie': categorie,
        'sous_categories': sous_categories,
        'annonces': annonces
    })


def annonces_par_souscategorie(request, souscategorie_id):
    souscategorie = get_object_or_404(SousCategorie, id=souscategorie_id)
    # affiche une liste verticale d'annonces, les plus récentes en haut
    annonces = Annonce.objects.filter(sous_categorie_id=souscategorie.id).order_by('-date_pub')
    return render(request, 'store/sous_annonce.html', {
        'annonces': annonces,
        'souscategorie': souscategorie
    })

def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)

    telephone_clean = None
    if annonce.telephone:
        telephone_clean = ''.join(filter(str.isdigit, annonce.telephone))

    return render(request, 'store/annonce_detail.html', {
        'annonce': annonce,
        'telephone_clean': telephone_clean
    })


def get_sous_categories(request):
    categorie_id = request.GET.get('categorie_id')
    if not categorie_id:
        return JsonResponse([], safe=False)
    sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id)
    data = [{'id': sc.id, 'nom': sc.nom} for sc in sous_categories]
    return JsonResponse(data, safe=False)
