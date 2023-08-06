## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/purchases.css'))}
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('{}.download_excel'.format(permission_prefix)):
      <li>${h.link_to("Download {} as Excel".format(model_title), url('{}.download_excel'.format(route_prefix), uuid=batch.uuid))}</li>
  % endif
</%def>

${parent.body()}
