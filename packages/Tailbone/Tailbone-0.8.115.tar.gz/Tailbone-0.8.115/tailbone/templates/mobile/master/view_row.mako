## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

<%def name="title()">${index_title} &raquo; ${parent_title} &raquo; ${instance_title}</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${h.link_to(parent_title, parent_url)} &raquo; ${instance_title}</%def>

${form.render()|n}

% if master.mobile_rows_editable and instance_editable and request.has_perm('{}.edit_row'.format(permission_prefix)):
  ${h.link_to("Edit", url('mobile.{}.edit_row'.format(route_prefix), uuid=instance.batch_uuid, row_uuid=instance.uuid), class_='ui-btn')}
% endif

% if master.mobile_rows_deletable and master.row_deletable(row) and request.has_perm('{}.delete_row'.format(permission_prefix)):
    ${h.form(url('mobile.{}.delete_row'.format(route_prefix), uuid=parent_instance.uuid, row_uuid=row.uuid))}
    ${h.csrf_token(request)}
    ${h.submit('submit', "Delete this Row")}
    ${h.end_form()}
% endif
