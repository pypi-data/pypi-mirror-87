from enum import Enum


class LicenseType(Enum):
    """Types of licenses that are used to configure security roles."""

    __tdx_type__ = "TeamDynamix.Api.Roles.LicenseTypes"

    NONE = 0
    ENTERPRISE = 1
    PROJECT_MANAGER = 2
    TECHNICIAN = 3
    TEAM_MEMBER = 4
    STUDENT_TECHNICIAN = 5
    CLIENT = 6
    CLIENT_WITH_REPORTING = 7
    PROJECT_MANAGER_WITH_REPORTING = 8
    TECHNICIAN_WITH_REPORTING = 9
    TEAM_MEMBER_WITH_REPORTING = 10
