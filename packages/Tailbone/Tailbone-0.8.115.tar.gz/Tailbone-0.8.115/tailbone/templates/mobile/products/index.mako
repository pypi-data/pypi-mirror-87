## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/index.mako" />

% if master.mobile_creatable and request.has_perm('{}.create'.format(permission_prefix)):
    ${h.link_to("New {}".format(model_title), url('mobile.{}.create'.format(route_prefix)), class_='ui-btn ui-corner-all')}
% endif

% if quick_lookup:

    ${h.form(url('mobile.{}.quick_lookup'.format(route_prefix)))}
    ${h.csrf_token(request)}
    ${h.text('quick_entry', placeholder=placeholder, autocomplete='off', **{'data-type': 'search', 'data-url': url('mobile.{}.quick_lookup'.format(route_prefix)), 'data-wedge': 'true' if quick_lookup_keyboard_wedge else 'false'})}
    ${h.end_form()}

% else: ## not quick_only
    ${grid.render_complete()|n}
% endif
