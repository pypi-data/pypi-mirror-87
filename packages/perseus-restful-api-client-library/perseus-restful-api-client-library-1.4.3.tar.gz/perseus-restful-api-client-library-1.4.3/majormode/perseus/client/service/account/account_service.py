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

from majormode.perseus.client.api import PerseusConnection
from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.constant.account import AccountType
from majormode.perseus.model import obj
from majormode.perseus.model.contact import Contact
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object

import getpass
import json
import os


class AccountService(BaseService):
    class AuthenticationFailureException(BaseService.BaseServiceException):
        """
        Signal that the email address or password that has been provided for
        authenticating a user account is incorrect.
        """
        pass

    class ContactAlreadyUsedException(BaseService.BaseServiceException):
        """
        Signal that one or more contact information such as, for instance, an
        email address, provided to sign-up a user account, is already used by
        another user account of the platform.
        """
        pass

    class UnsupportedOAuthServiceProvider(BaseService.BaseServiceException):
        """
        Signal that the specified OAuth Service Provider is not yet supported
        by the platform.
        """
        pass

    BaseService._declare_custom_exceptions({
        'AuthenticationFailureException': AuthenticationFailureException,
        'ContactAlreadyUsedException': ContactAlreadyUsedException,
        'UnsupportedOAuthServiceProvider': UnsupportedOAuthServiceProvider
    })

    def __init__(self, session):
        super().__init__(session)

    def is_contact_available(self, contact):
        """
        Indicate whether the specified contact information is available.

        In the case this contact information would have been already
        registered by a user, indicate whether this contact information has
        been also verified.


        :param contact: An instance `Contact`


        :return: A tuple containing the following values:

            * `is_available`: `True` if the specified contact is not registered by
              any existing account; `False` otherwise.

            * `is_verified`: `True` if the specified contact has been registered
              and verified; `False` otherwise.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account/contact/(name)/availability',
                url_bits={
                    'name': str(contact.name)
                },
                arguments={
                    'value': contact.value
                },
                authentication_required=False,
                signature_required=True))

        return payload.is_available, payload.is_verified

    def set_fullname(self, fullname):
        """
        Update the complete full name of a user.


        :param fullname: Full name by which the user is known, as given by the
            user himself, i.e., untrusted information.


        :return: An instance containing the following attributes:

            * ``account_id`` (required): Identification of the user's account.

            * ``fullname`` (required): The new full name of the user.

            * ``update_time`` (required): Time of the most recent modification of
              the attributes of the user's account.


        @raise DeletedObjectException: If the user's account has been deleted.

        @raise DisabledObjectException: If the user's account has been
            disabled.

        @raise Undefined ObjectException: If the specified identification
            doesn't refer to a user account registered to the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.PUT,
                path='/account/fullname',
                message_body={
                    'fullname': fullname
                },
                authentication_required=True,
                signature_required=True))

    def upload_avatar(self, file):
        """
        Upload a new picture of this user account, also known as the avatar,
        which is the graphical representation of the user.


        :param file: A file-like object to upload to the platform.


        :return: An instance containing the following attributes:

            * ``file_name`` (required): The original local file name as the
            ``filename`` parameter of the ``Content-Disposition`` header.

            * ``picture_id`` (required): Identification of the new avatar of the
                user's account as registered to the platform.

            * ``picture_url`` (required): Uniform Resource Locator (URL) that
              specifies the location of the user's avatar.  The client application
              can use this URL and append the query parameter ``size`` to specify
              a given pixel resolution of the photo, such as ``thumbnail``,
              ``small``, ``medium``, or ``large``.

            * ``update_time`` (required): Time of the most recent modification of
              the attributes of the user's account.  This information should be
              stored by the client application to manage its cache of user
              accounts.


        @raise DeletedObjectException: If the user's account has been deleted.

        @raise DisabledObjectException: If the user's account has been
            disabled.

        @raise InvalidOperation: If the format of the uploaded image is not
            supported.

        @raise Undefined ObjectException: If the specified identification
            doesn't refer to a user account registered to the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.PUT,
                path='/account/avatar',
                files=[file],
                authentication_required=True,
                signature_required=True))
































    def add_contacts(self, contacts):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/contacts',
                message_body=contacts,
                authentication_required=False,
                signature_required=True))

    def __sign_in(self, email_address, password):
        """
        Sign-in the user against the platform providing his email address and
        his password.


        :param email_address: email address of the user.

        :param password: password of the user.


        :return: a session instance containing the following members:

            * ``account_id`` (required): identification of the account of the
              user.

            * ``contacts`` (required): a list of contact information that can be
              used as primary contact information for this user account.  A
              contact information corresponds to the following tuples::

                   ``(name, value, is_verified)``

                where:

                * ``name``: an item of the enumeration ``ContactName``.

                * ``value``: value of the property representing by a string.

                * ``is_verified``: indicate whether this contact information has been
                  verified.

            * ``expiration_time``: time when the login session will expire.

            * ``fullname``: complete full name of the user as given by the user
              himself, i.e., untrusted information, or as determined from his
              email address as for a ghost account.

            * ``session_id``: identification of the login session of the user.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/session',
                message_body={
                    'email_address': email_address,
                    'password': password
                },
                authentication_required=False,
                signature_required=True))

        self.set_session(self.session.connection.build_authenticated_session(payload))

        return self.session

    def get_account(self, account_id, include_pending=False):
        accounts = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account',
                arguments={
                    'ids': account_id,
                    'include_pending': include_pending
                },
                authentication_required=False,
                signature_required=True))

        if len(accounts) == 0:
            raise self.UndefinedObjectException()

        return accounts[0]

    def get_contact_verification_request(self, request_id):
        """

        :param request_id:


        :return:
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account/contact/verification/(request_id)',
                url_bits={
                    'request_id': request_id
                },
                authentication_required=False,
                signature_required=True))

    def get_password_reset_request(
            self, request_id,
            check_access=False,
            check_app=False,
            check_status=False):
        """
        Return extended information about the specified password reset that a
        user has requested for his account.


        :param request_id: identification of the password request.

        :param check_access: indicate whether the function must check if the
            user on behalf of whom the function is called is either the user
            who added this photo.

        :param check_app: indicate whether the function must check if the
            client application on behalf of which the function is called is
            the same than the client application that requested the password
            reset of the user's account.

        :param check_status: indicate whether the function must check the
            current status of this passwor reset request and raise an
            exception if this status is not of enabled.


        :return: an instance containing the following members:

            * ``account_id`` (required): identification of the user's account
              which the user has requested to reset his password.

            * ``app_id`` (required): identification of the client application that
              submitted on behalf of the user the request to reset the password
              of his account.

            * ``attempt_count`` (required): number of times the platform sent an
              email to the user with an embedded link to let this user reset his
              password.

            * ``creation_time`` (required): time when the user requested to reset
              the password of his account.

            * ``request_count`` (required): number of times the user requested to
              reset his password before he finally changed it.

            * ``request_id`` (required): identification of this password reset
              request.

            * ``update_time`` (required): the most recent time when the platform
              sent an email to the user with an embedded link to let this user
              reset his password.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account/password/reset/request/(request_id)',
                url_bits={
                    'request_id': request_id
                },
                arguments={
                    'check_access': check_access,
                    'check_app': check_app,
                    'check_status': check_status
                },
                authentication_required=False,
                signature_required=True))

        return payload

    def get_sns_data_deletion(self, request_id):
        """
        Return information about a request sent to the platform to delete the
        data of a user that an application has collected from the given Social
        Networking Service about this user.


        :param request_id: identification of the data deletion request as
            registered to the platform.


        :return: an instance containing the following attributes:

            * ``creation_time`` (required): time when the request to delete the data
              of a user has been initiated.

            * ``object_status`` (required): current status of this data deletion
              request.

            * ``request_id`` (required): the identification of the data deletion
              request as registered to the platform.

            * ``sns_app_id`` (required): identification of the application as
              registered to the 3rd party Social Networking Service.

            * ``sns_name`` (required): code name of the 3rd party Social Networking
              Service.

            * ``sns_user_id`` (required): identification of the user as registered
              to the 3rd party Social Networking Service.

            * ``update_time`` (required): time of the most recent update of the
              access token of this user.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account/sns/deletion/request/(request_id)',
                url_bits={
                    'request_id': request_id
                },
                authentication_required=False,
                signature_required=True))



    def is_contact_verification_request(self, name, request_id):
        """
        Check whether the given identification corresponds to a verification
        request of the specified type of contact.


        :param name: an instance `Contact.ContactName` of the contact that is
            requested to be verified.

        :param request_id: identification of the contact verification request.


        :return: `True` if the specified identification corresponds to a
            contact verification request registered to the platform;
            ``False`` otherwise.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/account/(name)/verification/(request_id)',
                url_bits={
                    'name': name,
                    'request_id': request_id
                },
                authentication_required=False,
                signature_required=True))

        return payload.data

    def request_contact_verification(self, contact, locale=DEFAULT_LOCALE):
        """
        Request the platform to initiate the process to verify the specified
        contact information.

        The function generates a *nonce* ("number used once"), which is a
        pseudo-random number issued to identify the verification of the
        contact information.  To confirm the contact information of the user,
        the function ``confirm_contact`` will have to be called with this
        *nonce*.


        :param contact: an instance `Contact`.

        :param locale: a ``Locale`` instance referencing the preferred
            language of the user.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/(name)/verification',
                url_bits={
                    'name': contact.name
                },
                message_body={
                    'locale': locale,
                    'value': contact.value
                },
                authentication_required=False,
                signature_required=True))

    def request_password_reset(self, email_address):
        """
        Request the platform to initiate the process to help the user in
        resetting his password that he has forgotten.

        The function generates a *nonce* ("number used once"), which is a
        pseudo-random number issued to identify the request of the user.  This
        nonce will be sent to the user to his email address, more likely in a
        HTML link that will redirect the end user to a web page responsible
        for allowing the user to reset his password (cf. function
        ``change_forgotten_password`` that must be passed this *nonce*).

        Note: if the user sends consecutively two requests to reset his
        password within the minimal allowed duration of time, the function
        ignores the new request and returns the identification of the previous
        request.


        :param email_address: email address of the account of the user who is
            requesting to reset is forgotten password.


        @raise DeletedObjectException: if the user account has been deleted.

        @raise DisabledObjectException: if the user account has been disabled.

        @raise InvalidOperationException: if a password reset has already been
            requested recently for this email address.

        @raise UndefinedObjectException: if the specified email address
            doesn't refer to any user account registered against the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/password/reset/request',
                message_body={
                    'email_address': email_address
                },
                authentication_required=False,
                signature_required=True))

    def request_sns_data_deletion(self, sns_name, sns_app_id, sns_user_id):
        """
        Request the platform to delete the data of the specified user that an
        application has collected from the given Social Networking Service
        about this user.


        :param sns_name: code name of the 3rd party Social Networking Service.

        :param sns_app_id: identification of the application as registered to
            the 3rd party Social Networking Service.

        :param sns_user_id: identification of the user as registered to the
            3rd party Social Networking Service.


        :return: an instance containing the following attributes:

            * ``creation_time`` (required): time when this request has been
              registered to the platform.

            * ``request_id`` (required): identification of the data deletion
              request as registered to the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/sns/deletion/request',
                message_body={
                    'sns_app_id': sns_app_id,
                    'sns_name': sns_name,
                    'sns_user_id': sns_user_id
                },
                authentication_required=False,
                signature_required=True))

    def reset_password(self, request_id, new_password):
        """
        Change the password of the account of a user who forgot his password
        and who requested the platform to reset, as this user cannot login
        into the platform anymore.


        :param request_id: identification of the request of the user to reset
            his forgotten that the function ``request_password_reset``
            generated.

        :param new_password: new password of this user's account.


        @raise InvalidArgumentException: if the new password doesn't conform
            to the rules of password definition.

        @raise UndefinedObjectException: if the specified identification
            doesn't refer to a request from a user to reset his forgotten
            password.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account/password/reset',
                message_body={
                    'new_password': new_password,
                    'request_id': request_id
                },
                authentication_required=False,
            signature_required=True))

    def sign_out(self):
        """
        Sign out the user from his login session.


        @raise IllegalAccessException: if the specified login session doesn't
            belong to the specified user.

        @raise UndefinedObjectException: if the specified identification
            doesn't refer to any user login session registered against the
            platform.
        """
        payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.DELETE,
                path='/account/session',
                authentication_required=True,
                signature_required=True))

        self.flush_session()

        return payload

    def sign_up_with_oauth(
            self, provider_name, user_id,
            oauth_consumer_key, oauth_consumer_secret, access_token,
            auto_sign_in=False):
        """
        Sign-up the user against the platform providing the OAuth access token
        used by the Consumer to gain access to to the Protected Resources on
        behalf of the User


        :param provider_name: code name of the Service Provider, such as, for
            instance, ``facebook``, ``twitter``, etc.

        :param user_id: identification of the 3rd party user account on the
            Service Provider.

        :param oauth_consumer_key: a value used by the Consumer to identify
            itself to the Service Provider.

        :param oauth_consumer_secret: a secret used by the Consumer to
            establish ownership of the Consumer Key.

        :param access_token: a value used by the Consumer to gain access to
            the Protected Resources on behalf of the User, instead of using
            the User’s Service Provider credentials.

        :param auto_sign_in: indicate whether the platform is requested to
            sign-in this user once the sign-up procedure completes
            successfully.


        @raise IllegalAccessException: if the identifier of the user that the
            specified OAuth token impersonates is not the identifier that is
            passed to the function.
        """
        session_payload = Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/account',
                arguments={
                    'auto_sign_in': auto_sign_in
                },
                message_body={
                    'access_token': access_token,
                    'oauth_consumer_key': oauth_consumer_key,
                    'oauth_consumer_secret': oauth_consumer_secret,
                    'provider_name': provider_name,
                    'user_id': user_id
                },
                authentication_required=False,
                signature_required=True))

        if auto_sign_in:
            self.set_session(self.session.connection.build_authenticated_session(session_payload))

        return session_payload

    @staticmethod
    def terminal_login(
            connection=None,
            reset_session_info=False,
            store_session_info=True,
            session_file_path_name=None):
        """
        Connect and log into a server platform as specified with connection
        properties, requesting the user to prove his identity to the server
        platform by providing his credentials.

        If a session has been already stored in the specified file, the
        function retrieves the connection and session properties from this
        file, update the connection instance ``connection`` passed to
        this function, and return a session instance built with these stored
        session properties.


        :param connection: an instance of ``PerseusConnection``
            containing the connection properties to the server platform.

        :param reset_session_info: indicate whether to reset session
            information that would have been previously stored on the local
            disk in the file specified by its path and name.

        :param store_session_info: indicate whether to store the session on
            the local disk with the specified path and file name.

        :param session_file_path_name: the path and the name of the file where
            the session information, and possibly the connection information,
            will be saved in.


        :return: An authenticated session of the user logged to the RESTful
            API server.
        """
        session = None

        # If the hostname and the port number of the Perseus RESTful API server
        # have not been defined, request the user to enter them.
        hostname = connection.hostname if connection and connection.hostname \
            else input("Enter the RESTful API server's hostname: ")

        port_number = connection.port_number if connection and connection.port_number \
            else PerseusConnection.DEFAULT_PORT_NUMBER

        # Check whether a login session of the user is already stored for this
        # RESTful API server.
        if session_file_path_name is None:
            session_file_path_name = '.%s.session' % hostname

        if os.path.exists(session_file_path_name):
            if reset_session_info:
                os.remove(session_file_path_name)
            else:
                try:
                    with open(session_file_path_name) as fd:
                        payload = json.loads(fd.read())
                        connection = PerseusConnection.from_json(hostname, payload, port_number=port_number)
                        return connection.build_session(payload)
                except ValueError:
                    pass

        # If the consumer key and secret have not been passed to the function,
        # request the user to enter them.
        consumer_key = connection.consumer_key if connection and connection.consumer_key \
            else input('Enter your Consumer Key: ')

        consumer_secret = connection.consumer_secret if connection and connection.consumer_secret \
            else getpass.getpass('Enter your Consumer Secret: ')

        if connection is None:
            connection = PerseusConnection(
                hostname,
                consumer_key,
                consumer_secret,
                port_number=port_number)

        # If the user is not already logged, request the user to provide his
        # credentials.
        if session is None:
            email_address = input("Enter your email address: ")
            password = getpass.getpass()
            session = AccountService(connection).__sign_in(email_address, password)

            if store_session_info:
                payload = Object()
                payload.merge(connection)
                payload.merge(session)

                with os.fdopen(os.open(session_file_path_name, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as handle:
                    handle.write(json.dumps(obj.stringify(payload)))

        return session
