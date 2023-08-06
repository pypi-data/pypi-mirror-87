
/************************************************************
 *
 * tailbone.mobile.receiving.js
 *
 * Global logic for mobile receiving feature
 *
 ************************************************************/


// toggle visibility of "Receive" type buttons based on whether vendor is set
$(document).on('autocompleteitemselected', 'form[name="new-receiving-batch"] .vendor', function(event, uuid) {
    $('#new-receiving-types').show();
});
$(document).on('autocompleteitemcleared', 'form[name="new-receiving-batch"] .vendor', function(event) {
    $('#new-receiving-types').hide();
});
$(document).on('change', 'form[name="new-receiving-batch"] select[name="vendor"]', function(event) {
    if ($(this).val()) {
        $('#new-receiving-types').show();
    } else {
        $('#new-receiving-types').hide();
    }
});


// submit new receiving batch form when user clicks "Receive" type button
$(document).on('click', 'form[name="new-receiving-batch"] .start-receiving', function() {
    var form = $(this).parents('form');
    form.find('input[name="workflow"]').val($(this).data('workflow'));
    form.submit();
});


// submit new receiving batch form when user clicks Purchase Order option
$(document).on('click', 'form[name="new-receiving-batch"] [data-role="listview"] a', function() {
    var form = $(this).parents('form');
    var key = $(this).parents('li').data('key');
    form.find('[name="workflow"]').val('from_po');
    form.find('.purchase-order-field').val(key);
    form.submit();
    return false;
});


// handle receiving action buttons
$(document).on('click', 'form.receiving-update .receiving-actions button', function() {
    var action = $(this).data('action');
    var form = $(this).parents('form:first');
    var uom = form.find('[name="keypad-uom"]:checked').val();
    var mode = form.find('[name="mode"]:checked').val();
    var qty = form.find('.keypad-quantity').text();
    if (action == 'add' || action == 'subtract') {
        if (qty != '0') {
            if (action == 'subtract') {
                qty = '-' + qty;
            }

            if (uom == 'CS') {
                form.find('[name="cases"]').val(qty);
            } else { // units
                form.find('[name="units"]').val(qty);
            }

            if (action == 'add' && mode == 'expired') {
                var expiry = form.find('input[name="expiration_date"]');
                if (! /^\d{4}-\d{2}-\d{2}$/.test(expiry.val())) {
                    alert("Please enter a valid expiration date.");
                    expiry.focus();
                    return;
                }
            }

            form.submit();
        }
    }
});


// quick-receive (1 case or unit)
$(document).on('click', 'form.receiving-update .quick-receive', function() {
    var form = $(this).parents('form:first');
    form.find('[name="mode"]').val('received');
    var quantity = $(this).data('quantity');
    if ($(this).data('uom') == 'CS') {
        form.find('[name="cases"]').val(quantity);
    } else {
        form.find('[name="units"]').val(quantity);
    }
    form.find('input[name="quick_receive"]').val('true');
    form.submit();
});
