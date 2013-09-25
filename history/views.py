###
### django libraries
###
from django.views.decorators.csrf import csrf_exempt


###
### project libraries
###
import history.models as MD
import lib.json_response as JR


###
### module functions
###
def history_do(request, category, action, **kwargs):
    # validate the index worker
    if category not in _iworker:
        pass
    if action not in _iworker[category]:
        # return error with invalid action message
        pass
    # invoke worker's action
    func = _iworker[category][action]
    result = func(**kwargs)
    return JR.return_result(result)


# --- TAIEX actions ---
def list_taiex(**kwargs):
    return 'list_taiex'


def len_taiex(**kwargs):
    return 'len_taiex'


@csrf_exempt
def add_taiex(**kwargs):
    return 'add_taiex'


def list_tx(**kwargs):
    return 'list_tx'


def len_tx(**kwargs):
    return 'len_tx'


@csrf_exempt
def add_tx(**kwargs):
    return 'add_tx'


###
### module variables
###
_iworker = dict(
    taiex = dict(
        list = list_taiex,
        len = len_taiex,
        add = add_taiex),
    tx = dict(
        list = list_tx,
        len = list_tx,
        add = add_tx),
)
