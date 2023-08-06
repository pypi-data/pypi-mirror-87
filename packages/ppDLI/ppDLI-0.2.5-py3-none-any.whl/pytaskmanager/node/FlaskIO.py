import logging
import requests
import time
import jwt
import datetime

from typing import NamedTuple

module_name = __name__.split('.')[1]

class ServerInfo(NamedTuple):
    """Data-class to store the server info"""
    host: str
    port: int 
    path: str

class ClientBaseProtocol(object):
    """Implemention base protocols for communicating with server instance"""

    def __init__(self, host: str, port: int, path: str='/api'):
        """Set connection parameters"""
        self.log = logging.getLogger(module_name)

        # server settings
        self.__host = host
        self.__port = port
        self.__api_path = path

        # tokens
        self._access_token = None
        self.__refresh_token = None
        self.__refresh_url = None
    
    def generate_path_to(self, endpoint: str):
        """Generate URL from host port and endpoint"""
        if endpoint.startswith('/'):
            path = self.base_path + endpoint
        else:
            path = self.base_path + '/' + endpoint

        self.log.debug(f"Generated path to {path}")
        return path
    
    def request(self, endpoint: str, json: dict=None, method: str='get', params=None):
        """Execute (protected) HTTP request to the server with payload, parameters
        
        raise an error if status code > 200
        return JSON formatted data
        """
        
        assert self._access_token

        # get appropiate method 
        rest_method = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }.get(method.lower(), 'get')

        # send request to server
        url = self.generate_path_to(endpoint)
        self.log.debug(f'Making request: {method.upper()} | {url}')
        response = rest_method(url, json=json, headers=self.headers, params=params)

        # server says no!
        if response.status_code > 200:
            # self.log.debug(f"Server did respond code={response.status_code}\
            #     and message={response.get('msg', 'None')}")
            self.log.error(f'Server responded with error code: {response.status_code}')
            self.log.debug(response)

            # FIXME: this should happen only *once* to prevent infinite recursion!
            # refresh token and try again
            self.refresh_token()
            return self.request(endpoint, json=json, method=method)

        # self.log.debug(f"Response data={response.json()}")
        return response.json()
    
    def authenticate(self, credentials: dict, path="token/user"):
        """Authenticate using credentials"""
        self.log.debug(f"Authenticating using {credentials}")

        # authenticate
        url = self.generate_path_to(path)
        response = requests.post(url, json=credentials)
        data = response.json()
        
        # handle negative responses    
        if response.status_code > 200:
            self.log.critical(f"Failed to authenticate {data.get('msg')}")
            raise Exception("Failed to authenticate")

        # store tokens
        self.log.info("successfully authenticated")
        self._access_token = data.get("access_token")
        self.__refresh_token = data.get("refresh_token")
        self.__refresh_url = data.get("refresh_url")

    def refresh_token(self):
        self.log.info("Refreshing token")
        assert self.__refresh_url

        # send request to server
        if self.__port:
            url = f"{self.__host}:{self.__port}{self.__refresh_url}"
        else:
            url = f"{self.__host}{self.__refresh_url}"

        response = requests.post(url, headers={
            'Authorization': 'Bearer ' + self.__refresh_token})

        # server says no!
        if response.status_code != 200:
            self.log.critical("Could not refresh token")
            raise Exception("Authentication Error!")
        
        self._access_token = response.json()["_access_token"]

    def post_task(self, name, image, collaboration_id, input_='', 
        description='', organization_ids :list=[]):
        return self.request('task', method='post', json={
            "name": name,
            "image": image, 
            "collaboration_id": collaboration_id,
            "input": input_,
            "description": description,
            "organization_ids": organization_ids
        })

    def get_results(self, id=None, state=None, include_task=False, task_id=None, node_id=None):
        
        # create formatted params
        params = dict()
        if state:
            params['state'] = state
        if include_task:
            params['include'] = 'task'
        if task_id:
            params['task_id'] = task_id
        if node_id:
            params['node_id'] = node_id
        
        self.log.debug(f"obtaining results using params={params}")
        return self.request(
            endpoint='result' if not id else f'result/{id}', 
            params=params
        )
    
    @property
    def headers(self):
        if self._access_token:
            return {'Authorization': 'Bearer ' + self._access_token}
        else:
            return {}
    
    @property
    def token(self):
        return self._access_token

    @property
    def host(self):
        return self.__host
    
    @property
    def port(self):
        return self.__port

    @property
    def path(self):
        return self.__api_path

    @property
    def base_path(self):
        if self.__port:
            return f"{self.host}:{self.port}{self.__api_path}"

        return f"{self.host}{self.__api_path}"
        # return self.host + ':' + str(self.port) + self.__api_path


class ClientUserProtocol(ClientBaseProtocol):
    """Specific commands for the user"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None

    def authenticate(self, username: str, password: str):
        super(ClientUserProtocol, self).authenticate({
            "username": username,
            "password": password
        }, path="token/user")

        # obtain the server authenticatable id
        self.id = jwt.decode(self.token, verify=False)['identity']
    
    

class ClientContainerProtocol(ClientBaseProtocol):
    """Specific commands for the container"""
    
    def __init__(self, token:str, *args, **kwargs):
        """All permissions of the container are derived from the 
        container."""

        super().__init__(*args, **kwargs)

        # obtain the identity from the token
        container_identity = jwt.decode(token, verify=False)['identity']
        self.image =  container_identity.get("image")
        self.host_node_id = container_identity.get("node_id")
        self.collaboration_id = container_identity.get("collaboration_id")

        self.log.info(
            f"Container in collaboration_id={self.collaboration_id} \n"
            f"Key created by node_id {self.host_node_id} \n"
            f"Can only use image={self.image}"
        )

        self._access_token = token
        self.log.debug(f"Access token={self._access_token}")

    def authenticate(self):
        """Containers obtain their key via their host Node."""
        return
    def refresh_token(self):
        """Containers cannot refresh their token."""
        #TODO we might want to notify node/server about this...
        raise Exception("Containers cannot refresh!")

    def get_results(self, task_id: int):
        """Containers should be allowed to obtain the data of their 
        children."""
        return self.request(
            f"task/{task_id}/result"
        )
        
    def create_new_task(self, input_, organization_ids=[]):
        return self.post_task(
            name="subtask",
            description=f"task from container on node_id={self.host_node_id}",
            collaboration_id=self.collaboration_id,
            organization_ids=organization_ids,
            input_=input_,
            image=self.image
        )
    
    def get_organizations_in_my_collaboration(self):
        organizations = self.request(
            f"collaboration/{self.collaboration_id}/organization")
        return organizations
        # return list(map(lambda organization: organization.id, organizations))


class ClientNodeProtocol(ClientBaseProtocol):
    """Specific commands/properties for the node"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # server properties from this instance
        self.id = None
        self.name = None
        self.collaboration_id = None
    
    def authenticate(self, api_key: str):
        """Nodes authenticate using an API-key"""
        super(ClientNodeProtocol, self).authenticate(
            {"api_key": api_key}, path="token/node")

        # obtain the server authenticatable id
        self.id = jwt.decode(self.token, verify=False)['identity']

        # get info on how the server sees me
        node = self.request(f"node/{self.id}")
        self.name = node.get("name")
        self.collaboration_id = node.get("collaboration")
        
    def request_token_for_container(self, task_id: int, image: str):
        """Generate a token that can be used by a docker container"""
        self.log.debug
        (f"requesting container token for task_id={task_id} and image={image}")
        return self.request('/token/container', method="post", json={
            "task_id": task_id,
            "image": image
        })

    def get_results(self, id=None, state=None, include_task=False, task_id=None):
        return super().get_results(
            id=id,
            state=state,
            include_task=include_task,
            task_id=task_id,
            node_id=self.id
        )

    def set_task_start_time(self, id: int):
        self.patch_results(id, result={
            "started_at": datetime.datetime.now().isoformat()
        })

    def patch_results(self, id: int, result: dict):
        # self.log.debug(f"patching results={result}")
        return self.request(f"result/{id}", json=result, method='patch')
