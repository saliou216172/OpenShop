from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import AnnonceForm
from .models import Annonce, Categorie, SousCategorie
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

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
    annonces = Annonce.objects.filter(
    categorie=categorie
    ).annotate(
    premium_order=Case(
        When(
            is_premium=True,
            premium_until__gte=timezone.now(),
            then=Value(0)
        ),
        default=Value(1),
        output_field=IntegerField()
    )
    ).order_by('premium_order', '-date_pub')

    return render(request, 'store/annonces.html', {
        'categorie': categorie,
        'sous_categories': sous_categories,
        'annonces': annonces
    })


def annonces_par_souscategorie(request, souscategorie_id):
    souscategorie = get_object_or_404(SousCategorie, id=souscategorie_id)
    # affiche une liste verticale d'annonces, les plus récentes en haut
    annonces = Annonce.objects.filter(
    sous_categorie_id=souscategorie.id
    ).annotate(
    premium_order=Case(
        When(
            is_premium=True,
            premium_until__gte=timezone.now(),
            then=Value(0)
        ),
        default=Value(1),
        output_field=IntegerField()
    )
    ).order_by('premium_order', '-date_pub')
    
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
