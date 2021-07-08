from django.shortcuts import render
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'


def handler400(request, exception):
    return render(request, "status/400.html", status=400)


def handler403(request, exception):
    return render(request, "status/403.html", status=403)


def handler404(request, exception):
    return render(request, "status/404.html", status=404)


def handler500(request, *args, **argv):
    return render(request, "status/500.html", status=500)


def handler503(request, exception):
    return render(request, "status/503.html", status=503)
