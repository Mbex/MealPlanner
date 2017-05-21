import flask

def preflight_allow_CORS():

    response = flask.Response(status=201)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    # print "PREFLIGHT RESPONSE: \n", response.headers
    return response

print vars(preflight_allow_CORS().headers)


varriables = vars(preflight_allow_CORS().headers)["_list"]
self.assertTrue()
