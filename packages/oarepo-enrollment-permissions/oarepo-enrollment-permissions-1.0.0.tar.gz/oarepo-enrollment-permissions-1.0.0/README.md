# oarepo-enrollment-permissions

Work in progress, do not use yet

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]
[![image][8]][9]

[image]: https://img.shields.io/travis/oarepo/oarepo-enrollment-permissions.svg

[1]: https://travis-ci.com/oarepo/oarepo-enrollment-permissions

[2]: https://img.shields.io/coveralls/oarepo/oarepo-enrollment-permissions.svg

[3]: https://coveralls.io/r/oarepo/oarepo-enrollment-permissions

[4]: https://img.shields.io/github/tag/oarepo/oarepo-enrollment-permissions.svg

[5]: https://github.com/oarepo/oarepo-enrollment-permissions/releases

[6]: https://img.shields.io/pypi/dm/oarepo-enrollment-permissions.svg

[7]: https://pypi.python.org/pypi/oarepo-enrollment-permissions

[8]: https://img.shields.io/github/license/oarepo/oarepo-enrollment-permissions.svg

[9]: https://github.com/oarepo/oarepo-enrollment-permissions/blob/master/LICENSE

OArepo Enrollment Permissions library is a bridge between oarepo-enrollment library and invenio records. It provides
means to assign user permission to perform actions upon a record (list, update, delete, custom actions).

## Installation

```bash
pip install oarepo-enrollment-permissions
```

## Usage

1. In your rest configuration, set ``search_class`` class either to
   ``oarepo_enrollment_permissions.RecordsSearch`` or to a class inheriting
   from ``oarepo_enrollment_permissions.RecordsSearchMixin``.
2. If your ``read_permission_factory_imp`` is not ``check_elasticsearch``, be sure to include the result
   of ``oarepo_enrollment_permissions.read_permission_factory``
   in your permission factory - see below for details).
3. Use ``oarepo_enrollment_permissions.update_permission_factory`` as your update permission factory (or call if from
   your own permission factory - see below for details).
4. Use ``oarepo_enrollment_permissions.delete_permission_factory`` as your delete permission factory (or call if from
   your own permission factory - see below for details).
5. Use ``oarepo_enrollment_permissions.create_permission_factory`` as your create permission factory (or call if from
   your own permission factory - see below for details).

Now you are all set, no one has an access until granted.

## Granting access

Access is granted via enrollment process. The following enrollment types are available:

### Collection

Gives rights to manipulate with a collection. A collection is defined as records with the same values at a given json
pointer (specified in configuration or passed to the enroll call).

To grant access to a collection on command-line, call:

```bash
invenio oarepo:enroll collection <email> <collection key> actions=read,update,delete,create
```

If you want to perform the same in REST API, call:

```json5
{
    'enrollment_type': "collection",
    'recipient': "someone@example.com",
    'external_key': 'test',
    'operation': 'read'
    // either comma separated or an array
}
```

### Single record

You can grant rights to a single record as well. To do that, invoke:

```bash
invenio oarepo:enroll record <email> <record_uuid> actions=read,update,delete
```

Again, the same can be achieved via API:

```json5
{
    'enrollment_type': "record",
    'recipient': "someone@example.com",
    'external_key': '1234-...-1234',
    'operation': 'read'
    // either comma separated or an array
}
```

## Listing and Revoking access

See ``oarepo-enrollment`` for help with these.

## Customizing search/listing permissions

The provided search class (or mixin) behaves a bit differently than the default invenio RecordsSearch. For anonymous
users, the default behaviour is to return empty collection. For authenticated users, enrollments are inspected and are
used to filter the records.

This process can be customized via:

```python
from oarepo_enrollment_permissions import RecordsSearch


class MyRecordsSearch(RecordsSearch):
    class Meta:
        # put customizations in here
        pass
```

### Anonymous user

If anonymous user should get access to all/some records, specify ``default_anonymous_filter``
property on Meta class.

This property can be either elasticsearch query (Q, Bool) or it might be a function with a signature
``default_anonymous_filter(search=<RecordsSearch>, **kwargs) -> Union[Q, Bool]``. The result of the function is passed
to the default elasticsearch filter.

### Authenticated user

On ``Meta`` class, invenio supports passing ``default_filter``. For convenience reasons this library
adds ``default_filter_factory(search=<RecordsSearch>, **kwargs) -> Union[Q, Bool]`` that takes precedence if used.

At first the library looks at all successful enrollments of the user whose handler contains
``get_elasticsearch_filter`` class method. Then these handlers are called (with the enrollments as parameters) to get
filtering query.

There might be a ``default_filter`` defined on the search. If it is, the queries from handlers are combined with the
default filter depending on the value of ``default_filter_mode`` ``Meta`` property:

* ``or`` (the default value) - user is granted access if either ``default_filter`` or at least one of handler filters
  match
* ``and`` - user is granted access if ``default_filter`` and at least one of handler filters match.

If there is no ``default_filter`` used, user is granted access to the record if at least one of handler filters match.

## API

### Implementing custom permission-enabled enrollment handler

To implement a custom permission-enabled handler, add the following methods:

```python

from oarepo_enrollments import EnrollmentHandler
from invenio_accounts.models import User
from elasticsearch_dsl import Q


class MyCollectionAccess(EnrollmentHandler):
    def enroll(self, user: User, role=None, **kwargs) -> None:
        # no handling required for collections
        pass

    def revoke(self, user: User, role=None, **kwargs) -> None:
        # no handling required for collections
        pass

    def get_elasticsearch_filter(self, search=None, queryset=None, **kwargs):
        collections = []
        for enrollment in queryset:
            collection = enrollment.extra_data.get('collection')
            if collection:
                collections.append(collection)
        if collections:
            return Q('terms', collections=collections)
        return None

    def post_filter_elasticsearch_result(self, search=None, result=None, **kwargs):
        # can be used to hide metadata from results
        pass
```

## Configuration

### Collection permissions configuration

To use builtin collection permissions, you have to specify the path or query for filtering collections. There are two
ways of doing that - global and per-search.

#### Global configuration

In your config file, set:

```python
OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_FILTER = 'collection'
```

This can be either path in the document that will be placed to ``Q('terms', <path> = [allowed collections])``
or it might be a callable ``(search=None, collections=None, **)`` that should return either elasticsearch ``Q``
or ``Bool``.

#### Local configuration

Alternatively, define the path/callable on Meta:

```python
from oarepo_enrollment_permissions import RecordsSearch
from elasticsearch_dsl import Q


class MyRecordsSearch(RecordsSearch):
    class Meta:
        permissions_collection_filter = 'collections'

        # or

        @classmethod
        def permissions_collection_filter(cls, search=None, collections=None, **kwargs):
            return Q('terms', collection__key=collections)
```

### Record permissions configuration

Normally there is no need to override record configuration.
