__version__ = '1.0.0'

from .sso import get_boto3_session, login, list_available_roles
from .assignments import list_assignments
