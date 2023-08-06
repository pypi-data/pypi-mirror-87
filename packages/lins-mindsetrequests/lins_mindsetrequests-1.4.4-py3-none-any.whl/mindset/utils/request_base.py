from requests import request
from requests.exceptions import ConnectTimeout, ReadTimeout
from requests.models import Response
from os import environ
from json import dumps
from re import match
from urllib.parse import urlencode


def mindset_request(method, path, json={}, query_params={}):
    url = url_factory(path, query_params)
    try:
        return request(method, url, json=json, timeout=float(environ.get('REQUEST_TIMEOUT', 5)))
    except (ConnectTimeout, ReadTimeout):
        return response_factory(408, {'error': f'Connection to {url} timed out'})


def response_factory(status_code, json):
    response = Response()
    response.status_code = status_code
    response._content = f'{dumps(json)}'.encode('UTF-8')
    return response


def url_factory(path='', query_params={}):
    if not match(r'(https?:\/\/(?:www\.|(?!www)))\S*$', environ.get('API_INTEGRACAO_URL', '')):
        raise EnvironmentError('URL inválida. Verifique a variável de ambiente "API_INTEGRACAO_URL".')
    if environ['API_INTEGRACAO_URL'][-1] == '/':
        raise EnvironmentError('URL inválida. Remova a contrabarra no final da url.')
    query_string = {urlencode(query_params): f'?{urlencode(query_params)}'}
    return f'{environ["API_INTEGRACAO_URL"]}{path}{query_string.get(urlencode(query_params), "")}'
