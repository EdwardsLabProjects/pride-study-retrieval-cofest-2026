
import urllib.request, urllib.parse, json, base64

def get(id):
    request = '/pride/'+id
    return couch_webservice_request(request)

def search(payload):
    if isinstance(payload,str):
        payload = json.loads(payload)
    pagesize = 100
    payload["limit"] = pagesize
    request = '/pride/_find'
    response = couch_webservice_request(request,payload,method='POST')
    payload["bookmark"] = response["bookmark"]
    for doc in response["docs"]:
        yield doc
    nret = len(response["docs"])
    skip = nret
    while nret >= pagesize:
        payload["skip"] = skip
        response = couch_webservice_request(request,payload,method='POST')
        for doc in response["docs"]:
            yield doc
        nret = len(response["docs"])
        skip += nret

def searchids(payloadstr,ids):
    payloadstr = payloadstr.replace("___XXX_IDS_XXX___",",".join(map(lambda s: ('%r'%(s,)).replace('\'','"'),ids)))
    for doc in search(payloadstr):
        yield doc

def couch_webservice_request(request,*args,**kwargs):
    baseurl = 'https://edwardslab.bmcb.georgetown.edu/pride-couchdb'
    url = baseurl + "/" + request.lstrip('/')
    if 'username' not in kwargs:
         kwargs['username'] = 'public'
    if 'password' not in kwargs:
         kwargs['password'] = 'public'
    return webservice_request(url,*args,**kwargs)

def webservice_request(request,
                       payload={},
                       method='GET',
                       username=None,
                       password=None):
    headers = {'Content-type': 'application/json',
               'Accept':       'application/json'}
    opener = urllib.request.build_opener(urllib.request.HTTPHandler())
    if username and password:
        b64 = base64.b64encode(('%s:%s'%(username, password)).encode()).decode()
        headers["Authorization"] = "Basic %s"%(b64,)
    url = request
    if method == 'GET':
        if payload != {}:
            url += '?' + urllib.parse.urlencode(payload)
        request = urllib.request.Request(url, headers=headers)
    elif method == 'POST':
        request = urllib.request.Request(url, json.dumps(payload).encode(), headers=headers)
    elif method == 'PUT':
        request = urllib.request.Request(url, json.dumps(payload).encode(), headers=headers)
        request.get_method = lambda: 'PUT'
    elif method == 'DELETE':
        request = urllib.request.Request(url, json.dumps(payload).encode(), headers=headers)
        request.get_method = lambda: 'DELETE'
    else:
        raise RuntimeError('Bad method '+method)
    try:
        return json.loads(opener.open(request).read())
    except urllib.request.HTTPError as e:
        return {u'error': True, u'errorcode': e.code, u'errormsg': e.msg}
    return {u'error': True}
