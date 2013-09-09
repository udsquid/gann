###
### python libraries
###
import json


###
### django libraries
###
from django.core import serializers as SRL
from django.db.models.query import QuerySet
from django.http import HttpResponse


###
### module functions
###
def return_result(data):
    if isinstance(data, QuerySet):
        final_data = _to_json(data)
    else:
        final_data = data
    res = dict(success = True,
               data = final_data)
    return HttpResponse(json.dumps(res))


def return_already_exists():
    res = dict(success = False,
               reason = "already exists")
    return HttpResponse(json.dumps(res))


###
### helper functions
###
def _to_json(data):
    json_data = SRL.serialize('json', data)
    return json.loads(json_data)
