import json


def test_rest_update_anonymous(api_client, es, sample_records):
    resp = api_client.patch(
        f'/records-security/{sample_records["A"][0].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 401


def test_rest_update_not_authorized(api_client, es, sample_records, login, enrolled_user):
    login(api_client, enrolled_user.id)

    resp = api_client.patch(
        f'/records-security/{sample_records["A"][0].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 403


def test_rest_update_authorized(api_client, es, sample_records, login, record_updating_user):
    login(api_client, record_updating_user.id)

    resp = api_client.patch(
        f'/records-security/{sample_records["A"][0].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 200

    resp = api_client.patch(
        f'/records-security/{sample_records["A"][1].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 200

    resp = api_client.patch(
        f'/records-security/{sample_records["B"][0].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 200

    # user has rights for the whole collection A and just B[0]
    resp = api_client.patch(
        f'/records-security/{sample_records["B"][1].pid.pid_value}',
        data=json.dumps([{'path': '/title', 'op': 'replace', 'value': 'test'}]),
        headers={'content-type': 'application/json-patch+json'}
    )
    assert resp.status_code == 403
