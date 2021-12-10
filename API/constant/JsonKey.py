
class JsonKey(object):
    ERRORS = "errors"

    class UserProfile(object):
        ID = "id"
        LOGIN = "login"
        PASSWORD = "password"
        COUNTRY_ID = "country_id"

        COUNTRY = "country"

    class Countries(object):
        ID = "id"
        TITLE = "title"
        PREFIX = "prefix"

    class Types(object):
        ID = "id"
        RU_TITLE = "ru_title"
        EN_TITLE = "en_title"

    class Histories(object):
        ID = "id"
        USER_ID = "user_id"
        TYPE_ID = "type_id"
        DATE = "date"
        DESCRIPTION = "description"