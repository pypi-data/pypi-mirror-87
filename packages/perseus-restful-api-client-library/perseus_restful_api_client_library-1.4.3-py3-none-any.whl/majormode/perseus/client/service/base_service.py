# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import os

from majormode.perseus.client.api import PerseusConnection
from majormode.perseus.client.api import PerseusSession
from majormode.perseus.model.enum import Enum
from majormode.perseus.model.obj import Object
from majormode.perseus.utils import cast


class BaseService:
    """
    Base class of service.

    It provides logging facility to the inheriting service class.  The
    logger is identifier by the global constant ``LOGGER_NAME`` of
    the Python module ``settings``.

    It also provides facility to publish messages to an Advanced
    Message Queuing Protocol (AMQP) compliant broker, which connection
    properties are defined in the dictionary
    ``AMQP_CONNECTION_PROPERTIES`` defined in the Python module.
    ``settings``.
    """
    HttpMethod = Enum(
        'DELETE',
        'GET',
        'HEAD',
        'POST',
        'PUT'
    )

    class BaseServiceException(Exception):
        """
        Base class of exception that a service might raise to indicate some
        unexpected conditions.
        """
        def __init__(self, message=None, payload=None):
            super(BaseService.BaseServiceException, self).__init__(message)
            self.__payload = payload

        @property
        def message(self):
            return str(self)

        @property
        def payload(self):
            return self.__payload

    class DeletedObjectException(BaseServiceException):
        """
        Signal that the specified object has been deleted and as such it
        cannot be used or referenced anymore.
        """
        pass

    class DisabledObjectException(BaseServiceException):
        """
        Signal that the specified object has been disabled and as such it
        cannot be used.
        """
        pass

    class ExpiredSessionException(BaseServiceException):
        """
        Signal that the account session of the user has expired.  The user
        needs to login again.
        """
        pass

    class InvalidOperationException(BaseServiceException):
        """
        Signal the operation requested is invalid, for instance one or several
        arguments provided within the request are not coherent together or the
        state of the object on which the operation is requested.
        """
        pass

    class IllegalAccessException(BaseServiceException):
        """
        Signal that the user on behalf whom a function is called is not
        authorized to perform the action requested.
        """
        pass

    class InvalidArgumentException(BaseServiceException):
        """
        Signal that an argument passed to a function is invalid, more likely
        of the wrong type.
        """
        pass

    class UndefinedObjectException(BaseServiceException):
        """
        Signal that the specified object doesn't exist and as such it cannot
        be referenced.
        """
        pass

    class MultipartFormData(object):
        """
        Represent data to be uploaded to the platform as in a multipart MIME
        data stream "multipart/form-data".
        """
        def __init__(self, field_name, file_name,
                file_path_name=None,
                data=None):
            """
            Build a new instance of this class.

            @param field_name: original field name in the form to send to the
                platform to upload a file.

            @param file_name: name of the file as defined in the HTTP request that
                the client application sent to the platform.

            @param file_path_name: complete file path name of the file to upload.

            # @param content_type: specify the nature of the data in the content of
            #     the file that has been uploaded to the platform entity, by giving
            #     type and subtype identifiers, and by providing auxiliary
            #     information that may be required for certain types.

            @param data: content of the file that has been uploaded.
            """
            if data is None and file_path_name is None:
                raise self.InvalidArgumentException("Either data MUST be not null, either a file path name MUST be specified")

            self.field_name = field_name
            self.file_name = file_name
            self.file_path_name = file_path_name
            self.data = data

        @staticmethod
        def from_file(file_path_name, field_name=None):
            file_name = os.path.basename(file_path_name)
            return BaseService.MultipartFormData(
                    field_name or os.path.splitext(file_name)[0],
                    file_name,
                    file_path_name=file_path_name)

        def read_data(self):
            if self.data is not None:
                return self.data


    BASE_SERVICE_EXCEPTIONS = {
        'DeletedObjectException': DeletedObjectException,
        'DisabledObjectException': DisabledObjectException,
        'ExpiredSessionException': ExpiredSessionException,
        'InvalidOperationException': InvalidOperationException,
        'IllegalAccessException': IllegalAccessException,
        'InvalidArgumentException': InvalidArgumentException,
        'UndefinedObjectException': UndefinedObjectException
    }

#    DEFAULT_LIMIT = 20
#    MAXIMUM_LIMIT = 100

    # Default number of items that a remote method would return.
    DEFAULT_RESULT_SET_SIZE = 20

    # Maximum number of items that a remote method would return.
    MAXIMUM_RESULT_SET_SIZE = 100

    def __init__(self, session_or_connection):
        """
        Build an instance ``BaseService``.

        @param session_or_connection: an instance of a class that inherits
            from ``PerseusSession``, such as ``PerseusAnonymousSession`` or
            ``PerseusAuthenticatedSession``.  This constructor also accepts an
            instance of a class that inherits from ``PerseusConnection``; in
            that case, this constructor builds an anonymous session.
        """
        if session_or_connection is None:
            raise ValueError('A session or a connection properties object MUST be passed')

        self._service_name = self.__class__.__name__

        if isinstance(session_or_connection, PerseusSession):
            self.session = session_or_connection
        elif isinstance(session_or_connection, PerseusConnection):
            self.session = session_or_connection.build_session()
        else:
            raise ValueError("The class of the instance session MUST inherits from 'PerseusSession' or 'PerseusConnection'")

    @staticmethod
    def _declare_custom_exceptions(exceptions):
        BaseService.BASE_SERVICE_EXCEPTIONS.update(exceptions)

    def __default_error_handler__(self, error, payload):
        """
        Default handler of error the server platform raises when a HTTP
        request fails.

        @param error: an instance ``urllib2.HTTPError``.
        """
        try:
            exception_name = payload['error']
            exception_class = BaseService.BASE_SERVICE_EXCEPTIONS[exception_name]

            raise exception_class(
                    message=payload.get('message'),
                    payload=payload.get('payload'))

        except KeyError:
            raise Exception('Undeclared platform service exception "%s"' % payload['error'])

    @staticmethod
    def decode_object(obj, cast_operators):
        def __decode_value__(value, cast_operator=None):
            return value if value is None or cast_operator is None else \
                cast.string_to_enum(value, cast_operator) if isinstance(cast_operator, enum.Enum) \
                else cast_operator(value)

        return Object(**dict([ (name, __decode_value__(value, cast_operators.get(name)))
                 for (name, value) in obj.__dict__.iteritems() ]))

    def flush_session(self):
        self.session = self.session.connection.build_session()

    def get_session(self):
        return self.session

    def get_service_name(self):
        return self._service_name

    def send_request(self,
            http_method=HttpMethod.GET,
            headers=None,
            path=None,
            url_bits=None,
            arguments=None,
            message_body=None,
            files=None,
            authentication_required=False,
            signature_required=True,
            compatibility_required=False,
            radioactive_tracer=False):
        return self.session.__request__(
                http_method=http_method,
                headers=headers,
                path=path,
                url_bits=url_bits,
                arguments=arguments,
                files=files,
                message_body=message_body,
                authentication_required=authentication_required,
                signature_required=signature_required,
                compatibility_required=compatibility_required,
                radioactive_tracer=radioactive_tracer,
                error_handler=self.__default_error_handler__)

    def set_session(self, session):
        """
        Redefine the session used by the instance of this inherited service,
        for instance, when the user signs-in or when he signs-out.

        @param session: an instance of a class that inherits from
            ``PerseusSession``, such as ``PerseusAnonymousSession`` or
            ``PerseusAuthenticatedSession``.
        """
        if session and not isinstance(session, PerseusSession):
            raise Exception('The class of the instance session MUST inherits from ``PerseusSession``')

        self.session = session
