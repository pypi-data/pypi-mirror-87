import json
from pprint import pprint


def test_rest_create_anonymous_default_access(api_client, es, sample_records):
    resp = api_client.post(f'/records-security/', data=json.dumps({
        'collection': 'A',
        'title': 'created test'
    }), headers={'content-type': 'application/json'})
    pprint(resp.data)
    assert resp.status_code == 401


def test_rest_create_user_no_rights(api_client, es, sample_records, login, record_user):
    login(api_client, record_user.id)
    resp = api_client.post(f'/records-security/', data=json.dumps({
        'collection': 'A',
        'title': 'created test'
    }), headers={'content-type': 'application/json'})
    pprint(resp.data)
    assert resp.status_code == 403


def test_rest_create_user_collection_rights(api_client, es, sample_records, login, record_creating_user):
    login(api_client, record_creating_user.id)
    resp = api_client.post(f'/records-security/', data=json.dumps({
        'collection': 'A',
        'title': 'created test'
    }), headers={'content-type': 'application/json'})
    pprint(resp.data)
    assert resp.status_code == 201

    resp = api_client.post(f'/records-security/', data=json.dumps({
        'collection': 'B',
        'title': 'created test'
    }), headers={'content-type': 'application/json'})
    pprint(resp.data)
    assert resp.status_code == 403
