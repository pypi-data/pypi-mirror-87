from elasticsearch_dsl import FacetedResponse as ESFacetedResponse, FacetedSearch, Q
from elasticsearch_dsl.query import Bool
from elasticsearch_dsl.response import Response as ESResponse
from flask_login import current_user
from invenio_search import RecordsSearch as InvenioRecordsSearch
from invenio_search.api import MinShouldMatch
from invenio_search.utils import build_alias_name

from oarepo_enrollment_permissions.proxies import current_enrollment_permissions


class Response(ESResponse):
    # TODO: filter results metadata here
    pass


class FacetedResponse(ESFacetedResponse):
    # TODO: filter results metadata here
    pass


class RecordsSearchMixin(InvenioRecordsSearch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._response_class = Response

        if current_user.is_anonymous:
            self._filter_anonymous_user()
            return

        self._make_default_filter_callable()

        flt = self._make_current_user_filter()
        if not flt:
            return

        if self.query:
            # there was a default filter applied, wrap it up
            mode = getattr(self.Meta, 'default_filter_mode', 'or')
            if mode == 'or':
                self.query = Bool(
                    minimum_should_match=MinShouldMatch("0<1"),
                    filter=[
                        Bool(should=[*flt, self.query], minimum_should_match=1)
                    ])
            elif mode == 'and':
                self.query = Bool(
                    minimum_should_match=MinShouldMatch("0<1"),
                    filter=[*flt, self.query])
        else:
            self.query = Bool(minimum_should_match=MinShouldMatch("0<1"), filter=flt)

    def _make_default_filter_callable(self):
        # handling callable in default filter
        default_filter = getattr(self.Meta, 'default_filter_factory', None)
        if default_filter:
            default_filter = default_filter(search=self)
            # replace query with the result of the callable filter
            self.query = Bool(minimum_should_match=MinShouldMatch("0<1"),
                              filter=default_filter)

    def _filter_anonymous_user(self):
        # anonymous user
        default_anonymous_filter = getattr(self.Meta, 'default_anonymous_filter', None)
        if default_anonymous_filter:
            if callable(default_anonymous_filter):
                default_anonymous_filter = default_anonymous_filter(search=self)

            self.query = Bool(minimum_should_match=MinShouldMatch("0<1"),
                              filter=default_anonymous_filter)
            return

        # otherwise the anonymous user is denied access
        self.query = self.match_none_filter

    def _make_current_user_filter(self):
        filters = current_enrollment_permissions.get_user_elasticsearch_filters(self, current_user)
        if not filters:
            return [Q('match_none')]
        return filters

    @property
    def match_none_filter(self):
        return Bool(minimum_should_match=MinShouldMatch("0<1"),
                    filter=Q('match_none'))

    @classmethod
    def faceted_search(cls, query=None, filters=None, search=None):
        search_ = search or cls()

        class RecordsFacetedSearch(FacetedSearch):
            """Pass defaults from ``cls.Meta`` object."""

            index = build_alias_name(search_._index[0])
            doc_types = getattr(search_.Meta, 'doc_types', ['*'])
            fields = getattr(search_.Meta, 'fields', ('*',))
            facets = getattr(search_.Meta, 'facets', {})

            def search(self):
                return search_.response_class(FacetedResponse)

        return RecordsFacetedSearch(query=query, filters=filters or {})


RecordsSearch = RecordsSearchMixin
