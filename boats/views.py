from django.views.generic import DetailView
from models import Boats
# Create your views here.


class index(DetailView):
    model = Boats
    template_name = 'preview.html'
    context_object_name = 'boat'