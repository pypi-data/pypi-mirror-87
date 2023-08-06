from enum import Enum


class EventTypes(Enum):
    CHANGE_USER = "ChangeUser"
    REGISTERED_USER = "RegisteredUser"
    USER_CHANGED = "UserChanged"


class RegisteredUserEventData:
    auth0_id: str
    email: str
    email_verified: bool
    first_name: str
    id: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, auth0_id: str, email: str, email_verified: bool, first_name: str, id: str, last_name: str, locale: str, picture: str) -> None:
        self.auth0_id = auth0_id
        self.email = email
        self.email_verified = email_verified
        self.first_name = first_name
        self.id = id
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class Metadata:
    trace_id: str
    user_id: str

    def __init__(self, trace_id: str, user_id: str) -> None:
        self.trace_id = trace_id
        self.user_id = user_id


class RegisteredUserEventType(Enum):
    REGISTERED_USER = "RegisteredUser"


class RegisteredUserEvent:
    data: RegisteredUserEventData
    id: str
    metadata: Metadata
    type: RegisteredUserEventType

    def __init__(self, data: RegisteredUserEventData, id: str, metadata: Metadata, type: RegisteredUserEventType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type


class ChangeUserEventData:
    first_name: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, first_name: str, last_name: str, locale: str, picture: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class ChangeUserEventType(Enum):
    CHANGE_USER = "ChangeUser"


class ChangeUserEvent:
    data: ChangeUserEventData
    id: str
    metadata: Metadata
    type: ChangeUserEventType

    def __init__(self, data: ChangeUserEventData, id: str, metadata: Metadata, type: ChangeUserEventType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type


class UserChangedEventData:
    first_name: str
    last_name: str
    locale: str
    picture: str

    def __init__(self, first_name: str, last_name: str, locale: str, picture: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.picture = picture


class UserChangedEventType(Enum):
    USER_CHANGED = "UserChanged"


class UserChangedEvent:
    data: UserChangedEventData
    id: str
    metadata: Metadata
    type: UserChangedEventType

    def __init__(self, data: UserChangedEventData, id: str, metadata: Metadata, type: UserChangedEventType) -> None:
        self.data = data
        self.id = id
        self.metadata = metadata
        self.type = type
