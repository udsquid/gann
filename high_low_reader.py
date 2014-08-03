#
# python libraries
#
import httplib2


#
# module functions
#
def do_read(source):
    records = list()
    with open(source) as f:
        lines = f.readlines()
        for l in lines:
            time, price = l.replace(',', '').strip().split()
            records.append((time, price))
    return records


def post_to_repo(records):
    server = httplib2.Http()
    url_tmpl = 'http://{host}:{port}/high_low/' + \
               'point/add/' + \
               '?time={time}&price={price}'
    for t, p in records:
        param = dict(
            host='localhost',
            port=8000,
            time=t.replace('/', '-'),
            price=p)
        url = url_tmpl.format(**param)
        resp, data = server.request(url, 'POST')
        if resp['status'] != '200':
            raise Exception("server return error: %s" % repr(resp))


#
# main procedure
#
if __name__ == '__main__':
    import os.path
    full_path = os.path.abspath("data/taiex_high_low.txt")
    print "Reading data.. ",
    records = do_read(full_path)
    print "done!"
    print "Posting into repository.. "
    post_to_repo(records)
    print "done!"
