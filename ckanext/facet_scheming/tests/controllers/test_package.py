# encoding: utf-8

import pytest
import six
from ckan.lib.helpers import url_for
from bs4 import BeautifulSoup
import ckanext.facet_scheming.helpers as fs_helpers
import ckanext.facet_scheming.utils as fs_utils
from ckanext.facet_scheming.tests.config import fake_context as fake_context
import ckanext.facet_scheming.tests.utils as test_utils

import ckan.tests.helpers as helpers
import ckan.tests.factories as factories

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

def _package_show(_context, _data_dict):
    _context['package']={}
        

@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestPackage(object):
    def test_new_tags(self, app):
        dataset = factories.Dataset(**test_utils.create_fake_context())
        response = app.get(url_for("dataset.read", id=dataset["name"]))
        assert helpers.body_contains(response, "Linked Data")
        assert helpers.body_contains(response, "Geospatial Metadata")

    def test_linked_data_tab(self, app):
        dataset = factories.Dataset(**fake_context)
        response = app.get(url_for("facet_scheming.index",id=dataset["name"]))
        assert helpers.body_contains(response, f"dataset/{dataset['name']}.rdf")
        assert helpers.body_contains(response, f"dataset/{dataset['name']}.xml")
        assert helpers.body_contains(response, f"dataset/{dataset['name']}.n3")
        assert helpers.body_contains(response, f"dataset/{dataset['name']}.ttl")
        assert helpers.body_contains(response, f"dataset/{dataset['name']}.jsonld")

    def test_geospatial_metadata_tab(self, app):
        dataset = factories.Dataset(**fake_context)
        inspire_link="/csw/?service=CSW&version=2.0.2&request=GetRecordById&id={id}&elementSetName=full&outputSchema={schema}"
        response = app.get(url_for("facet_scheming.inspire",id=dataset["name"]))
        
        assert helpers.body_contains(response, inspire_link.format(id=dataset['name'],schema="http://www.isotc211.org/2005/gmd"))
        assert helpers.body_contains(response, inspire_link.format(id=dataset['name'],schema="http://www.opengis.net/cat/csw/2.0.2"))
        assert helpers.body_contains(response, inspire_link.format(id=dataset['name'],schema="http://www.w3.org/2005/Atom"))
        assert helpers.body_contains(response, inspire_link.format(id=dataset['name'],schema="http://www.opengis.net/cat/csw/csdgm"))

@pytest.mark.usefixtures("clean_db", "clean_index")
class TestFrontendFacets(object):
    def test_facets_display(self,app):
        org = factories.Organization(name="test-org-facet", title="Test Org")
        factories.Dataset(**test_utils.create_fake_context(owner_org=org["id"],theme_es="http://datos.gob.es/kos/sector-publico/sector/medio-ambiente"))
        factories.Dataset(**test_utils.create_fake_context(owner_org=org["id"],theme_es="http://datos.gob.es/kos/sector-publico/sector/medio-ambiente"))
        
        response = app.get(url_for("dataset.search"))
        html = BeautifulSoup(response.body)
        
        #Recojo el módulo de filtros
        filter_item = html.find("div",class_="filters").find("div")
        assert filter_item is not None, "No se ha generado la columna de facets"
        
        section = filter_item.find_all("section", class_="module")
        
        assert "Themes (NTI-RISP)" in [y for x in section for y in x.find("h2").stripped_strings], "No se ha generado el facet Themes (NTI-RISP)"

        assert 1 == len([z for x in section if "Themes (NTI-RISP)"
                     in x.find("h2").stripped_strings for y 
                     in x.find_all("span",class_="item-count") for z
                     in y.string if "2" in y]), "El facet Themes (NTI-RISP) no tiene el número esperado de elementos"

        assert 1 == len([y['href'] 
                         for x in section if "Themes (NTI-RISP)" in x.find("h2").stripped_strings 
                         for y in x.find_all("a") if "dataset/?theme_es=http%3A%2F%2Fdatos.gob.es%2Fkos%2Fsector-publico%2Fsector%2Fmedio-ambiente" in y['href']
                         ]), "El facet Themes (NTI-RISP) no tiene el enlace esperado"
        

