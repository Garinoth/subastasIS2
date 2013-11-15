from django.shortcuts import render


def index(request):
    pass


def test(request):
    context = {}
    return render(request, 'subastas/index.html', context)
