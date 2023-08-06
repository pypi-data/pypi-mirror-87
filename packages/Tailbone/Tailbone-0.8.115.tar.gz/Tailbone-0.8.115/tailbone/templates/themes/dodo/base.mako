## -*- coding: utf-8; -*-
## largely copied from https://github.com/dansup/bulma-templates/blob/master/templates/admin.html
## <%namespace file="/feedback_dialog.mako" import="feedback_dialog" />
<%namespace name="base_meta" file="/base_meta.mako" />
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  ## <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${base_meta.global_title()} &raquo; ${capture(self.title)|n}</title>

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,700" rel="stylesheet">
  <!-- Bulma Version 0.7.4-->
  <link rel="stylesheet" href="https://unpkg.com/bulma@0.7.4/css/bulma.min.css" />
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/dodo/css/admin.css') + '?ver={}'.format(tailbone.__version__))}

  ${h.stylesheet_link(request.static_url('tailbone:static/themes/dodo/css/base.css') + '?ver={}'.format(tailbone.__version__))}

  % if background_color:
      <style type="text/css">
        html, body {
            background-color: ${background_color};
        }
      </style>
  % endif

  % if not request.rattail_config.production():
      <style type="text/css">
        html, body, body > .navbar {
          background-image: url(${request.static_url('tailbone:static/img/testing.png')});
        }
      </style>
  % endif

  ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
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


</head>

<body>

    <!-- START NAV -->
    <nav class="navbar is-white">
        <div class="container">
            <div class="navbar-brand">
                <a class="navbar-item brand-text" href="${url('home')}">
                  ${base_meta.header_logo()}
                  ${base_meta.global_title()}
                </a>

                <div class="navbar-burger burger" data-target="navMenu">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div id="navMenu" class="navbar-menu">
                <div class="navbar-start">

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

                </div><!-- navbar-start -->

                <div class="navbar-end">

                  ## Theme Picker
                  % if expose_theme_picker and request.has_perm('common.change_app_theme'):
                      <div class="level-item">
                        ${h.form(url('change_theme'), method="post")}
                        ${h.csrf_token(request)}
                        <div class="columns is-vcentered">
                          <div class="column">
                            Theme:
                          </div>
                          <div class="column theme-picker">
                            <div class="select">
                              ${h.select('theme', theme, options=theme_picker_options, id='theme-picker')}
                            </div>
                          </div>
                        </div>
                        ${h.end_form()}
                      </div>
                  % endif
                  
                </div><!-- navbar-end -->

            </div><!-- navbar-menu -->
        </div>
    </nav>
    <!-- END NAV -->
    <div class="container">
        <div class="columns">
            <div class="column is-3 ">
                <aside class="menu is-hidden-mobile">

                  % for topitem in menus:
                      % if topitem.is_link:
                          ${h.link_to(topitem.title, topitem.url, target=topitem.target, class_='navbar-item')}
                      % else:
                          <p class="menu-label">${topitem.title}</p>
                          <ul class="menu-list">
                            % for subitem in topitem.items:
                                % if not subitem.is_sep:
                                    <li>${h.link_to(subitem.title, subitem.url, target=subitem.target)}</li>
                                % endif
                            % endfor
                          </ul>
                      % endif
                  % endfor

                </aside>
            </div>
            <div class="column is-9">
                <nav class="breadcrumb" aria-label="breadcrumbs">
                    <ul>

                      ## Current Context
                      % if master:
                          % if master.listing:
                              <li>${index_title}</li>
                          % else:
                              <li>${h.link_to(index_title, index_url)}</li>
                              % if parent_url is not Undefined:
                                  <li>${h.link_to(parent_title, parent_url)}</li>
                              % elif instance_url is not Undefined:
                                  <li>${h.link_to(instance_title, instance_url)}</li>
                              % endif
##                                 % if master.viewing and grid_index:
##                                     ${grid_index_nav()}
##                                 % endif
                          % endif
                      % elif index_title:
                          <li>${index_title}</li>
                      % endif

                      % if capture(self.content_title):

##                           % if show_prev_next is not Undefined and show_prev_next:
##                               <div style="float: right;">
##                                 % if prev_url:
##                                     ${h.link_to("« Older", prev_url, class_='button autodisable')}
##                                 % else:
##                                     ${h.link_to("« Older", '#', class_='button', disabled='disabled')}
##                                 % endif
##                                 % if next_url:
##                                     ${h.link_to("Newer »", next_url, class_='button autodisable')}
##                                 % else:
##                                     ${h.link_to("Newer »", '#', class_='button', disabled='disabled')}
##                                 % endif
##                               </div>
##                           % endif

                          <li class="is-active"><a href="#" aria-current="page">${self.content_title()}</a></li>
                      % endif

                    </ul>
                </nav>
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

            </div>
        </div>
    </div>
    ${h.javascript_link(request.static_url('tailbone:static/themes/dodo/js/bulma.js'), async='true')}
</body>

</html>

<%def name="title()"></%def>

<%def name="content_title()">
  ${self.title()}
</%def>
