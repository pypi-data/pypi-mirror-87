## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'view' template for mobile.  Features a basic field list, and
## links to edit/delete the object when appropriate.
## 
## ##############################################################################
<%inherit file="/mobile/base.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title}</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${instance_title}</%def>

${form.render()|n}

% if master.has_rows:

    % if master.mobile_rows_creatable and master.rows_creatable_for(instance):
        ## TODO: this seems like a poor choice of names? what are we really testing for here?
        % if master.mobile_rows_creatable_via_browse:
            <% add_title = "Add Record" if add_item_title is Undefined else add_item_title %>
            ${h.link_to(add_title, url('mobile.{}.create_row'.format(route_prefix), uuid=instance.uuid), class_='ui-btn ui-corner-all')}
        % endif
    % endif
    % if master.mobile_rows_quickable and master.rows_quickable_for(instance):
        <% placeholder = '' if quick_entry_placeholder is Undefined else quick_entry_placeholder %>
        ${h.form(url('mobile.{}.quick_row'.format(route_prefix), uuid=instance.uuid))}
        ${h.csrf_token(request)}
        % if quick_row_autocomplete:
            <div class="field autocomplete quick-row" data-url="${quick_row_autocomplete_url}">
              ${h.hidden('quick_entry')}
              ${h.text('quick_row_autocomplete_text', placeholder=placeholder, autocomplete='off', data_type='search')}
              <ul data-role="listview" data-inset="true" data-filter="true" data-input="#quick_row_autocomplete_text"></ul>
              <button type="button" style="display: none;">Change</button>
            </div>
        % else:
            ${h.text('quick_entry', placeholder=placeholder, autocomplete='off', **{'data-type': 'search', 'data-url': url('mobile.{}.quick_row'.format(route_prefix), uuid=instance.uuid), 'data-wedge': 'true' if quick_row_keyboard_wedge else 'false'})}
        % endif
        ${h.end_form()}
    % endif

    <br />
    ${grid.render_complete()|n}
% endif

% if master.mobile_editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
    ${h.link_to("Edit This", url('mobile.{}.edit'.format(route_prefix), uuid=instance.uuid), class_='ui-btn ui-corner-all')}
% endif
