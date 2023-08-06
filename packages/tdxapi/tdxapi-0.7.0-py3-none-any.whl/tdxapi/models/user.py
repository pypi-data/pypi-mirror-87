import attr

from tdxapi.enums.time_zone import TimeZone
from tdxapi.enums.user_type import UserType
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList
from tdxapi.models.user_application import UserApplication


@attr.s(kw_only=True)
class User(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Users.User"

    #: The UID of the user.
    uid = attr.ib(default=None, converter=to_uid, metadata={"tdx_name": "UID"})

    #: The UID of the organization associated with the user.
    beid = attr.ib(default=None, converter=to_uid, metadata={"tdx_name": "BEID"})

    #: The integer ID of the organization associated with the user.
    beid_int = attr.ib(default=None, metadata={"tdx_name": "BEIDInt"})

    #: The active status of the user.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The confidential status of the user.
    is_confidential = attr.ib(default=None, metadata={"tdx_name": "IsConfidential"})

    #: The username of the user.
    username = attr.ib(default=None, metadata={"tdx_name": "UserName"})

    #: The full name of the user.
    full_name = attr.ib(default=None, metadata={"tdx_name": "FullName"})

    #: The first name of the user.
    first_name = attr.ib(default=None, metadata={"tdx_name": "FirstName"})

    #: The last name of the user.
    last_name = attr.ib(default=None, metadata={"tdx_name": "LastName"})

    #: The middle name of the user.
    middle_name = attr.ib(default=None, metadata={"tdx_name": "MiddleName"})

    #: The salutation of the user.
    salutation = attr.ib(default=None, metadata={"tdx_name": "Salutation"})

    #: The nickname of the user.
    nickname = attr.ib(default=None, metadata={"tdx_name": "Nickname"})

    #: The ID of the default account/department associated with the user.
    default_account_id = attr.ib(
        default=None, metadata={"tdx_name": "DefaultAccountID"}
    )

    #: The name of the default account/department associated with the user.
    default_account_name = attr.ib(
        default=None, metadata={"tdx_name": "DefaultAccountName"}
    )

    #: The primary email address of the user.
    primary_email = attr.ib(default=None, metadata={"tdx_name": "PrimaryEmail"})

    #: The alternate email address of the user.
    alternate_email = attr.ib(default=None, metadata={"tdx_name": "AlternateEmail"})

    #: The organizational ID of the user.
    external_id = attr.ib(default=None, metadata={"tdx_name": "ExternalID"})

    #: The alternate ID of the user.
    alternate_id = attr.ib(default=None, metadata={"tdx_name": "AlternateID"})

    #: The system-defined (non-platform) applications associated with the user.
    sys_apps = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "Applications"}
    )

    #: The name of the global security role associated with the user.
    security_role_name = attr.ib(
        default=None, metadata={"tdx_name": "SecurityRoleName"}
    )

    #: The UID of the global security role associated with the user.
    security_role_id = attr.ib(default=None, metadata={"tdx_name": "SecurityRoleID"})

    #: The global security role permissions associated with the user.
    permissions = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "Permissions"}
    )

    #: The organizationally-defined (platform) applications associated with the user.
    apps = attr.ib(
        default=attr.Factory(list),
        converter=UserApplication.from_data,
        metadata={"tdx_name": "OrgApplications"},
    )

    #: The ID of the primary client portal application associated with the user.
    primary_client_portal_app_id = attr.ib(
        default=None, metadata={"tdx_name": "PrimaryClientPortalApplicationID"}
    )

    #: The IDs of the groups associated with the user.
    group_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "GroupIDs"})

    #: The integer ID of the user.
    ref_id = attr.ib(default=None, metadata={"tdx_name": "ReferenceID"})

    #: The alert email address of the user where system notifications are delivered.
    alert_email = attr.ib(default=None, metadata={"tdx_name": "AlertEmail"})

    #: The profile image file name of the user.
    profile_image_file_name = attr.ib(
        default=None, metadata={"tdx_name": "ProfileImageFileName"}
    )

    #: The company of the user.
    company = attr.ib(default=None, metadata={"tdx_name": "Company"})

    #: The title of the user.
    title = attr.ib(default=None, metadata={"tdx_name": "Title"})

    #: The home phone number of the user.
    home_phone = attr.ib(default=None, metadata={"tdx_name": "HomePhone"})

    #: The primary phone number of the user.
    primary_phone = attr.ib(default=None, metadata={"tdx_name": "PrimaryPhone"})

    #: The work phone number of the user.
    work_phone = attr.ib(default=None, metadata={"tdx_name": "WorkPhone"})

    #: The pager number of the user.
    pager = attr.ib(default=None, metadata={"tdx_name": "Pager"})

    #: The other phone number of the user.
    other_phone = attr.ib(default=None, metadata={"tdx_name": "OtherPhone"})

    #: The mobile phone number of the user.
    mobile_phone = attr.ib(default=None, metadata={"tdx_name": "MobilePhone"})

    #: The fax number of the user.
    fax = attr.ib(default=None, metadata={"tdx_name": "Fax"})

    #: The ID of the default priority associated with the user.
    default_priority_id = attr.ib(
        default=None, metadata={"tdx_name": "DefaultPriorityID"}
    )

    #: The name of the default priority associated with the user.
    default_priority_name = attr.ib(
        default=None, metadata={"tdx_name": "DefaultPriorityName"}
    )

    #: The "About Me" information associated with the user.
    about_me = attr.ib(default=None, metadata={"tdx_name": "AboutMe"})

    #: The work address of the user.
    work_address = attr.ib(default=None, metadata={"tdx_name": "WorkAddress"})

    #: The work city of the user.
    work_city = attr.ib(default=None, metadata={"tdx_name": "WorkCity"})

    #: The work state abbreviation of the user.
    work_state = attr.ib(default=None, metadata={"tdx_name": "WorkState"})

    #: The work zip code of the user.
    work_zip = attr.ib(default=None, metadata={"tdx_name": "WorkZip"})

    #: The work country of the user.
    work_country = attr.ib(default=None, metadata={"tdx_name": "WorkCountry"})

    #: The home address of the user.
    home_address = attr.ib(default=None, metadata={"tdx_name": "HomeAddress"})

    #: The home city of the user.
    home_city = attr.ib(default=None, metadata={"tdx_name": "HomeCity"})

    #: The home state abbreviation of the user.
    home_state = attr.ib(default=None, metadata={"tdx_name": "HomeState"})

    #: The home zip code of the user.
    home_zip = attr.ib(default=None, metadata={"tdx_name": "HomeZip"})

    #: The home country of the user.
    home_country = attr.ib(default=None, metadata={"tdx_name": "HomeCountry"})

    #: The ID of the location associated with the user.
    location_id = attr.ib(default=None, metadata={"tdx_name": "LocationID"})

    #: The name of the location associated with the user.
    location_name = attr.ib(default=None, metadata={"tdx_name": "LocationName"})

    #: The ID of the location room associated with the user.
    location_room_id = attr.ib(default=None, metadata={"tdx_name": "LocationRoomID"})

    #: The name of the location room associated with the user.
    location_room_name = attr.ib(
        default=None, metadata={"tdx_name": "LocationRoomName"}
    )

    #: The default bill rate of the user.
    default_rate = attr.ib(default=None, metadata={"tdx_name": "DefaultRate"})

    #: The cost rate of the user.
    cost_rate = attr.ib(default=None, metadata={"tdx_name": "CostRate"})

    #: The employee status of the user.
    is_employee = attr.ib(default=None, metadata={"tdx_name": "IsEmployee"})

    #: The number of workable hours in a work day for the user.
    workable_hours = attr.ib(default=None, metadata={"tdx_name": "WorkableHours"})

    #: Whether the user's capacity is managed, meaning they can have capacity and will
    #: appear on capacity/availability reports.
    is_capacity_managed = attr.ib(
        default=None, metadata={"tdx_name": "IsCapacityManaged"}
    )

    #: The date after which the user should start reporting time. This also governs
    #: capacity calculations.
    report_time_start_date = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ReportTimeAfterDate"},
    )

    #: The date after which the user is no longer available for scheduling and no longer
    #: required to log time.
    report_time_end_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDate"}
    )

    #: Whether the user should report time.
    should_report_time = attr.ib(
        default=None, metadata={"tdx_name": "ShouldReportTime"}
    )

    #: The UID of the person who the user reports to.
    reports_to_uid = attr.ib(default=None, metadata={"tdx_name": "ReportsToUID"})

    #: The full name of the person who the user reports to.
    reports_to_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ReportsToFullName"}
    )

    #: The ID of the resource pool associated with the user.
    resource_pool_id = attr.ib(default=None, metadata={"tdx_name": "ResourcePoolID"})

    #: The name of the resource pool associated with the user.
    resource_pool_name = attr.ib(
        default=None, metadata={"tdx_name": "ResourcePoolName"}
    )

    #: The time zone associated with the user.
    tz = attr.ib(
        default=TimeZone.DEFAULT, converter=TimeZone, metadata={"tdx_name": "TZID"}
    )

    #: The name of the time zone associated with the user.
    tzname = attr.ib(default=None, metadata={"tdx_name": "TZName"})

    #: The type of the user.
    type_id = attr.ib(default=None, converter=UserType, metadata={"tdx_name": "TypeID"})

    #: The authentication username of the user, used for authenticating with
    #: non-TeamDynamix authentication types.
    authentication_username = attr.ib(
        default=None, metadata={"tdx_name": "AuthenticationUserName"}
    )

    #: The ID of the authentication provider the new user will use for authentication.
    authentication_provider_id = attr.ib(
        default=None, metadata={"tdx_name": "AuthenticationProviderID"}
    )

    #: The custom attributes associated with the user.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )

    #: The Instant Messenger (IM) provider associated with the user.
    im_provider = attr.ib(default=None, metadata={"tdx_name": "IMProvider"})

    #: The Instant Messenger (IM) username/handle associated with the user.
    im_handle = attr.ib(default=None, metadata={"tdx_name": "IMHandle"})
