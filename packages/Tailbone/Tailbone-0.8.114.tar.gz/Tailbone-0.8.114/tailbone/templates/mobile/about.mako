## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />
<%namespace name="base_meta" file="/base_meta.mako" />

<%def name="title()">About ${base_meta.app_title()}</%def>

<h2>${project_title} ${project_version}</h2>

% for name, version in packages.items():
    <h3>${name} ${version}</h3>
% endfor

<p>Please see <a href="https://rattailproject.org/">rattailproject.org</a> for more info.</p>
