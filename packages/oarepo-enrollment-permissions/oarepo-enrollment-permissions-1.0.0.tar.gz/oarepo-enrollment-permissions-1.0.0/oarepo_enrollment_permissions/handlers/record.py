from elasticsearch_dsl import Q
from flask import current_app
from invenio_accounts.models import User
from oarepo_enrollments import EnrollmentHandler, Enrollment
from sqlalchemy.util import classproperty


class RecordHandler(EnrollmentHandler):
    cached_record_filter = None

    def enroll(self, user: User, **kwargs) -> None:
        # this enrollment is enforced dynamically, does not influence data, so just pass
        pass

    def revoke(self, user: User, **kwargs) -> None:
        # this enrollment is enforced dynamically, does not influence data, so just pass
        pass

    @classproperty
    def record_filter(cls):
        if cls.cached_record_filter:
            return cls.cached_record_filter
        cls.cached_record_filter = \
            current_app.config['OAREPO_ENROLLMENT_PERMISSIONS_RECORD_FILTER']
        return cls.cached_record_filter

    @classmethod
    def get_elasticsearch_filter(cls, search=None, queryset=None, indices=None, **kwargs):
        records = []
        for enrollment in queryset:
            record = enrollment.external_key
            if not record:
                continue
            records.append(record)

        if records:
            es_filter = getattr(search.Meta, 'permissions_record_filter', None) or cls.record_filter
            if callable(es_filter):
                return es_filter(search=search, record_uuids=records, **kwargs)
            return Q('terms', **{es_filter: records})
        return None

    @classmethod
    def get_permission(cls, queryset, record=None, **kwargs):
        return RecordPermission(queryset, record)

    def post_filter_elasticsearch_result(self, search=None, result=None, **kwargs):
        # can be used to hide metadata from results
        pass


class RecordPermission:
    def __init__(self, queryset, record):
        self.queryset = queryset
        self.record = record

    def can(self):
        return self.record and self.queryset.filter(Enrollment.external_key == str(self.record.id)).count() > 0
