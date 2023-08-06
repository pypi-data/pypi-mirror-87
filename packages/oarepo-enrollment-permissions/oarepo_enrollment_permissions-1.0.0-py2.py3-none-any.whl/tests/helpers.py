import uuid
from collections import namedtuple

from flask_security import login_user
from invenio_accounts.models import User
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.minters import recid_minter
from invenio_records import Record

from oarepo_enrollment_permissions.handlers.collection import CollectionHandler


def test_login(user_id=None):
    login_user(User.query.get(user_id), remember=True)
    return 'OK'


class LiteEntryPoint:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def load(self):
        return self.val


def extra_entrypoints(app, group=None, name=None):
    data = {
        'oarepo_enrollments.enrollments': [
            LiteEntryPoint('collection', CollectionHandler),
        ],
    }

    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


def dedate(x):
    if isinstance(x, list):
        return [dedate(xx) for xx in x]
    if isinstance(x, dict):
        return {
            k: (v if 'timestamp' not in k or not v else '--timestamp--') for k, v in x.items()
        }
    return x


def record_to_index(record):
    return 'test-records-record', '_doc'


PIDRecord = namedtuple('PIDRecord', 'pid record')


def make_sample_record(db, title, collection):
    rec = {
        'title': title,
        'collection': collection
    }
    record_uuid = uuid.uuid4()
    pid = recid_minter(record_uuid, rec)
    rec = Record.create(rec, id_=record_uuid)
    db.session.commit()
    indexer = RecordIndexer()
    indexer.index(rec)
    return PIDRecord(pid, rec)
