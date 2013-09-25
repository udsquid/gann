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
def return_result(success, data, **kwargs):
    if isinstance(data, QuerySet):
        data = _qs_to_json(data)
    result = dict(success = success,
                  data = data)
    result.update(kwargs)
    return HttpResponse(json.dumps(result))


def return_success(data=None):
    return return_result(success=True, data=data)


def return_error(reason, data=None):
    return return_result(success=False, data=data, reason=reason)


def return_already_exists(data):
    return return_error(
        reason = "already exists",
        data = data)


###
### helper functions
###
def _qs_to_json(data):
    json_data = SRL.serialize('json', data)
    return json.loads(json_data)
