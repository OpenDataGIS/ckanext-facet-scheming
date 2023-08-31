# encoding: utf-8

import pytest
import six
from ckan.lib.helpers import url_for
from bs4 import BeautifulSoup
import ckanext.facet_scheming.helpers as fs_helpers
import ckanext.facet_scheming.utils as fs_utils

from ckan.tests import factories

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock


#@pytest.mark.usefixtures("with_request_context")
class TestHome(object):
 
    def test_home_renders(self, app):
        response = app.get(url_for("home.index"))
        assert "Welcome to CKAN" in response.body

    def test_template_head_end(self, app):
        # test-core.ini sets ckan.template_head_end to this:
        test_link = (
            '<link rel="stylesheet" '
            'href="TEST_TEMPLATE_HEAD_END.css" type="text/css">'
        )
        response = app.get(url_for("home.index"))
        assert test_link in response.body

    def test_template_footer_end(self, app):
        # test-core.ini sets ckan.template_footer_end to this:
        test_html = "<strong>TEST TEMPLATE_FOOTER_END TEST</strong>"
        response = app.get(url_for("home.index"))
        assert test_html in response.body

    @pytest.mark.ckan_config(
        "ckan.legacy_route_mappings", '{"my_home_route": "home.index"}'
    )
    def test_map_pylons_to_flask_route(self, app):
        response = app.get(url_for("my_home_route"))
        assert "Welcome to CKAN" in response.body

        response = app.get(url_for("home"))
        assert "Welcome to CKAN" in response.body

    @pytest.mark.ckan_config(
        "ckan.legacy_route_mappings", {"my_home_route": "home.index"}
    )
    def test_map_pylons_to_flask_route_using_dict(self, app):
        response = app.get(url_for("my_home_route"))
        assert "Welcome to CKAN" in response.body

        response = app.get(url_for("home"))
        assert "Welcome to CKAN" in response.body
