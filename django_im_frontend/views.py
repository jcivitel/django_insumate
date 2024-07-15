from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
def dashboard(request):
    template = loader.get_template("projects/project_list.html")

    template_opts = dict()

    return HttpResponse(template.render(template_opts, request))
