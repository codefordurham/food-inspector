from django import template
from collections import OrderedDict
register = template.Library()


@register.inclusion_tag('tags/establishment_detail_table.html')
def details_to_table(inspection):
    """
    Displays key-value-paired inspection data in a table.
    """

    inspection_details = OrderedDict()

    inspection_details["grade"] = inspection.grade
    inspection_details["inspection_reason_desc"] = inspection.inspection_reason_desc
    inspection_details["violations"] = inspection.violations
    inspection_details["final_score_sum"] = inspection.final_score_sum

    return {'inspection_details': inspection_details}

