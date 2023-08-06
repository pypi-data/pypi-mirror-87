import requests

from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from hns_tr069_sdk.axiros.exceptions import *
from typing import List
from datetime import datetime
from time import sleep


class HTTPtimeoutAdapter(HTTPAdapter):
    """ Adds timeout to requests HTTP adapter """

    def __init__(self, timeout: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def send(self, *args, **kwargs):
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout
        return super(HTTPtimeoutAdapter, self).send(*args, **kwargs)


class AxirosBase(requests.Session):

    _HEADERS = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }

    def __init__(
            self,
            acs_api_url: str,
            acs_username: str,
            acs_password: str,
            wait_timeout: int = 45,
            global_timeout: int = 5
    ):

        super().__init__()
        self.acs_api_url = acs_api_url
        self.acs_username = acs_username
        self.acs_password = acs_password
        self.wait_timeout = wait_timeout

        self._adapter = HTTPtimeoutAdapter(global_timeout)
        self.mount('http://', self._adapter)
        self.mount('https://', self._adapter)

        self.headers.update(self._HEADERS)
        self.auth = HTTPBasicAuth(username=self.acs_username, password=self.acs_password)

    def __repr__(self):
        return f'{self.__class__.__name__}(acs_api_url="{self.acs_api_url}, acs_username={self.acs_username}")'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def close_session(self):
        """ Closes requests session """

        self.close()

    @staticmethod
    def _parse_resp(resp: requests.Response, method: str, method_params: dict = None) -> dict:
        if resp.ok:
            data = resp.json()
            if data['Result']['code'] == 500:
                raise SBError(
                    response_content=resp.content.decode(),
                    response_status=resp.status_code,
                    msg=f'South bound call error for method: {method}, request params: {method_params}'
                )
            elif data['Result']['code'] == 507:
                raise SBTimeoutError(
                    response_content=resp.content.decode(),
                    response_status=resp.status_code,
                    msg=f'South bound call timeout error for method: {method}, request params: {method_params}'
                )
            elif data['Result']['code'] == 508:
                raise SBCancelledError(
                    response_content=resp.content.decode(),
                    response_status=resp.status_code,
                    msg=f'South bound call cancelled error for method: {method}, request params: {method_params}'
                )
            return data
        raise ResponseNotOkError(
            response_content=resp.content.decode(),
            response_status=resp.status_code,
            msg=f'Response not ok for method: {method}, request params: {method_params}'
        )

    @staticmethod
    def _parse_ticketid(resp: dict) -> int:
        return resp['Result']['ticketid']

    def _southbound_call(self, method: str, method_params: dict, timeout: int = None) -> dict:
        """ Generic call to perform a southbound action on ACS """

        ticketid = self.create_ticket(method, method_params)
        current = datetime.now()
        if timeout:
            wait_timeout = timeout
        else:
            wait_timeout = self.wait_timeout

        while True:
            delta = datetime.now() - current
            output = self.get_ticket_output(ticketid)
            if output['Result']['code'] == 200:
                return output
            elif delta.seconds > wait_timeout:
                raise SBTimeoutError(
                    response_content='',
                    response_status=507,
                    msg=f'Timeout getting ticket output for {method} with method params: {method_params}. '
                        f'ACS result: {output}'
                )
            else:
                sleep(1)

    def post(self, method: str, post_data: dict, **kwargs) -> requests.Response:
        return super(AxirosBase, self).post(url=f'{self.acs_api_url}/{method}', json=post_data, **kwargs)

    def create_ticket(self, method: str, method_params: dict) -> int:
        """
        Creates a ticket on ACS for the method specified
        :param method: ACS method name
        :param method_params: Parameters for the method call
        :return: ticketid
        """

        resp = self.post(method, post_data=method_params)
        output = self._parse_resp(resp, method, method_params)
        return self._parse_ticketid(output)

    def get_ticket_output(self, ticketid: int) -> dict:
        """
        Gets response from ticket created on ACS
        :param ticketid: ticket id
        :return: ticket response
        """

        method = 'get_generic_sb_result'
        ticket_params = {'ticketid': ticketid}
        resp = self.post(method, post_data=ticket_params)
        return self._parse_resp(resp, method, method_params=ticket_params)

    def get_parameter_value(self, method_params: dict) -> List[dict]:
        """
        Performs TR069 GetParameterValues call
        :param method_params: ACS method call parameters
        :return: Parameter values
        example:
            [{'value': 3600, 'key': 'InternetGatewayDevice.ManagementServer.PeriodicInformInterval'}]
        :raise SBTimeoutError: If unable to get the output in the timeout period
        """

        method = 'GetParameterValues'
        output = self._southbound_call(method, method_params)
        return output['Result']['details']

    def set_parameter_value(self, method_params: dict) -> bool:
        """
        Performs TR069 SetParameterValues call
        :param method_params: ACS method call parameters
        :return: True if set was successful else False
        :raise SBTimeoutError: If unable to get the output in the timeout period
        """

        method = 'SetParameterValues'
        output = self._southbound_call(method, method_params)
        if output:
            return True
        return False

    def delete_cpe(self, cpe_id: str):
        """
        Deletes CPE
        :param cpe_id: CPE ID/Serial Number
        :return: None
        :raise ACSDeleteError: If failed to delete cpe
        :raise CPENotFoundError: If CPE is not found on TR069
        """

        method = 'DeleteCPEs'
        method_params = {
            'CPESearchOptions': {'cpeid': cpe_id},
            'CommandOptions': {'limit': 1}
        }
        res = self.post(method, method_params)
        if res.ok:
            if res.json()['Result']['code'] == 200:
                return
            elif res.json()['Result']['code'] == 400 \
                    and "Can't find CPE Objects" in res.json()['Result']['message']:
                raise CPENotFoundError(f'CPE ID: {cpe_id} not found on TR069 server')
        raise ACSDeleteError(f'Failed to delete CPE: {cpe_id}. ACS response: {res.content}')

    def factory_reset_cpe(self, cpe_id: str):
        """
        Factory resets CPE via TR069
        :param cpe_id: CPE ID/Serial Number
        :return:
        """

        method = 'FactoryReset'
        method_params = {
            'CPEIdentifier': {'cpeid': cpe_id},
            'CommandOptions': ''
        }
        try:
            _ = self._southbound_call(method, method_params)
            return
        except SBTimeoutError as timeout_error:
            raise FactoryResetFailedError(
                response_status=timeout_error.response_status,
                response_content=timeout_error.response_content,
                msg=f'Failed to factory reset CPE: {cpe_id}'
            ) from timeout_error


class AxirosACS(AxirosBase):

    def __init__(
            self,
            acs_api_url: str,
            acs_username: str,
            acs_password: str,
            wait_timeout: int = 45,
            global_timeout: int = 5
    ):
        """
        API to Axiros TR069 ACS
        :param acs_api_url: ACS API URL
        :param acs_username: ACS Username
        :param acs_password: ACS Password
        :param wait_timeout: Number of seconds before a timeout error is raised when getting the south bound call result
        :param global_timeout: Request timeout in seconds for every request within the session
        """
        super().__init__(
            acs_api_url,
            acs_username,
            acs_password,
            wait_timeout,
            global_timeout
        )

    def cpe_online(self, cpe_id: str) -> bool:
        """
        Checks if the CPE is online by querying for the parameter value:
        InternetGatewayDevice.ManagementServer.PeriodicInformInterval
        :param cpe_id: CPE ID/Serial Number
        :return: True if online else False
        """

        method_params = {
            'CPEIdentifier': {'cpeid': cpe_id},
            'CommandOptions': '',
            'Parameters': ['InternetGatewayDevice.ManagementServer.PeriodicInformInterval']
        }
        if self.get_parameter_value(method_params):
            return True
        return False

