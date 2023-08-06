## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />
<%namespace name="base_meta" file="/base_meta.mako" />

<%def name="title()">Home</%def>

<%def name="page_title()"></%def>

<div style="text-align: center;">
  ${h.image(image_url, "{} logo".format(capture(base_meta.app_title)), id='logo', width=300)}
  <h3>Welcome to ${base_meta.app_title()}</h3>
</div>
