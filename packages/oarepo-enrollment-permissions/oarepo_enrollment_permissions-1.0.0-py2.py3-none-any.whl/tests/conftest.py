import os

import pytest
from flask import Blueprint
from invenio_accounts.models import User
from invenio_app.factory import create_app as factory_app
from invenio_indexer.api import RecordIndexer
from invenio_search import current_search
from oarepo_enrollments.models import Enrollment

from oarepo_enrollment_permissions import RecordsSearch
from oarepo_enrollment_permissions.permissions import read_permission_factory, update_permission_factory, \
    delete_permission_factory, create_permission_factory
from .helpers import test_login, make_sample_record
from .search import CustomAnonymousRecordsSearch, CustomAnonymousRecordsCallableSearch, RecordsSecuritySearch, \
    anonymous_get_read_permission_factory

import logging

logging.basicConfig()
logging.getLogger('elasticsearch').setLevel(logging.DEBUG)


@pytest.fixture(scope="module")
def create_app():
    """Return invenio app."""
    return factory_app


@pytest.fixture()
def api(app):
    current_api = app.wsgi_app.mounts['/api']
    with current_api.app_context():
        yield current_api


def gen_rest_endpoint(search_class, path, custom_read_permission_factory=None):
    return dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        search_class=search_class,
        indexer_class=RecordIndexer,
        search_index='test-records-record',
        search_type='_doc',
        record_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_search'),
        },
        list_route=f'/{path}/',
        item_route=f'/{path}/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=create_permission_factory,
        delete_permission_factory_imp=delete_permission_factory,
        update_permission_factory_imp=update_permission_factory,
        read_permission_factory_imp=custom_read_permission_factory or read_permission_factory,
    )


@pytest.fixture(scope="module")
def app_config(app_config):
    """Flask application fixture."""
    app_config = dict(
        TESTING=True,
        JSON_AS_ASCII=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        PREFERRED_URL_SCHEME='https',
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:////tmp/test.sqlite'
            # 'sqlite:///:memory:'
        ),
        SERVER_NAME='localhost',
        MAIL_SUPPRESS_SEND=True,
        SEARCH_ELASTIC_HOSTS=os.environ.get('SEARCH_ELASTIC_HOSTS', None),
        OAREPO_ENROLLMENT_MAIL_TEMPLATES={
            'test-template': {
                'subject': 'subject',
                'body': 'body {{ enrollment_url }}',
                'html': False
            }
        },
        RECORDS_REST_ENDPOINTS={
            'recid': gen_rest_endpoint(RecordsSearch, 'records-no-security'),
            'recid1': gen_rest_endpoint(
                RecordsSecuritySearch, 'records-security'),
            'recid2': gen_rest_endpoint(
                CustomAnonymousRecordsSearch, 'records-anonymous-custom',
                custom_read_permission_factory=anonymous_get_read_permission_factory),
            'recid3': gen_rest_endpoint(CustomAnonymousRecordsCallableSearch, 'records-anonymous-custom-callable'),
        },
        INDEXER_RECORD_TO_INDEX='tests.helpers:record_to_index'
    )
    return app_config


def create_user(db, email):
    u = User()
    u.email = email
    u.active = True
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def granting_user(db):
    return create_user(db, 'granting@example.com')


@pytest.fixture
def enrolled_user(db):
    return create_user(db, 'enrolled@example.com')


@pytest.fixture
def no_access_user(db):
    return create_user(db, 'no_access@example.com')


@pytest.fixture
def record_user(db, sample_records, granting_user):
    user = create_user(db, 'record@example.com')

    enrollment = Enrollment.create('record', str(sample_records["A"][0].pid.object_uuid), user.email, granting_user,
                                   actions=['read'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    enrollment = Enrollment.create('record', str(sample_records["B"][0].pid.object_uuid), user.email, granting_user,
                                   actions=['read'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    db.session.commit()

    return user


@pytest.fixture
def record_creating_user(db, sample_records, granting_user):
    user = create_user(db, 'creating@example.com')

    enrollment = Enrollment.create('collection', "A",
                                   user.email, granting_user,
                                   actions=['create'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    db.session.commit()

    return user


@pytest.fixture
def record_updating_user(db, sample_records, granting_user):
    user = create_user(db, 'updating@example.com')

    enrollment = Enrollment.create('collection', "A",
                                   user.email, granting_user,
                                   actions=['update'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    enrollment = Enrollment.create('record', str(sample_records["B"][0].pid.object_uuid),
                                   user.email, granting_user,
                                   actions=['update'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    db.session.commit()

    return user


@pytest.fixture
def record_deleting_user(db, sample_records, granting_user):
    user = create_user(db, 'deleting@example.com')

    enrollment = Enrollment.create('collection', "A",
                                   user.email, granting_user,
                                   actions=['delete'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    enrollment = Enrollment.create('record', str(sample_records["B"][0].pid.object_uuid),
                                   user.email, granting_user,
                                   actions=['delete'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = user
    db.session.add(enrollment)

    db.session.commit()

    return user


@pytest.fixture
def collection_enrollment(db, granting_user, enrolled_user):
    enrollment = Enrollment.create('collection', 'B', enrolled_user.email, granting_user,
                                   actions=['read'])
    enrollment.state = Enrollment.SUCCESS
    enrollment.enrolled_user = enrolled_user
    db.session.add(enrollment)
    db.session.commit()
    return enrollment


@pytest.fixture()
def login(api):
    """Test blueprint with dynamically added testing endpoints."""
    blue = Blueprint(
        '_tests',
        __name__,
        url_prefix='/_tests/'
    )

    if blue.name in api.blueprints:
        del api.blueprints[blue.name]

    if api.view_functions.get('_tests.test_login') is not None:
        del api.view_functions['_tests.test_login']

    blue.add_url_rule('_login/<user_id>', view_func=test_login)

    api.register_blueprint(blue)

    def do_login(api_client, user_id):
        assert api_client.get(f'_tests/_login/{user_id}').status_code == 200

    return do_login


@pytest.fixture()
def api_client(api):
    with api.test_client() as client:
        yield client


@pytest.fixture()
def sample_records(api, db):
    try:
        current_search.client.indices.delete('test-records-record')
    except:
        pass
    if 'records-record' not in current_search.mappings:
        current_search.register_mappings('records', 'tests.mappings')
    list(current_search.delete())
    list(current_search.create())
    records = {
        'A': [
            make_sample_record(db, 'Test 1 in collection A', 'A'),
            make_sample_record(db, 'Test 2 in collection A', 'A')
        ],
        'B': [
            make_sample_record(db, 'Test 1 in collection B', 'B'),
            make_sample_record(db, 'Test 2 in collection B', 'B')
        ]
    }
    current_search.flush_and_refresh('test-records-record')
    return records
