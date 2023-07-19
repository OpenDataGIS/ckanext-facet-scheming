# encoding: utf-8
import ckan.model as model
import ckan.lib.base as base
import ckan.logic as logic
from flask import Blueprint
from ckanext.facet_scheming.utils import get_linked_data, get_inspire

from ckan.plugins.toolkit import render, g

from logging import getLogger

logger = getLogger(__name__)
get_action = logic.get_action

fscheming = Blueprint(u'facet_scheming', __name__)


@fscheming.route(u'/dataset/linked_data/<id>')
def index(id):
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': g.user,
        u'for_view': True,
        u'auth_user_obj': g.userobj
    }
    data_dict = {u'id': id, u'include_tracking': True}

    # check if package exists
    try:
        pkg_dict = get_action(u'package_show')(context, data_dict)
        pkg = context[u'package']
    except (logic.NotFound, logic.NotAuthorized):
        return base.abort(404, _(u'Dataset {dataset} not found').format({dataset:id}))

    return render('facet_scheming/custom_data/index.html',extra_vars={
            u'pkg_dict': pkg_dict,
            u'endpoint': 'dcat.read_dataset',
            u'data_list': get_linked_data(id),
        })

@fscheming.route(u'/dataset/inspire/<id>')
def inspire(id):
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': g.user,
        u'for_view': True,
        u'auth_user_obj': g.userobj
    }
    data_dict = {u'id': id, u'include_tracking': True}

    # check if package exists
    try:
        pkg_dict = get_action(u'package_show')(context, data_dict)
        pkg = context[u'package']
    except (logic.NotFound, logic.NotAuthorized):
        return base.abort(404, _(u'Dataset {dataset} not found').format({dataset:id}))

    return render('facet_scheming/custom_data/index.html',extra_vars={
            u'pkg_dict': pkg_dict,
            u'id': id,
            u'data_list': get_inspire(),
        })
