###
### django libraries
###
from django.views.decorators.csrf import csrf_exempt


###
### project libraries
###
from point_filter import *
import high_low.models as MD
import lib.json_response as JR


###
### HTTP/JSON APIs
###
def list_points(request, **kwargs):
    start = request.REQUEST.get('id', 1)
    count = request.REQUEST.get('count', 10)
    pt_qs = MD.Point.objects.filter(id__gte=start)
    return JR.return_success(pt_qs[:count])


def get_length(request, **kwargs):
    pt_qs = MD.Point.objects.all()
    return JR.return_success(pt_qs.count())


@csrf_exempt
def add_point(request, **kwargs):
    req = request.REQUEST
    # check existence
    t = MD.Point.objects.filter(time=req['time'],
                                price=req['price'])
    if t.exists():
        return JR.return_already_exists()
    # add a new point
    p = MD.Point(time = req['time'],
                 price = req['price'])
    p.save()
    return JR.return_success(dict(id=p.pk))


def filter_points(request, **kwargs):
    amp = request.REQUEST.get('amplitude', 450)
    pt_qs = MD.Point.objects.all()
    result = _filter_points(list(pt_qs), float(amp))
    return JR.return_success(result)


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
