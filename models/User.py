""" User Model """

from masoniteorm.models import Model
from masoniteorm.relationships import has_one
from masoniteorm.scopes import UUIDPrimaryKeyMixin

class User(Model, UUIDPrimaryKeyMixin):
    """User Model"""

    __hidden__ = ["password", "created_at", "is_active", "is_verified"]

    __uuid_version__ = 4

    __primary_key__ = "id"

    __primary_key_type__ = "str"

    __force_update__ = True

