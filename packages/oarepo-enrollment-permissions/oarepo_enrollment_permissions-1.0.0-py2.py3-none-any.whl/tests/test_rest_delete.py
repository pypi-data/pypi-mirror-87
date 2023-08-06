def test_rest_delete_anonymous(api_client, es, sample_records):
    resp = api_client.delete(
        f'/records-security/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 401


def test_rest_delete_not_authorized(api_client, es, sample_records, login, enrolled_user):
    login(api_client, enrolled_user.id)

    resp = api_client.delete(
        f'/records-security/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 403


def test_rest_delete_authorized(api_client, es, sample_records, login, record_deleting_user, record_updating_user):
    login(api_client, record_updating_user.id)
    resp = api_client.delete(
        f'/records-security/{sample_records["A"][1].pid.pid_value}')
    assert resp.status_code == 403


    login(api_client, record_deleting_user.id)
    resp = api_client.delete(
        f'/records-security/{sample_records["A"][0].pid.pid_value}')
    assert resp.status_code == 204

    resp = api_client.delete(
        f'/records-security/{sample_records["A"][1].pid.pid_value}')
    assert resp.status_code == 204

    resp = api_client.delete(
        f'/records-security/{sample_records["B"][0].pid.pid_value}')
    assert resp.status_code == 204

    # user has rights for the whole collection A and just B[0]
    resp = api_client.delete(
        f'/records-security/{sample_records["B"][1].pid.pid_value}')
    assert resp.status_code == 403
