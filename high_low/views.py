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
from django.views.decorators.csrf import csrf_exempt


###
### project libraries
###
from point_filter import *
import high_low.models as MD


###
### HTTP/JSON APIs
###
def list_points(request, **kwargs):
    start = request.REQUEST.get('id', 1)
    count = request.REQUEST.get('count', 10)
    pt_qs = MD.Point.objects.filter(id__gte=start)
    return return_result(pt_qs[:count])


def get_length(request, **kwargs):
    pt_qs = MD.Point.objects.all()
    return return_result(pt_qs.count())


@csrf_exempt
def add_point(request, **kwargs):
    req = request.REQUEST
    # check existence
    t = MD.Point.objects.filter(time=req['time'],
                                price=req['price'])
    if t.exists():
        return return_already_exists()
    # add a new point
    p = MD.Point(time = req['time'],
                 price = req['price'])
    p.save()
    return return_result(dict(id=p.pk))


def filter_points(request, **kwargs):
    amp = request.REQUEST.get('amplitude', 450)
    pt_qs = MD.Point.objects.all()
    result = _filter_points(list(pt_qs), float(amp))
    return return_result(result)


###
### helper functions
###
# --- http/json ---
def return_result(data):
    if isinstance(data, QuerySet):
        final_data = to_json(data)
    else:
        final_data = data
    res = dict(success = True,
               data = final_data)
    return HttpResponse(json.dumps(res))


def return_already_exists():
    res = dict(success = False,
               reason = "already exists")
    return HttpResponse(json.dumps(res))


def to_json(data):
    json_data = SRL.serialize('json', data)
    return json.loads(json_data)


# --- models ---
def _filter_points(pt_list, amp):
    """Forward points one by one to check the amplitude,
    save peak/trough when amplitude is greater than given value.
    """
    init(amp)
    for p in pt_list:
        forward2(p)
    cleanup2()
    return get_result()
