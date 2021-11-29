from pathlib import Path

import pytest
from twisted.web.error import Error

from scrapyd.interfaces import IEggStorage


class TestWebservice:
    def test_list_spiders(self, txrequest, site_with_egg):
        txrequest.args = {
            b'project': [b'quotesbot']
        }
        endpoint = b'listspiders.json'
        content = site_with_egg.children[endpoint].render_GET(txrequest)
        assert content['spiders'] == ['toscrape-css', 'toscrape-xpath']
        assert content['status'] == 'ok'

    def test_list_versions(self, txrequest, site_with_egg):
        txrequest.args = {
            b'project': [b'quotesbot'],
            b'spider': [b'toscrape-css']
        }
        endpoint = b'listversions.json'
        content = site_with_egg.children[endpoint].render_GET(txrequest)
        assert content['versions'] == ['0_1']
        assert content['status'] == 'ok'

    def test_list_projects(self, txrequest, site_with_egg):
        txrequest.args = {
            b'project': [b'quotesbot'],
            b'spider': [b'toscrape-css']
        }
        endpoint = b'listprojects.json'
        content = site_with_egg.children[endpoint].render_GET(txrequest)
        assert content['projects'] == ['quotesbot']

    def test_delete_version(self, txrequest, site_with_egg):
        endpoint = b'delversion.json'
        txrequest.args = {
            b'project': [b'quotesbot'],
            b'version': [b'0.1']
        }

        storage = site_with_egg.app.getComponent(IEggStorage)
        egg = storage.get('quotesbot')
        assert egg[0] is not None
        content = site_with_egg.children[endpoint].render_POST(txrequest)
        assert content['status'] == 'ok'
        assert 'node_name' in content
        assert storage.get('quotesbot')
        no_egg = storage.get('quotesbot')
        assert no_egg[0] is None

    def test_delete_project(self, txrequest, site_with_egg):
        endpoint = b'delproject.json'
        txrequest.args = {
            b'project': [b'quotesbot'],
        }

        storage = site_with_egg.app.getComponent(IEggStorage)
        egg = storage.get('quotesbot')
        assert egg[0] is not None

        content = site_with_egg.children[endpoint].render_POST(txrequest)
        assert content['status'] == 'ok'
        assert 'node_name' in content
        assert storage.get('quotesbot')
        no_egg = storage.get('quotesbot')
        assert no_egg[0] is None

    def test_addversion(self, txrequest, site_no_egg):
        endpoint = b'addversion.json'
        txrequest.args = {
            b'project': [b'quotesbot'],
            b'version': [b'0.1']
        }
        egg_path = Path(__file__).absolute().parent / "quotesbot.egg"
        with open(egg_path, 'rb') as f:
            txrequest.args[b'egg'] = [f.read()]

        storage = site_no_egg.app.getComponent(IEggStorage)
        egg = storage.get('quotesbot')
        assert egg[0] is None

        content = site_no_egg.children[endpoint].render_POST(txrequest)
        assert content['status'] == 'ok'
        assert 'node_name' in content
        assert storage.get('quotesbot')
        no_egg = storage.get('quotesbot')
        assert no_egg[0] == '0_1'

    @pytest.mark.parametrize('endpoint,attach_egg,method', [
        (b'addversion.json', True, 'render_POST'),
        (b'delproject.json', False, 'render_POST'),
        (b'delversion.json', False, 'render_POST'),
        (b'listspiders.json', False, 'render_GET'),
        (b'listjobs.json', False, 'render_GET'),
        (b'listprojects.json', False, 'render_GET')
    ])
    def test_bad_project_names(self, txrequest, site_no_egg,
                               endpoint, attach_egg, method):
        txrequest.args = {
            b'project': [b'/home/pawel/hosts'],
            b'version': [b'0.1'],
        }
        egg_path = Path(__file__).absolute().parent / "quotesbot.egg"
        if attach_egg:
            with open(egg_path, 'rb') as f:
                txrequest.args[b'egg'] = [f.read()]

        with pytest.raises(Error) as e:
            resource = site_no_egg.children[endpoint]
            getattr(resource, method)(txrequest)
            assert e.args[0] == 400

        storage = site_no_egg.app.getComponent(IEggStorage)
        egg = storage.get('quotesbot')
        assert egg[0] is None
