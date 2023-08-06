import os

import requests
import json
from dnac.maglev.security.Session import Session
from dnac.maglev.security.role.ResourceType import ResourceType
from dnac.maglev.security.role.Role import Role
from dnac.exception.OperationNotPermittedException import OperationNotPermittedException
from dnac.exception.NoSessionException import NoSessionException
from dnac.exception.DnacException import DnacException
from dnac.utils.os.FileSystem import FileSystem


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com


class SecurityManager:
    def __init__(self, maglev, admin_credentials=('admin', 'Maglev123')):
        self._maglev_ = maglev
        self._admin_credentials = admin_credentials
        self._session_ = Session(admin_credentials, None)
        # self._session_ = Session(None, None)

    @property
    def maglev(self):
        return self._maglev_

    @property
    def dnacCluster(self):
        return self.maglev.ip

    @property
    def adminCredentials(self):
        return self._admin_credentials

    @adminCredentials.setter
    def adminCredentials(self, ac):
        self._admin_credentials = ac

    @property
    def session(self):
        return self._session_

    @session.setter
    def session(self, new_session):
        self._session_ = new_session

    @property
    def loginUrl(self):
        return '/api/system/v1/identitymgmt/login'

    #
    @property
    def XauthToken(self):
        return self.getAuthTokenFor(None)

    def getAuthTokenFor(self, credentials):
        if not self.session or not self.session.credentials:
            raise NoSessionException('No login session - you must login before executing any operations')

        xauth_cookie = None
        login_url = self.get_dnac_url(self.loginUrl)
        res = self.login_dnac(login_url, credentials if credentials else self.session.credentials)
        if not res:
            # Cannot login - no session
            return None
        hdrs = res.headers
        cookie_key = 'Set-Cookie'
        if cookie_key in hdrs.keys():
            cookies = hdrs[cookie_key]
            cookie = cookies.split(';')
            lst = cookie[0].split('=')
            xauth_cookie = lst[1]
        #
        return xauth_cookie

    #

    def dnac_cookie_header(self, cookie):
        if cookie:
            return ({'X-auth-token': cookie.strip()})
        return None

    #

    def get_dnac_url(self, url):
        return 'https://' + self.dnacCluster + url

    # Login to DNAC as the specified user
    def login_as(self, credentials):
        self.session = Session(credentials, None)

    #
    # Login to DNAC using the specified credentials
    def login_dnac(self, dnac_url, credentials):
        # with requests.Session() as session:
        try:
            return requests.get(dnac_url, auth=credentials, verify=False)
        except:# (ConnectionError, ReadTimeout):
            return None

    #
    def call_dnac_with_session(self, dnac_url, session_cookie):
        # with requests.Session() as session:
        cookie_header = self.dnac_cookie_header(session_cookie)
        response = requests.get(dnac_url, headers=cookie_header, verify=False)
        if response.status_code == 403:
            raise OperationNotPermittedException('Specified http operation <GET> is not permitted for this user')
        return response

    #
    def post_image_to_dnac(self, dnac_url, image):
        session_cookie = self.XauthToken
        with open(image, 'rb') as img:
            name_img = os.path.basename(image)
            files = {'image': (name_img, img, 'multipart/form-data', {'Expires': '0'})}
            with requests.Session() as s:
                s.headers.update(self.dnac_cookie_header(session_cookie))
                response = s.post(dnac_url if dnac_url.startswith('http') else self.get_dnac_url(dnac_url), files=files,
                                  verify=False)
                return response

        raise NotImplementedError('Specified http operation <', http_operation + '> is not implemented')

    def download_as(self, dnac_url, target_file):
        if not FileSystem.is_file_writable(target_file):
            raise OperationNotPermittedException('Specified file <', target_file , '> not writeable')

        session_cookie = self.XauthToken
        with open(target_file, 'wb') as target:
            with requests.Session() as s:
                s.headers.update(self.dnac_cookie_header(session_cookie))
                actual_url = dnac_url if dnac_url.startswith('http') else self.get_dnac_url(dnac_url)
                response = s.get(dnac_url if dnac_url.startswith('http') else self.get_dnac_url(dnac_url), verify=False)
                if response.status_code == 200:
                    target.write(response.content)
                    return
                raise DnacException('Failed to download specified file')

        raise NotImplementedError('Specified http operation <', http_operation + '> is not implemented')


    #
    #
    def post_to_dnac_with_session(self, dnac_url, json_payload, session_cookie, operation='post', given_headers=None):
        # with requests.Session() as session:
        http_operation = operation.lower()
        cookie_header = self.dnac_cookie_header(session_cookie)
        all_headers = given_headers if given_headers else {'Content-Type': 'application/json', 'Accept': '*/*'}
        all_headers.update(cookie_header)
        if http_operation == 'post':
            response = requests.post(dnac_url, headers=all_headers, data=json_payload, verify=False)
            if response.status_code == 403:
                raise OperationNotPermittedException('Specified http operation <',
                                                     http_operation + '> is not permitted for this user')
            return response

        if http_operation == 'put':
            response = requests.put(dnac_url, headers=all_headers, data=json_payload, verify=False)
            if response.status_code == 403:
                raise OperationNotPermittedException('Specified http operation <',
                                                     http_operation + '> is not permitted for this user')
            return response

        if http_operation == 'delete':
            response = requests.delete(dnac_url, headers=all_headers, verify=False)
            if response.status_code == 403:
                raise OperationNotPermittedException('Specified http operation <',
                                                     http_operation + '> is not permitted for this user')
            return response

        raise NotImplementedError('Specified http operation <', http_operation + '> is not implemented')

    #
    def call_dnac(self, url):
        return self.call_dnac_with_session(self.get_dnac_url(url), self.XauthToken)

    #
    def post_to_dnac(self, url, json_payload, operation='post', given_headers=None):
        return self.post_to_dnac_with_session(self.get_dnac_url(url), json_payload, self.XauthToken, operation,
                                              given_headers)

#
