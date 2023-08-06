from pprint import pprint


def test_rest_get_anonymous_default_access(api_client, es, sample_records):
    resp = api_client.get(f'/records-no-security/{sample_records["A"][0].pid.pid_value}')
    pprint(resp.data)
    assert resp.status_code == 401


def test_rest_get_anonymous_custom_access(api_client, es, sample_records):
    resp = api_client.get(f'/records-anonymous-custom/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 200
    assert resp.json['metadata'] == dict(sample_records["A"][0].record)

    resp = api_client.get(f'/records-anonymous-custom/{sample_records["B"][0].pid.pid_value}')
    assert resp.status_code == 401


def test_rest_get_no_access(api_client, es, sample_records, no_access_user, login):
    login(api_client, no_access_user.id)
    resp = api_client.get(f'/records-no-security/{sample_records["A"][0].pid.pid_value}')
    pprint(resp.data)
    assert resp.status_code == 403


def test_rest_get_collection_access(api_client, es, sample_records, collection_enrollment, enrolled_user, login):
    login(api_client, enrolled_user.id)
    resp = api_client.get(f'/records-security/{sample_records["B"][0].pid.pid_value}')
    assert resp.status_code == 200
    assert resp.json['metadata'] == dict(sample_records["B"][0].record)

    resp = api_client.get(f'/records-anonymous-custom/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 403


def test_rest_get_record_user(api_client, es, sample_records, login, record_user):
    login(api_client, record_user.id)
    resp = api_client.get(f'/records-security/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 200
    assert resp.json['metadata'] == dict(sample_records["A"][0].record)

    resp = api_client.get(f'/records-security/{sample_records["B"][0].pid.pid_value}')
    assert resp.status_code == 200
    assert resp.json['metadata'] == dict(sample_records["B"][0].record)

    resp = api_client.get(f'/records-security/{sample_records["A"][1].pid.pid_value}')
    assert resp.status_code == 403

    resp = api_client.get(f'/records-security/{sample_records["B"][1].pid.pid_value}')
    assert resp.status_code == 403
