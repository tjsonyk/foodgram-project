from django.shortcuts import render
from django.views.generic.base import TemplateView


def page_not_found(request, exception):
    return render(request, '404.html', {"path": request.path}, status=404)


def server_error(request):
    return render(request, '500.html', status=500)


class JustStaticPage(TemplateView):
    template_name = 'project.html'