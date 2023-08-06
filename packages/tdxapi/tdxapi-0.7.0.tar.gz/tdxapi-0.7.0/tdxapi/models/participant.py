import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Participant(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Feed.Participant"

    #: The full name of the participant.
    full_name = attr.ib(default=None, metadata={"tdx_name": "FullName"})

    #: The email address of the participant.
    email = attr.ib(default=None, metadata={"tdx_name": "Email"})
