# json pointer identifying collection
OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_JSONPOINTER = None

# A filter that denotes a collection. Can be either a path interpreted by Q
# or a callable taking search and a list of allowed collection identifiers
# returning Q/ES bool
# (search: RecordsSearch = None, collections=["A", "B"], **kwargs) => Q|Bool
OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_FILTER = 'collection'

#
# If collection filter above is not a path but callable, one needs to supply permission
# handler. It takes (allowed_collections=["A", "B"], record=<instance of Record>, **kwargs)
# and should return an instance of a class having 'can()' method (such as Permission class).
#
OAREPO_ENROLLMENT_PERMISSIONS_COLLECTION_PERMISSION_HANDLER = None

# A filter for filtering records. Can be either a path interpreted by Q
# or a callable taking search and a list of allowed record uuids
# returning Q/ES bool
# (search: RecordsSearch = None, record_uuids=["A", "B"], **kwargs) => Q|Bool
#
# normally there is no need to override this
OAREPO_ENROLLMENT_PERMISSIONS_RECORD_FILTER = '_id'
