import pytest

from chris.app.app import App
from chris.app.http_codes import HTTPCodes


class TestApp:

    @pytest.fixture
    def client(self):
        app = App()
        app._app.config['TESTING'] = True

        with app._app.test_client() as client:
            yield client

    def test_get_projects(self, client):
        route = 'v1/projects'
        response = client.get(route)
        assert response.status_code == HTTPCodes.SUCCESS_GENERAL
        assert len(response.json) > 20
        assert 'project_id' in response.json[0]
