from elasticsearch_dsl import Q
from flask import current_app
from invenio_accounts.models import User
from jsonpointer import resolve_pointer
from oarepo_enrollments import EnrollmentHandler
from sqlalchemy.util import classproperty


class CollectionHandler(EnrollmentHandler):
    cached_collection_filter = None

    def enroll(self, user: User, **kwargs) -> None:
        # this enrollment is enforced dynamically, does not influence data, so just pass
        pass

    def revoke(self, user: User, **kwargs) -> None:
        # this enrollment is enforced dynamically, does not influence data, so just pass
        pass

    @classproperty
    def collection_filter(cls):
        if cls.cached_collection_filter:
            return cls.cached_collection_filter
        cls.cached_collection_filter = \
            current_app.config['OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_FILTER']
        return cls.cached_collection_filter

    @classmethod
    def get_elasticsearch_filter(cls, search=None, queryset=None, **kwargs):
        collections = cls.get_collections(queryset)

        if collections:
            es_filter = getattr(search.Meta, 'permissions_collection_filter', None) or cls.collection_filter
            if callable(es_filter):
                return es_filter(search=search, collections=list(collections), **kwargs)
            return Q('terms', **{es_filter: list(collections)})
        return None

    @classmethod
    def get_collections(cls, queryset):
        collections = set()
        for enrollment in queryset:
            collection = enrollment.external_key
            if not collection:
                continue
            collections.add(collection)
        return collections

    @classmethod
    def get_permission(cls, queryset, record=None, data=None, **kwargs):
        allowed_collections = cls.get_collections(queryset)
        path = cls.collection_filter
        if callable(path):
            handler = current_app.config['OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_PERMISSION_HANDLER']
            if not handler:
                raise NotImplementedError('Please supply OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_PERMISSION_HANDLER')
            return handler(allowed_collections=allowed_collections, record=record, data=data, **kwargs)
        path = convert_path_to_jsonpointer(path)
        collections = resolve_pointer(record or data or {}, path)
        return CollectionPermission(collections, allowed_collections)

    def post_filter_elasticsearch_result(self, search=None, result=None, **kwargs):
        # can be used to hide metadata from results
        pass


def convert_path_to_jsonpointer(path):
    return '/' + path.replace('__', '/')


class CollectionPermission:
    def __init__(self, record_collections, allowed_collections):
        self.record_collections = record_collections
        self.allowed_collections = allowed_collections

    def can(self):
        if isinstance(self.record_collections, (list, tuple)):
            for col in self.record_collections:
                if col in self.allowed_collections:
                    return True
            return False
        return self.record_collections in self.allowed_collections
