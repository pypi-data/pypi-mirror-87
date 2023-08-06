## -*- coding: utf-8; -*-
<%namespace file="/grids/nav.mako" import="grid_index_nav" />
<%namespace file="/feedback_dialog.mako" import="feedback_dialog" />
<%namespace name="base_meta" file="/base_meta.mako" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${base_meta.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${base_meta.favicon()}
    ${self.header_core()}

    % if background_color:
        <style type="text/css">
          body, .navbar, .footer {
              background-color: ${background_color};
          }
        </style>
    % endif

    % if not request.rattail_config.production():
        <style type="text/css">
          body, .navbar, .footer {
            background-image: url(${request.static_url('tailbone:static/img/testing.png')});
          }
        </style>
    % endif

    ${self.head_tags()}
  </head>

  <body>
    <header>

      <nav class="navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-menu">
          <div class="navbar-start">

            % for topitem in menus:
                % if topitem.is_link:
                    ${h.link_to(topitem.title, topitem.url, target=topitem.target, class_='navbar-item')}
                % else:
                    <div class="navbar-item has-dropdown is-hoverable">
                      <a class="navbar-link">${topitem.title}</a>
                      <div class="navbar-dropdown">
                        % for subitem in topitem.items:
                            % if subitem.is_sep:
                                <hr class="navbar-divider">
                            % else:
                                ${h.link_to(subitem.title, subitem.url, class_='navbar-item', target=subitem.target)}
                            % endif
                        % endfor
                      </div>
                    </div>
                % endif
            % endfor

          </div><!-- navbar-start -->
          <div class="navbar-end">

            ## User Menu
            % if request.user:
                <div class="navbar-item has-dropdown is-hoverable">
                  % if messaging_enabled:
                      <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}${" ({})".format(inbox_count) if inbox_count else ''}</a>
                  % else:
                      <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}</a>
                  % endif
                  <div class="navbar-dropdown">
                    % if request.is_root:
                        ${h.link_to("Stop being root", url('stop_root'), class_='navbar-item root-user')}
                    % elif request.is_admin:
                        ${h.link_to("Become root", url('become_root'), class_='navbar-item root-user')}
                    % endif
                    % if messaging_enabled:
                        ${h.link_to("Messages{}".format(" ({})".format(inbox_count) if inbox_count else ''), url('messages.inbox'), class_='navbar-item')}
                    % endif
                    ${h.link_to("Change Password", url('change_password'), class_='navbar-item')}
                    ${h.link_to("Logout", url('logout'), class_='navbar-item')}
                  </div>
                </div>
            % else:
                ${h.link_to("Login", url('login'), class_='navbar-item')}
            % endif

          </div><!-- navbar-end -->
        </div>
      </nav>

      <nav class="level">
        <div class="level-left">

          ## App Logo / Name
          <div class="level-item">
            <a class="home" href="${url('home')}">
              <div id="header-logo">${base_meta.header_logo()}</div>
              <span class="global-title">${base_meta.global_title()}</span>
            </a>
          </div>

          ## Current Context
          <div id="current-context" class="level-item">
            % if master:
                <span>&raquo;</span>
                % if master.listing:
                    <span>${index_title}</span>
                % else:
                    ${h.link_to(index_title, index_url)}
                    % if parent_url is not Undefined:
                        <span>&raquo;</span>
                        ${h.link_to(parent_title, parent_url)}
                    % elif instance_url is not Undefined:
                        <span>&raquo;</span>
                        ${h.link_to(instance_title, instance_url)}
                    % endif
                    % if master.viewing and grid_index:
                        ${grid_index_nav()}
                    % endif
                % endif
            % elif index_title:
                <span>&raquo;</span>
                <span>${index_title}</span>
            % endif
          </div>

        </div><!-- level-left -->
        <div class="level-right">

          ## Theme Picker
          % if expose_theme_picker and request.has_perm('common.change_app_theme'):
              <div class="level-item">
                ${h.form(url('change_theme'), method="post")}
                ${h.csrf_token(request)}
                Theme:
                <div class="theme-picker">
                  <div class="select">
                    ${h.select('theme', theme, options=theme_picker_options, id='theme-picker')}
                  </div>
                </div>
                ${h.end_form()}
              </div>
          % endif

          ## Help Button
          % if help_url is not Undefined and help_url:
              <div class="level-item">
                ${h.link_to("Help", help_url, target='_blank', class_='button')}
              </div>
          % endif

          ## Feedback Button
          <div class="level-item">
            <button type="button" class="button is-primary" id="feedback">Feedback</button>
          </div>

        </div><!-- level-right -->
      </nav><!-- level -->
    </header>

    ## Page Title
    <section id="content-title" class="hero is-primary">
      <div class="container">
        % if capture(self.content_title):

            % if show_prev_next is not Undefined and show_prev_next:
                <div style="float: right;">
                  % if prev_url:
                      ${h.link_to("« Older", prev_url, class_='button autodisable')}
                  % else:
                      ${h.link_to("« Older", '#', class_='button', disabled='disabled')}
                  % endif
                  % if next_url:
                      ${h.link_to("Newer »", next_url, class_='button autodisable')}
                  % else:
                      ${h.link_to("Newer »", '#', class_='button', disabled='disabled')}
                  % endif
                </div>
            % endif

            <h1 class="title">${self.content_title()}</h1>
        % endif
      </div>
    </section>

    <div class="content-wrapper">

    ## Page Body
    <section id="page-body">

      % if request.session.peek_flash('error'):
          % for error in request.session.pop_flash('error'):
              <div class="notification is-warning">
                <!-- <button class="delete"></button> -->
                ${error}
              </div>
          % endfor
      % endif

      % if request.session.peek_flash():
          % for msg in request.session.pop_flash():
              <div class="notification is-info">
                <!-- <button class="delete"></button> -->
                ${msg}
              </div>
          % endfor
      % endif

      ${self.body()}
    </section>

    ## Feedback Dialog
    ${feedback_dialog()}

    ## Footer
    <footer class="footer">
      <div class="content">
        ${base_meta.footer()}
      </div>
    </footer>

    </div><!-- content-wrapper -->

  </body>
</html>

<%def name="title()"></%def>

<%def name="content_title()">
  ${self.title()}
</%def>

<%def name="header_core()">

  ${self.core_javascript()}
  ${self.extra_javascript()}
  ${self.core_styles()}
  ${self.extra_styles()}

  ## TODO: should this be elsewhere / more customizable?
  % if dform is not Undefined:
      <% resources = dform.get_widget_resources() %>
      % for path in resources['js']:
          ${h.javascript_link(request.static_url(path))}
      % endfor
      % for path in resources['css']:
          ${h.stylesheet_link(request.static_url(path))}
      % endfor
  % endif
</%def>

<%def name="core_javascript()">
  ${self.jquery()}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.loadmask.min.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.ui.timepicker.js'))}
  <script type="text/javascript">
    var session_timeout = ${request.get_session_timeout() or 'null'};
    var logout_url = '${request.route_url('logout')}';
    var noop_url = '${request.route_url('noop')}';
    % if expose_theme_picker and request.has_perm('common.change_app_theme'):
        $(function() {
            $('#theme-picker').change(function() {
                $(this).parents('form:first').submit();
            });
        });
    % endif
  </script>
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.feedback.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js') + '?ver={}'.format(tailbone.__version__))}
</%def>

<%def name="jquery()">
  ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
  ${h.javascript_link('https://code.jquery.com/ui/{}/jquery-ui.min.js'.format(request.rattail_config.get('tailbone', 'jquery_ui.version', default='1.11.4')))}
</%def>

<%def name="extra_javascript()"></%def>

<%def name="core_styles()">

  ${h.stylesheet_link('https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css')}

  ${self.jquery_theme()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.loadmask.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.timepicker.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.tailbone.css') + '?ver={}'.format(tailbone.__version__))}

  ${h.stylesheet_link(request.static_url('tailbone:static/themes/bobcat/css/base.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/bobcat/css/layout.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/filters.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/bobcat/css/forms.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/diffs.css') + '?ver={}'.format(tailbone.__version__))}
</%def>

<%def name="jquery_theme()">
  ${h.stylesheet_link('https://code.jquery.com/ui/1.11.4/themes/dark-hive/jquery-ui.css')}
</%def>

<%def name="extra_styles()"></%def>

<%def name="head_tags()"></%def>

<%def name="wtfield(form, name, **kwargs)">
  <div class="field-wrapper${' error' if form[name].errors else ''}">
    <label for="${name}">${form[name].label}</label>
    <div class="field">
      ${form[name](**kwargs)}
    </div>
  </div>
</%def>
