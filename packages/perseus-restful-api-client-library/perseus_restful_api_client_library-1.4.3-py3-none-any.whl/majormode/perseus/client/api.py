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

import datetime
import hashlib
import hmac
import json
import logging
import re
import requests
import socket
import urllib.parse
import urllib.request
import uuid
import traceback

from majormode.perseus.constant.http import HttpMethod
from majormode.perseus.constant.http import HttpScheme
from majormode.perseus.model import obj
from majormode.perseus.model.obj import Object
from majormode.perseus.utils import cast


class PerseusConnection:
    """
    Connection properties to access a RESTful API server built on the
    Perseus server framework.
    """
    DEFAULT_HTTP_PORT_NUMBER = 80
    DEFAULT_HTTPS_PORT_NUMBER = 443
    DEFAULT_PORT_NUMBER = DEFAULT_HTTPS_PORT_NUMBER

    def __build_anonymous_session(self):
        """
        Build an anonymous user session to the RESTful API server identified
        by this connection.


        :return: An object `PerseusAnonymousSession` connected to the RESTful
            API server identified by this connection.
        """
        return PerseusAnonymousSession(self)

    def __build_authenticated_session(self, payload, strict=True):
        """
        Build an authenticated user session to the RESTful API server
        identified by this connection.

        The function retrieves the session properties from the specified
        payload.


        :param payload: the payload of the user session provided as:

            * A dictionary

            * A string representation of a JSON object

            * An object `Object`


        :return: An objet `PerseusAuthenticatedSession`.
        """
        try:
            return PerseusAuthenticatedSession(self, payload) if isinstance(payload, Object) else \
                PerseusAuthenticatedSession.from_payload(
                    self,
                    cast.string_to_json(payload) if isinstance(payload, str) else payload)
        except KeyError as exception:
            if strict:
                raise exception
            else:
                logging.debug(traceback.format_exc())
                return self.__build_anonymous_session()

    def __init__(
            self,
            hostname,
            consumer_key,
            consumer_secret,
            api_version=None,
            port_number=None,
            debug=False,
            timeout=None,
            radioactive_tracer=False):
        """
        Build an object `PerseusConnection` defining the properties to connect
        to a RESTful API server built on the Perseus server framework.


        :param hostname: Fully qualified domain name of the RESTful API
            server.

        :param consumer_key: A value used by the consumer to identify itself
            to the service provider.

        :param consumer_secret: Secret used by the consumer to establish
            ownership of the consumer key.

        :param api_version: An object `Version` that indicates the version
            of the platform RESTful API that is integrated.

        :param port_number: Port number, added to the RESTful API server's IP
            address, to complete the destination address for the communication
            session.  That is, data packets are routed across the network to
            the specific destination IP address, and then, upon reaching the
            destination computer, are further routed to the specific process
            bound to the destination port_number number.

        :param debug: Enable or disable debug mode.  If this is `True`, the
            cURL representation of a request sent to the RESTful API server is
            written to the standard input.

        :param timeout: Enforce the request to be processed within this
            predetermined elapsed time, expressed in seconds, rather than
            waiting indefinitely.  The request will be aborted after the
            timeout period has elapsed.  This is based on the assumption that
            further waiting is useless, and some other action is necessary.

        :param radioactive_tracer: Indicate whether the HTTP request needs
            to integrate a "radioactive tracer", i.e., a nonce ("number used
            once"), a pseudo-random number, used to explore the mechanism of
            subsequent procedure calls by tracing the path that the HTTP
            request follows.  The HTTP request is added an additional header
            `X-Radioactive-Tracer`.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.api_version = api_version
        self.hostname = hostname
        self.port_number = port_number or self.DEFAULT_PORT_NUMBER
        self.scheme = HttpScheme.https if self.port_number == self.DEFAULT_HTTPS_PORT_NUMBER else HttpScheme.http
        self.debug = debug
        self.timeout = timeout
        self.radioactive_tracer = radioactive_tracer

    def build_session(self, payload=None):
        """
        Build a user session to the RESTful API server identified by this
        connection.

        The user can be anonymous or authenticated.


        :param payload: A dictionary, or a string representation of a JSON
            expression, of the attributes of an existing session to this
            RESTful API server.


        :return: An object `PerseusAuthenticatedSession` if the payload of an
            existing authenticated user session was passed to this function,
            otherwise an object `PerseusAnonymousSession`.
        """
        return self.__build_anonymous_session() if not payload \
            else self.__build_authenticated_session(payload)

    @classmethod
    def from_json(cls, hostname, payload, port_number=None):
        """
        Build an object `PerseusConnection` from a JSON serialization of this
        object.


        :param hostname: Fully qualified domain name of the RESTful API
            server.

        :param payload: A JSON expression containing at least the following
            properties:

            * `consumer_key`: A value used by the consumer to identify itself to the
              service provider.

            * `consumer_secret`: Secret used by the consumer to establish ownership
              of the consumer key.

        :param port_number: Port number, added to the RESTful API server's IP
            address, to complete the destination address for the communication
            session.


        :return: An object `PerseusConnection`.
        """
        return PerseusConnection(
            hostname,
            payload['consumer_key'],
            payload['consumer_secret'],
            port_number=payload.get('port_number') or port_number or cls.DEFAULT_PORT_NUMBER)


class PerseusSession:
    """
    Session of user connected to a RESTful API server built on the Perseus
    server framework.
    """
    CRYPTOGRAPHIC_HASH_FUNCTION = hashlib.sha1

    class Request(urllib.request.Request):
        """
        Support of the explicit specification of a HTTP method.
        """
        def __init__(self, *args, **kwargs):
            http_method = kwargs.pop('http_method', None)
            self.__method = http_method and str(http_method)
            urllib.request.Request.__init__(self, *args, **kwargs)

        def get_method(self):
            return self.__method or super().get_method()

    class SocketTimeoutException(Exception):
        """
        Signal that a timeout occurs on a socket during blocking operations
        like the connection attempt of a HTTP request.
        """

    def __build_curl_command(self, http_method, path_query, message_body, headers):
        """
        Build the string representation of the cURL command-line that sends
        this request.


        :param http_method: An item of the enumeration `HttpMethod`.

        :param path_query: A string representation of the path and the query
            parameters of the URL endpoint.

        :param message_body: A string representation of the message body to
            pass along the HTTP request when the HTTP method `POST` or `PUT`
            is used.

        :param headers: A dictionary of headers to pass along the HTTP request.


        :return: A string representation of the cURL command-line that sends
            this request.
        """
        url_string = f'{self.connection.scheme}://{self.connection.hostname}:{self.connection.port_number}{path_query}'

        headers_string = ' '.join([
            f'-H "{key}: {value}"'
            for key, value in headers.items()
            if value is not None
        ])

        curl_string = f'curl -X {http_method} "{url_string}" {headers_string}'

        if http_method in (HttpMethod.POST, HttpMethod.PUT):
            curl_string += f" -d '{message_body or ''}'"

        return curl_string

    @classmethod
    def __build_path_query_string(cls, path, arguments):
        """
        Build the URL path with its query string.


        The query string is built with the specified list of arguments.  For
        each argument that would correspond to a list of items, the value
        of this argument is built with the concatenation of the string
        representation of each item separated with a comma.

        For instance, the query string built from the following arguments:

            {
              "foo": uuid.UUID('2981c498-694a-11e3-ba63-00224d868489'),
              "bar": [1, 2, 3, 5, 7, 11]
            }

        is:

            foo=2981c498-694a-11e3-ba63-00224d868489&bar=1,2,3,4,5,7,11


        :param path: The path to the URL endpoint.

        :param arguments: A dictionary corresponding to the query parameters
            to pass to the URL endpoint.


        :return:
        """
        if arguments is None:
            return path

        stringified_arguments = {
            key: cls.__stringify_query_parameter_value(value)
            for key, value in arguments.items()
            if value is not None
        }

        encoded_query_string = urllib.parse.urlencode(stringified_arguments)

        path_query_string = f'{path}?{encoded_query_string}'
        return path_query_string

    def __calculate_signature(self, path_query, message_body=None):
        """
        Return the signature of a HTTP request.


        :param path_query: A string representation of the path and the query
            parameters of the URL endpoint referenced by the HTTP request.

        :param message_body: The body message passed to HTTP request using the
            method `POST` or `PUT`.


        :return: The signature of the HTTP request.
        """
        message = path_query if message_body is None else f'{path_query}{message_body}'

        signature = hmac.new(
            self.connection.consumer_secret.encode(),
            msg=message.encode(),
            digestmod=self.CRYPTOGRAPHIC_HASH_FUNCTION) \
            .hexdigest()

        return signature

    @staticmethod
    def __expand_url_bits(path, url_bits):
        """
        Find and replace names of URL bits by their corresponding value.


        :param path: Path of the Uniform Resource Identifier (URI) that names
            a resource of the platform the HTTP request requires to gain
            access to.

        :param url_bits: In-line arguments, also known as bits of URL.


        :return: A string representing the path of the URL, which URL bits
            have been expanded with their respective values.
        """
        for url_bit in re.findall(r'\([a-z0-9_]*\)', path):
            path = path.replace(url_bit, str(url_bits[url_bit[1:-1]]))

        return path

    def __get_headers(
            self,
            path_query,
            authentication_required=False,
            compatibility_required=False,
            files=None,
            headers=None,
            message_body=None,
            radioactive_tracer=False,
            signature_required=True):
        """
        Add additional HTTP headers to pass along the HTTP request.


        :param path_query: A string representation of the path and query
            parameters of the URL endpoint referenced by the HTTP request.

        :param authentication_required: Indicate whether the specified
            endpoint of the RESTful API server requires the user to be logged
            in.  This user session MUST correspond to a
            `PerseusAuthenticatedSession` or the function will raise an
            exception `ValueError`.  The functions adds a header
            'X-Authentication' corresponding to the identification of this
            user session.

        :param compatibility_required: Indicate whether the client application
            requires to use a specific version of the RESTful API server for
            this particular HTTP request.  The function adds a header
            'X-API-Version' with the value of the API version specified in the
             object `PerseusConnection` associated with this user session
             object.

        :param files: A list of files to be uploaded to the RESTful API server.

        :param headers: A dictionary of HTTP header to pass along the HTTP
            request.

        :param message_body: The body message passed to HTTP request using the
            method `POST` or `PUT`.

        :param radioactive_tracer: Indicate whether to generate an identifier

        :param radioactive_tracer: Indicate whether the HTTP request needs
            to integrate a "radioactive tracer", i.e., a nonce ("number used
            once"), a pseudo-random number, used to explore the mechanism of
            subsequent procedure calls by tracing the path that the HTTP
            request follows.  The function adds a header 'X-Radioactive-Tracer'.

        :param signature_required: Indicate whether to sign the HTTP request
            with the Consumer Secret defined in the object `PerseusConnection`
            associated with this user session object.  The functions adds a
            header 'X-API-Sig'.


        :return: A dictionary of headers.
        """
        if headers is None:
            headers = {}

        # headers['Content-Type'] = 'multipart/form-data' if files else 'application/json'
        if not files:
            headers['Content-Type'] = 'application/json'

        if radioactive_tracer or self.connection.radioactive_tracer:
            headers['X-Radioactive-Tracer'] = uuid.uuid1().hex

        if self.session_id:
            headers['X-Authentication'] = self.session_id.hex
        elif authentication_required:
            raise ValueError("A user session MUST be specified when authentication is required")

        headers['X-API-Key'] = self.connection.consumer_key
        if signature_required:
            headers['X-API-Sig'] = self.__calculate_signature(path_query, message_body=message_body)

        if compatibility_required:
            headers['X-API-Version'] = str(self.connection.api_version)

        return headers

    def __init__(self, connection, attributes=None):
        """
        Build an object `PerseusSession`.


        :param connection: An object `PerseusConnection` that references a
            Perseus compliant RESTful API server to connect to.

        :param attributes: An object that contains at least the following
            attributes:

            * `account_id` (required): Identification of the user as
              registered to the server platform.

            * `session_id` (required): Identification of the session of the
              user authenticated against the RESTful API server.

            * `expiration_time (required)`: Time when the login session of
              the authenticated user will expire.
        """
        if not isinstance(connection, PerseusConnection):
            raise ValueError('argument "connection" MUST be an object "PerseusConnection"')

        self.connection = connection
        self.session_id = attributes and attributes.session_id
        self.account_id = attributes and attributes.account_id
        self.expiration_time = attributes and attributes.expiration_time

    def __request__(
            self,
            http_method,
            path,
            url_bits=None,
            arguments=None,
            headers=None,
            message_body=None,
            files=None,
            authentication_required=False,
            signature_required=True,
            compatibility_required=False,
            radioactive_tracer=False,
            error_handler=None):
        """
        Send the specified HTTP request and return the response of the
        RESTful API server.


        :param http_method: An item of the enumeration `HttpMethod` that
            indicates the HTTP method of the request to send.

        :param path: The path of the Uniform Resource Identifier (URI) that
            names a resource of the platform the HTTP request requires to
            gain access to.

        :param url_bits: In-line arguments, also known as bits of URL.

        :param arguments: A dictionary of key/value pairs representing the
            arguments to be passed in the query string of the HTTP request.

        :param headers: A dictionary of key/value pairs representing the
            headers of the HTTP request.

        :param message_body: An object corresponding to the message body to be
            passed in the HTTP request using a HTTP method `POST` or `PUT`.

        :param files: A list of file-like objects to be uploaded.  The
            function will create a data stream "multipart/form-data" and add
            each file within a multipart MIME field named with a auto-
            generated UUID.

        :param authentication_required: Indicate whether the HTTP request must
            be sent on behalf of an authenticated user.  The HTTP request is
            added an additional header 'X-Authentication' with the access
            token (session ID) that impersonates this user.

        :param signature_required: Indicate whether the HTTP request must be
            signed.  The HTTP request is added two additional headers
            'X-API-Key' and 'X-API-Sig'.  The latter is calculated based on
            the content of the HTTP request and the API secret key.

        :param compatibility_required: Indicate whether the HTTP request must
            be strictly compatible with the version of the server platform's
            API.  The HTTP request is added the HTTP header field
            `X-API-Version` which value complies with a version number using
            a standard tuple of integers: `major.minor.patch`.

        :param radioactive_tracer: Indicate whether the HTTP request needs
            to integrate a "radioactive tracer", i.e., a nonce ("number used
            once"), a pseudo-random number, used to explore the mechanism of
            subsequent procedure calls by tracing the path that the HTTP
            request follows.  The HTTP request is added an additional header
            'X-Radioactive-Tracer'.

        :param error_handler: A Python function that will be passed any
            instance `urllib2.HTTPError` that represents an exceptional
            situation, i.e., a condition, basically an error, that the
            platform would face when performing the HTTP request.  This
            function is responsible for raising the appropriate Python
            exception.


        :return: A JSON object representing the response to this HTTP request.


        :raise SocketTimeoutException: If a timeout occurs on the socket
            during blocking operations like the connection attempt of the HTTP
            request.
        """
        # Define the complete URL of the endpoint referenced by the HTTP request.
        path = self.__expand_url_bits(path, url_bits)
        path_query = self.__build_path_query_string(path, arguments)
        url = f'{self.connection.scheme}://{self.connection.hostname}:{self.connection.port_number}{path_query}'
        stringified_message_body = None if http_method not in (HttpMethod.POST, HttpMethod.PUT) \
            else json.dumps(obj.stringify(message_body) if message_body else {})

        # Define the HTTP headers to pass along the HTTP request.
        headers = self.__get_headers(
            path_query,
            headers=headers,
            message_body=stringified_message_body,
            authentication_required=authentication_required,
            compatibility_required=compatibility_required,
            files=files,
            radioactive_tracer=radioactive_tracer,
            signature_required=signature_required)

        if self.connection.debug:
            logging.debug(self.__build_curl_command(http_method, path_query, message_body, headers))

        # Send the HTTP request.
        execution_begin_time = datetime.datetime.now()

        try:
            if files:
                files = dict([(uuid.uuid1().hex, f) for f in files])
                response = requests.put(url, files=files, headers=headers)
                data = response.text
            else:
                request = PerseusSession.Request(
                    url,
                    data=stringified_message_body and stringified_message_body.encode(),
                    headers=headers,
                    http_method=http_method)
                response = urllib.request.urlopen(request, timeout=self.connection.timeout)
                data = response.read()

            logging.debug(data)

        except urllib.request.HTTPError as error:
            if error_handler:
                data = error.read()
                logging.error(data)
                logging.exception(error)
                error_handler(error, None if (data is None or len(data) == 0) else json.loads(data))
            else:
                raise error

        except urllib.request.URLError as error:
            logging.exception(error)
            raise self.SocketTimeoutException() if isinstance(error.reason, socket.timeout) else error

        except socket.timeout as error:
            logging.exception(error)
            raise PerseusSession.SocketTimeoutException()

        # Log the latency time, i.e. the time delta between the instant the
        # client application sends the request to the RESTful API server and
        # the instant this client application receives the response.
        #
        # This duration includes the time the request and its response takes
        # to travel back and forth over the network between the client
        # application and the RESTful API server. The Latency corresponds to
        # Response Time plus the Network Time, also known as Time to First Byte
        # (TTFB) for the time it takes in milliseconds for a client application
        # to receive the first byte of the response from a server.
        execution_end_time = datetime.datetime.now()
        execution_duration = execution_end_time - execution_begin_time
        execution_duration_milliseconds = execution_duration.seconds * 1000 \
            + execution_duration.microseconds / 1000

        logging.debug(f"Query {http_method} {url} executed in {execution_duration_milliseconds}ms")

        # Return the JSON expression of the data that the RESTful API server
        # returned.
        return None if data is None or len(data) == 0 \
            else json.loads(data)

    @staticmethod
    def __stringify_query_parameter_value(value):
        """
        Stringify the value of a query parameter.


        If the argument `value` passed to this function is a list, a tuple, or
        a set, the function convert each item to a string, and concatenate all
        the strings separated with a comma. Otherwise, the function simply
        returns the string representation of the argument `value`:

        ```python
        >>> __stringify_query_parameter_value([1, 2, 3, 5, 7, 11])
        '1,2,3,4,5,7,11'
        >>> __stringify_query_parameter_value(uuid.UUID('2981c498-694a-11e3-ba63-00224d868489'))
        '2981c498-694a-11e3-ba63-00224d868489'
        ```

        :param value: An object.


        :return: The stringified value of this object.
        """
        # path_query_string = path if arguments is None \
        #     else '%s?%s' % \
        #          (path,
        #           urllib.parse.urlencode(dict([
        #              (key, ','.join([str(item).encode('utf-8') for item in value])
        #                  if type(value) in [list, set, tuple] else str(value).encode('utf-8'))
        #              for (key, value) in arguments.items()
        #              if value is not None])))

        return str(value) if type(value) not in (list, set, tuple) \
            else ','.join([str(element) for element in value])


class PerseusAnonymousSession(PerseusSession):
    """
    Anonymous user session connected to a RESTful API server.
    """
    def __init__(self, connection):
        """
        Build an object `PerseusAnonymousSession`.


        :param connection: An object `PerseusConnection` referencing a RESTful
            API server the user is connected to.
        """
        super().__init__(connection)


class PerseusAuthenticatedSession(PerseusSession):
    """
    Login session of a user connected to a RESTful API server.
    """
    def __init__(self, connection, attributes):
        """
        Build an object `PerseusAuthenticatedSession`.


        :param connection: An object `PerseusAuthenticatedSession` referencing
            a RESTful API server the user is connected to.

        :param attributes: An object that contains at least the following
            attributes:

            * `account_id` (required): Identification of the user as
              registered to the server platform.

            * `session_id` (required): Identification of the session of the
              user authenticated against the RESTful API server.

            * `expiration_time (required)`: Time when the login session of
              the authenticated user will expire.
        """
        if not isinstance(attributes, Object):
            raise ValueError('the argument "attributes" MUST inherit from `Object')
        super().__init__(connection, attributes=attributes)

    @staticmethod
    def from_payload(connection, payload):
        """
        Build an object `PerseusAuthenticatedSession` from the JSON
        serialization of a user login session.


        :param connection: An object `PerseusConnection` referencing the
            RESTful API server the user session belongs to.

        :param payload: A JSON expression containing the attribute of the user
            session.  This JSON expression MUST contain at least the following
            properties:

            * `account_id` (required): Identification of the user as
              registered to the server platform.

            * `session_id` (required): Identification of the session of the
              user authenticated against the RESTful API server.

            * `expiration_time (required)`: Time when the login session of
              the authenticated user will expire.


        :return: An object `PerseusAuthenticatedSession`.
        """
        if not payload:
            return None

        # Build the session's attributes from the JSON payload.
        attributes = cast.json_to_object(payload)

        # Convert the common attributes to their respective type.  The client
        # application will probably have to convert custom attributes.
        attributes.account_id = cast.string_to_uuid(payload['account_id'])
        attributes.expiration_time = cast.string_to_timestamp(payload['expiration_time'])
        attributes.locale = cast.string_to_locale(payload.get('locale'))
        attributes.picture_id = cast.string_to_uuid(payload.get('picture_id'))
        attributes.session_id = cast.string_to_uuid(payload['session_id'])

        # Return the authenticated session of the user.
        return PerseusAuthenticatedSession(connection, attributes)
