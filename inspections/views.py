from django.views.generic import TemplateView, DetailView
from inspections.models import Establishment


class EstablishmentList(TemplateView):
    template_name = 'inspections/establishment_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstablishmentList, self).get_context_data(**kwargs)
        establishments = Establishment.objects.filter(status='ACTIVE')
        establishments = establishments.order_by('premise_name')
        context['establishments'] = establishments[:10]
        return context


class EstablishmentDetail(DetailView):
    model = Establishment
    context_object_name = 'establishment'

    def get_context_data(self, **kwargs):
        context = super(EstablishmentDetail, self).get_context_data(**kwargs)
        establishment = context['establishment']
        context['inspections'] = establishment.inspections.order_by('-insp_date')
        return context
