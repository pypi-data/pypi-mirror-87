## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">Receiving &raquo; New Batch</%def>

<%def name="page_title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; New Batch</%def>

${h.form(form.action_url, class_='ui-filterable', name='new-receiving-batch')}
${h.csrf_token(request)}

% if phase == 1:

    % if vendor_use_autocomplete:
        <div class="field-wrapper vendor">
          <div class="field autocomplete" data-url="${url('vendors.autocomplete')}">
            ${h.hidden('vendor')}
            ${h.text('new-receiving-batch-vendor-text', placeholder="Vendor name", autocomplete='off', **{'data-type': 'search'})}
            <ul data-role="listview" data-inset="true" data-filter="true" data-input="#new-receiving-batch-vendor-text"></ul>
            <button type="button" style="display: none;">Change Vendor</button>
          </div>
        </div>
    % else:
        <div class="field-row">
          <label for="vendor">Vendor</label>
          <div class="field">
            ${h.select('vendor', None, vendor_options)}
          </div>
        </div>
    % endif

    <br />

    <div id="new-receiving-types" style="display: none;">

      ${h.hidden('workflow')}
      ${h.hidden('phase', value='1')}

      % if master.allow_from_po:
          <button type="button" class="start-receiving" data-workflow="from_po">Receive from PO</button>
      % endif

      % if master.allow_from_scratch:
          <button type="button" class="start-receiving" data-workflow="from_scratch">Receive from Scratch</button>
      % endif

      % if master.allow_truck_dump:
          <button type="button" class="start-receiving" data-workflow="truck_dump">Receive Truck Dump</button>
      % endif

    </div>

% else: ## phase 2

    ${h.hidden('workflow')}
    ${h.hidden('phase', value='2')}

    <div class="field-wrapper vendor">
      <label>Vendor</label>
      <div class="field">
        ${h.hidden('vendor', value=vendor.uuid)}
        ${vendor}
      </div>
    </div>

    % if purchases:
        ${h.hidden(purchase_order_fieldname, class_='purchase-order-field')}
        <p>Please choose a Purchase Order to receive:</p>
        <ul data-role="listview" data-inset="true">
          % for key, purchase in purchases:
              <li data-key="${key}">${h.link_to(purchase, '#')}</li>
          % endfor
        </ul>
    % else:
        <p>(no eligible purchases found)</p>
    % endif

    % if master.allow_from_scratch:
        <button type="button" class="start-receiving" data-workflow="from_scratch">Receive from Scratch</button>
    % endif

    ${h.link_to("Cancel", url('mobile.{}'.format(route_prefix)), class_='ui-btn ui-corner-all')}

% endif

${h.end_form()}
