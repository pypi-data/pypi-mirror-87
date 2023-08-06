from valohai_cli.api import request


def get_datum_download_url(id):
    return request(
        method='get',
        url=f'/api/v0/data/{id}/download/',
    ).json()['url']
