from flask import request
from flask_principal import Permission
from invenio_records_rest.utils import deny_all
from oarepo_enrollments.proxies import current_enrollments
from oarepo_enrollments import Enrollment
from werkzeug.utils import cached_property

from . import config
from .permissions import PermissionCollection


class OARepoEnrollmentPermissionsState:
    def __init__(self, app):
        self.app = app

    @cached_property
    def permission_handlers(self):
        return {
            enrollment_type: handler for enrollment_type, handler in current_enrollments.handlers.items()
            if hasattr(handler, 'get_elasticsearch_filter')
        }

    @cached_property
    def permission_enrollment_types(self):
        return self.permission_handlers.keys()

    def get_user_elasticsearch_filters(self, search, user, action='read'):
        enrollments = Enrollment.query.filter(
            Enrollment.enrolled_user == user,
            Enrollment.state == Enrollment.SUCCESS,
            Enrollment.actions.any(action)
        )
        ret = []
        for enrollment_type, handler in self.permission_handlers.items():
            filter_query = current_enrollments.handlers[enrollment_type].get_elasticsearch_filter(
                search=search,
                queryset=enrollments.filter(Enrollment.enrollment_type == enrollment_type),
                indices=getattr(search, '_original_index', getattr(search, '_index', None))
            )
            if filter_query:
                ret.append(filter_query)
        return ret

    def get_action_permission(self, user, action, **kwargs):
        if user.is_anonymous:
            return deny_all()

        enrollments = Enrollment.query.filter(
            Enrollment.enrolled_user == user,
            Enrollment.state == Enrollment.SUCCESS,
            Enrollment.actions.any(action)
        )
        print(enrollments)
        ret = []
        for enrollment_type, handler in self.permission_handlers.items():
            perm = current_enrollments.handlers[enrollment_type].get_permission(
                queryset=enrollments.filter(Enrollment.enrollment_type == enrollment_type),
                **kwargs
            )
            if perm:
                ret.append(perm)
        if not ret:
            return deny_all()
        return PermissionCollection(*ret)


class OARepoEnrollmentPermissionsExt:
    def __init__(self, app, db=None):
        app.extensions['oarepo-enrollment-permissions'] = OARepoEnrollmentPermissionsState(app)
        self.init_config(app)

    def init_config(self, app):
        for k in dir(config):
            if k.startswith('OAREPO_ENROLLMENT_PERMISSIONS'):
                v = getattr(config, k)
                app.config.setdefault(k, v)
