from apispec import APISpec

from .operation import Operation
from .plugins import MultiOperationBuilderPlugin
import re


class Spec(object):
    OPENAPI_VERSION = '3.0.0'

    def __init__(self, postman_collection):
        self.postman_collection = postman_collection
        self._servers = ['http://localhost']

    @property
    def info(self):
        return self.get_info()

    @property
    def openapi(self):
        return Spec.OPENAPI_VERSION

    @property
    def servers(self):
        return self.get_servers()

    def add_servers(self, server):
        if isinstance(server, list):
            self._servers.extend(server)
        else:
            self._servers.append(server)
        return self

    def get_info(self, version='1.0.0'):
        return dict(
            title=self.postman_collection.name,
            description=self.postman_collection.description,
            version=version
        )

    def get_servers(self):
        return self._servers

    def convert(self, yaml=False, references=True, ignorespec=None, **options):
        spec = APISpec(
            title=self.info.get('title'),
            version=self.info.get('version'),
            openapi_version=self.openapi,
            plugins=[MultiOperationBuilderPlugin(references)],
            **options
        )
        results = []  # use a normal dictionary for our output
        server_url = []
        for requestitem in self.postman_collection.get_requestitems():
            try:
                requestitem_dict = requestitem.__dict__
                raw_url = requestitem_dict['requestitem']['request']['url']['raw']
                raw_path = '/'.join(requestitem_dict['requestitem']['request']['url']['path'])
                s_url = re.sub(raw_path,'',raw_url)
                if s_url[-1] == "/":
                    server_url.append(s_url[:-1])
                else:
                    server_url.append(s_url)
                spec.path(
                    path=requestitem.get_request().path,
                    operations=Operation(requestitem, ignorespec=ignorespec).get()
                )


            except Exception:
                pass
        for server in set(server_url):
            results.append({"url": server})
        server_list = {"servers": results}
        return spec.to_yaml() if yaml else spec.to_dict(), server_list
