from jupyhai.utils.auth import login_status
from valohai_cli.api import request
from valohai_cli.ctx import set_project_link
from valohai_cli.exceptions import APINotFoundError
from valohai_cli.settings import settings

from jupyhai import consts
from jupyhai.api_urls import PROJECTS_URL
from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import (
    get_current_environment,
    get_current_ignore,
    get_current_image,
    get_current_project,
    get_current_title,
    get_current_host_is_minihai,
)


class SettingsHandler(JupyhaiHandler):
    def get(self):
        project = get_current_project()
        result = {
            'project': getattr(project, 'id', None) or '',
            'environment': get_current_environment(),
            'image': get_current_image(),
            'title': get_current_title(),
            'ignore': get_current_ignore(),
            'hostIsMinihai': get_current_host_is_minihai(),
        }
        self.finish({'result': result})

    def post(self):
        args = self.get_json_body()
        project_id = args['project_id']
        image = args['image']
        title = args['title']
        ignore = args['ignore']
        environment_id = args.get('environment_id')
        host_is_minihai = args.get('host_is_minihai')
        self.set_jupyhai_settings(project_id, environment_id, image, title, ignore, host_is_minihai)
        self.finish({'success': True})

    def set_jupyhai_settings(self, project_id, environment, image, title, ignore, host_is_minihai):
        project = get_current_project()
        logged_in = login_status()
        if logged_in and (getattr(project, 'id', None) != project_id) and project_id:
            self.link_project(project_id)
        settings.persistence.update(
            jupyhai_image=image,
            jupyhai_environment=environment,
            jupyhai_title=title,
            jupyhai_ignore=ignore,
            jupyhai_host_is_minihai=host_is_minihai,
        )
        settings.persistence.save()

    def link_project(self, id):
        try:
            response = request('get', '%s%s/' % (PROJECTS_URL, id))
            responseJSON = response.json()
        except APINotFoundError:
            self.log.error('No Project %s found.' % id)
            return

        os_path = consts.ROOT_DIRECTORY
        if responseJSON:
            set_project_link(os_path, responseJSON)
        else:
            self.log.info(responseJSON)
            self.log.info("Error in linking project %s" % (id))
