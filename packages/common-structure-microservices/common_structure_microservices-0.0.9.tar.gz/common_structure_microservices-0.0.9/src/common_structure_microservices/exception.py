from rest_framework.exceptions import APIException


class GenericMicroserviceError(APIException):

    def __init__(self, detail, status):
        self.status_code = status
        super(GenericMicroserviceError, self).__init__(detail)

    status_code = 500
    default_detail = 'Error inesperado'
    default_code = 'generic_microservice_error'
