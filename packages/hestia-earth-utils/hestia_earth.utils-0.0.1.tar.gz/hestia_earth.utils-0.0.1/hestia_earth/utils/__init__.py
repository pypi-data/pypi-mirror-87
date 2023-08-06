from pkgutil import extend_path
import requests
import os
import json
from hestia_earth.schema import SchemaType

__path__ = extend_path(__path__, __name__)


def non_empty_value(value): return value != '' and value is not None and value != []


def join_args(values): return '&'.join(list(filter(non_empty_value, values))).strip()


def api_url(): return os.env.get('API_URL', 'https://api.hestia.earth')


def search_url(): return os.getenv('SEARCH_URL', 'https://search.hestia.earth')


def request_url(base_url: str, **kwargs):
    args = list(map(lambda key: '='.join([key, str(kwargs.get(key))]), kwargs.keys()))
    return f"{base_url}?{join_args(args)}"


def download_hestia(node_id: str, node_type=SchemaType.TERM, mode=''):
    # try to download file from s3 first, if fail use api
    try:
        import boto3
        file_key = f"{node_type.value}/{node_id}.jsonld"
        return json.loads(boto3.client('s3').get_object(Bucket=os.getenv('AWS_BUCKET'), Key=file_key)['Body'].read())
    except Exception:
        url = request_url(f"{api_url()}/download", type=node_type.value, id=node_id, mode=mode)
        return requests.get(url).json()
    except requests.exceptions.RequestException:
        return None


def find_node(node_type: SchemaType, args: dict, limit=10):
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {key: args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    hits = requests.post(search_url(), json.dumps({
        'query': {'bool': {'must': must}},
        'limit': limit,
        '_source': {'includes': ['name', '@id']}
    }), headers=headers).json()['hits']['hits']
    return list(map(lambda res: res.get('_source'), hits))


def find_node_exact(node_type: SchemaType, args: dict):
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {key: args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    hits = requests.post(search_url(), json.dumps({
        'query': {'bool': {'must': must}},
        'limit': 2,
        '_source': {'includes': ['name', '@id']}
    }), headers=headers).json()['hits']['hits']
    # do not return a duplicate
    return hits[0].get('_source') if len(hits) == 1 else None
