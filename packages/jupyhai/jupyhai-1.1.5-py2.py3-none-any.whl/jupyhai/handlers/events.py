from urllib.parse import urljoin

import aiohttp
from valohai_cli.api import get_host_and_token

from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import get_current_project


class EventsHandler(JupyhaiHandler):
    async def get(self, execution_id):
        self.finish({'results': await self.get_execution_events(execution_id)})

    async def get_execution_events(self, executionid):
        project = get_current_project()

        host, token = get_host_and_token()
        params = {'project': project.id}
        headers = {'Authorization': 'Token %s' % token}
        url = urljoin(host, '/api/v0/executions/%s/events/') % executionid

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                responseJSON = await response.json()
                if not responseJSON or not responseJSON['events']:
                    return

                return responseJSON['events']
