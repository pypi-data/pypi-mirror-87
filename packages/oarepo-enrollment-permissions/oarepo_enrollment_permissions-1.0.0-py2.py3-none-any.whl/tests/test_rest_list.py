from pprint import pprint

from invenio_search import RecordsSearch as InvenioRecordsSearch


def test_has_records(api_client, es, sample_records):
    data = InvenioRecordsSearch(index='test-records-record').execute()
    assert data['hits']['total']['value'] > 0


def test_rest_list_anonymous_default_access(api_client, es, sample_records):
    resp = api_client.get('/records-no-security/')
    assert resp.status_code == 200
    pprint(resp.json)
    assert resp.json['hits']['total'] == 0


def test_rest_list_anonymous_custom_access(api_client, es, sample_records):
    resp = api_client.get('/records-anonymous-custom/')
    assert resp.status_code == 200
    assert resp.json['hits']['total'] == 2  # 2 records in collection A


def test_rest_list_anonymous_custom_callable_access(api_client, es, sample_records):
    resp = api_client.get('/records-anonymous-custom-callable/')
    assert resp.status_code == 200
    assert resp.json['hits']['total'] == 2  # 2 records in collection A


def test_rest_list_no_access_user(api_client, es, sample_records, login, no_access_user):
    assert api_client.get(f'_tests/_login/{no_access_user.id}').status_code == 200
    resp = api_client.get('/records-security/')
    assert resp.status_code == 200
    assert resp.json['hits']['total'] == 0  # 2 records in collection A


def test_rest_list_granted_user(api_client, es, sample_records, login,
                                enrolled_user, collection_enrollment):
    assert api_client.get(f'_tests/_login/{enrolled_user.id}').status_code == 200
    resp = api_client.get('/records-security/')
    assert resp.status_code == 200
    assert resp.json['hits']['total'] == 2  # 2 records in collection A


def test_rest_list_record_user(
    api_client, es, sample_records, login,
    record_user):

    assert api_client.get(f'_tests/_login/{record_user.id}').status_code == 200
    resp = api_client.get('/records-security/')
    assert resp.status_code == 200
    assert resp.json['hits']['total'] == 2  # 2 records, one in A and one in B
    recs_by_collection = {}
    hits = resp.json['hits']['hits']
    recs_by_collection[hits[0]['metadata']['collection']] = hits[0]['metadata']
    recs_by_collection[hits[1]['metadata']['collection']] = hits[1]['metadata']

    assert len(recs_by_collection) == 2

    assert recs_by_collection['A']['control_number'] == sample_records['A'][0].pid.pid_value
    assert recs_by_collection['B']['control_number'] == sample_records['B'][0].pid.pid_value
