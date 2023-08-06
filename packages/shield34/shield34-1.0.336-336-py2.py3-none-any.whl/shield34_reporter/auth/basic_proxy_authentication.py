from requests.auth import HTTPProxyAuth


def authenticate_proxy(auth_info, response, **args):
    request = response.request.copy()
    HTTPProxyAuth(auth_info.username, auth_info.password).__call__(request)
    args_nostream = dict(args, stream=False)
    return response.connection.send(request, **args_nostream)