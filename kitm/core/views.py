from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from core.models import Nomenclature


def set_rating_nomenclature(request, nom_pk):
    if request.method == 'POST':
        print(nom_pk)
    nom_card = get_object_or_404(Nomenclature, pk=nom_pk)
    return render(request, 'includes/nom_card.html', {'nom_card': nom_card})
