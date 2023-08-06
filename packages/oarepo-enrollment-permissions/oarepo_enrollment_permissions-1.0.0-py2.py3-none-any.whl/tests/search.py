from elasticsearch_dsl import Q
from flask_login import current_user
from invenio_records_rest.utils import allow_all, deny_all

from oarepo_enrollment_permissions import RecordsSearch
from oarepo_enrollment_permissions.permissions import read_permission_factory


class CustomAnonymousRecordsSearch(RecordsSearch):
    class Meta:
        default_anonymous_filter = Q('term', collection='A')


class CustomAnonymousRecordsCallableSearch(RecordsSearch):
    class Meta:
        @classmethod
        def default_anonymous_filter(cls, search=None, **kwargs):
            assert search
            return Q('term', collection='A')


class RecordsSecuritySearch(RecordsSearch):
    pass


def anonymous_get_read_permission_factory(*args, **kwargs):
    if current_user.is_anonymous:
        if kwargs['record']['collection'] == 'A':
            return allow_all()
        else:
            return deny_all()
    return read_permission_factory(*args, **kwargs)
