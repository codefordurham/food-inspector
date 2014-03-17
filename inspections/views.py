from django.views.generic import ListView, DetailView
from inspections.models import Establishment, Inspection


class EstablishmentList(ListView):
    model = Establishment
    context_object_name = 'establishments'
    template_name = 'inspections/establishment_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        objects = self.model.objects.all()
        if query:
            objects = objects.filter(premise_name__icontains=query)
        objects = objects.filter(status='ACTIVE', est_type=1)
        objects = objects.order_by('premise_name')
        objects = objects.extra(
            select={
	    'grade': "SELECT score_sum FROM inspections_inspection WHERE inspections_inspection.est_id_id = inspections_establishment.id AND inspections_inspection.insp_type = '1' ORDER BY inspections_inspection.insp_date DESC LIMIT 1",
	    'insp_date': "SELECT insp_date FROM inspections_inspection WHERE inspections_inspection.est_id_id = inspections_establishment.id AND inspections_inspection.insp_type = '1' ORDER BY inspections_inspection.insp_date DESC LIMIT 1"
            },
        )
        return objects


class EstablishmentDetail(DetailView):
    model = Establishment
    context_object_name = 'establishment'


    @staticmethod
    def dump_inspection_to_dict(inspection):
        """
        Convenience function that dumps key-value-paired inspection data into a dictionary.
        """
        assert isinstance(inspection, Inspection)

        dump = dict()

        for attr in dir(inspection):
            try:
                if not callable(getattr(inspection, attr)) and not attr.startswith('_'):
                    # at some point we'll want to get localized string for this attribute
                    dump[attr] = getattr(inspection, attr)
            except AttributeError:
                pass

        return dump


    def get_context_data(self, **kwargs):
        context = super(EstablishmentDetail, self).get_context_data(**kwargs)
        establishment = context['establishment']
        context['inspections'] = establishment.inspections.order_by('-insp_date')

        # get a dump to populate the details table for each inspection
        for inspection in context['inspections']:
            inspection.dump = EstablishmentDetail.dump_inspection_to_dict(inspection)

        return context
