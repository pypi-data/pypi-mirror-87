## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view_row.mako" />
<%namespace file="/mobile/keypad.mako" import="keypad" />

<%def name="title()">Receiving &raquo; ${batch.id_str} &raquo; ${master.render_product_key_value(row)}</%def>

<%def name="page_title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; ${h.link_to(batch.id_str, url('mobile.receiving.view', uuid=batch.uuid))} &raquo; ${master.render_product_key_value(row)}</%def>


<div${' class="ui-grid-a"' if product_image_url else ''|n}>
  <div class="ui-block-a"${'' if instance.product else ' style="background-color: red;"'|n}>
    % if instance.product:
        <h3>${instance.brand_name or ""}</h3>
        <h3>${instance.description} ${instance.size or ''}</h3>
        % if allow_cases:
            <h3>1 CS = ${h.pretty_quantity(row.case_quantity or 1)} ${unit_uom}</h3>
        % endif
    % else:
        <h3>${instance.description}</h3>
    % endif
  </div>
  % if product_image_url:
    <div class="ui-block-b">
      ${h.image(product_image_url, "product image")}
    </div>
  % endif
</div>

<table${'' if instance.product else ' style="background-color: red;"'|n}>
  <tbody>
    % if batch.order_quantities_known:
        <tr>
          <td>ordered</td>
          <td>
            % if allow_cases:
                ${h.pretty_quantity(row.cases_ordered or 0)} /
            % endif
            ${h.pretty_quantity(row.units_ordered or 0)}
          </td>
        </tr>
    % endif
    <tr>
      <td>received</td>
      <td>
        % if allow_cases:
            ${h.pretty_quantity(row.cases_received or 0)} /
        % endif
        ${h.pretty_quantity(row.units_received or 0)}
      </td>
    </tr>
    <tr>
      <td>damaged</td>
      <td>
        % if allow_cases:
            ${h.pretty_quantity(row.cases_damaged or 0)} /
        % endif
        ${h.pretty_quantity(row.units_damaged or 0)}
      </td>
    </tr>
    % if allow_expired:
        <tr>
          <td>expired</td>
          <td>
            % if allow_cases:
                ${h.pretty_quantity(row.cases_expired or 0)} /
            % endif
            ${h.pretty_quantity(row.units_expired or 0)}
          </td>
        </tr>
    % endif
  </tbody>
</table>

% if request.session.peek_flash('receiving-warning'):
    % for error in request.session.pop_flash('receiving-warning'):
        <div class="receiving-warning">${error}</div>
    % endfor
% endif

% if not batch.executed and not batch.complete:

    ${h.form(request.current_route_url(), class_='receiving-update')}
    ${h.csrf_token(request)}
    ${h.hidden('row', value=row.uuid)}
    ${h.hidden('cases')}
    ${h.hidden('units')}

    ## only show quick-receive if we have an identifiable product
    % if quick_receive and instance.product:
        % if quick_receive_all:
            <button type="button" class="quick-receive" data-quantity="${quick_receive_quantity}" data-uom="${quick_receive_uom}">${quick_receive_text}</button>
        % elif allow_cases:
            <button type="button" class="quick-receive" data-quantity="1" data-uom="CS">Receive 1 CS</button>
            <div>
              ## TODO: probably should make these optional / configurable
              <button type="button" class="quick-receive ui-btn ui-btn-inline ui-corner-all" data-quantity="1" data-uom="EA">1 EA</button>
              <button type="button" class="quick-receive ui-btn ui-btn-inline ui-corner-all" data-quantity="3" data-uom="EA">3 EA</button>
              <button type="button" class="quick-receive ui-btn ui-btn-inline ui-corner-all" data-quantity="6" data-uom="EA">6 EA</button>
            </div>
            <br />
        % else:
            <button type="button" class="quick-receive" data-quantity="1" data-uom="${unit_uom}">Receive 1 ${unit_uom}</button>
        % endif
    % endif

    ${keypad(unit_uom, uom, allow_cases=allow_cases)}

    <table>
      <tbody>
        <tr>
          <td>
            <fieldset data-role="controlgroup" data-type="horizontal" class="receiving-mode">
              ${h.radio('mode', value='received', label="received", checked=True)}
              ${h.radio('mode', value='damaged', label="damaged")}
              % if allow_expired:
                  ${h.radio('mode', value='expired', label="expired")}
              % endif
            </fieldset>
          </td>
        </tr>
        <tr id="expiration-row" style="display: none;">
          <td>
            <div style="padding:10px 20px;">
              <label for="expiration_date">Expiration Date</label>
              <input name="expiration_date" type="date" value="" placeholder="YYYY-MM-DD" />
            </div>
          </td>
        </tr>
        <tr>
          <td>
            <fieldset data-role="controlgroup" data-type="horizontal" class="receiving-actions">
              <button type="button" data-action="add" class="ui-btn-inline ui-corner-all">Add</button>
              <button type="button" data-action="subtract" class="ui-btn-inline ui-corner-all">Subtract</button>
              ## <button type="button" data-action="clear" class="ui-btn-inline ui-corner-all ui-state-disabled">Clear</button>
            </fieldset>
          </td>
        </tr>
      </tbody>
    </table>

    ${h.hidden('quick_receive', value='false')}
    ${h.end_form()}

    % if master.mobile_rows_deletable and master.row_deletable(row) and request.has_perm('{}.delete_row'.format(permission_prefix)):
        ${h.form(url('mobile.{}.delete_row'.format(route_prefix), uuid=batch.uuid, row_uuid=row.uuid), class_='receiving-update')}
        ${h.csrf_token(request)}
        ${h.submit('submit', "Delete this Row")}
        ${h.end_form()}
    % endif

% endif
