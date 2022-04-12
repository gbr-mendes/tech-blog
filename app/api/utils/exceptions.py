from rest_framework.exceptions import APIException

class PostNotFound(APIException):
    status_code = 400
    default_detail = "We couldn't find the requested post!"
    default_code = "post_not_found"


class UUIDInvalid(APIException):
    status_code = 400
    default_detail = "UUID passed as parameter is invalid"
    default_code = "invalid_uuid"
