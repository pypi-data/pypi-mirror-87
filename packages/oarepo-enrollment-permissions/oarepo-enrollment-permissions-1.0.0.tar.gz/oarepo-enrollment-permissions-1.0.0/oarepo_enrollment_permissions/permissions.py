from flask import request
from flask_login import current_user

from oarepo_enrollment_permissions.proxies import current_enrollment_permissions


class PermissionCollection:
    def __init__(self, *permissions, combining_operation='or'):
        self.permissions = permissions
        self.combining_operation = combining_operation

    def can(self):
        if not self.permissions:
            return False
        for perm in self.permissions:
            if perm.can():
                if self.combining_operation == 'or':
                    return True
            else:
                if self.combining_operation == 'and':
                    return False

        return self.combining_operation == 'and'


def read_permission_factory(*args, **kwargs):
    return current_enrollment_permissions.get_action_permission(current_user, 'read', **kwargs)


def update_permission_factory(*args, **kwargs):
    return current_enrollment_permissions.get_action_permission(current_user, 'update', **kwargs)


def delete_permission_factory(*args, **kwargs):
    return current_enrollment_permissions.get_action_permission(current_user, 'delete', **kwargs)


def create_permission_factory(*args, **kwargs):
    return current_enrollment_permissions.get_action_permission(
        current_user, 'create', data=request.json, **kwargs)
