
/************************************************************
 *
 * tailbone.mobile.js
 *
 * Global logic for mobile app
 *
 ************************************************************/


$(function() {

    // must init header/footer toolbars since ours are "external"
    $('[data-role="header"], [data-role="footer"]').toolbar({theme: 'a'});
});


$(document).on('pagecontainerchange', function(event, ui) {

    // in some cases (i.e. when no user is logged in) we may want the (external)
    // header toolbar button to change between pages.  here's how we do that.
    // note however that we do this *always* even when not technically needed
    var link = $('[data-role="header"] a:first');
    var newlink = ui.toPage.find('.replacement-header a');
    link.text(newlink.text());
    link.attr('href', newlink.attr('href'));
    link.removeClass('ui-icon-home ui-icon-user');
    link.addClass(newlink.attr('class'));
});


$(document).on('click', '#feedback-button', function() {

    // prepare and display 'feedback' popup dialog
    var popup = $('.ui-page-active #feedback-popup');
    popup.find('.referrer .field').html(location.href);
    popup.find('.referrer input').val(location.href);
    popup.find('.user_name input').val('');
    popup.find('.message textarea').val('');
    popup.data('feedback-sent', false);
    popup.popup('open');
});


$(document).on('click', '#feedback-popup .submit', function() {

    // send message when 'feedback' submit button pressed
    var popup = $('.ui-page-active #feedback-popup');
    var form = popup.find('form');
    $.post(form.attr('action'), form.serializeArray(), function(data) {
        if (data.ok) {

            // mark "feedback sent" flag, for popupafterclose
            popup.data('feedback-sent', true);
            popup.popup('close');
        }
    });

});


$(document).on('click', '#feedback-form-buttons .cancel', function() {

    // close 'feedback' popup when user clicks Cancel
    var popup = $('.ui-page-active #feedback-popup');
    popup.popup('close');
});


$(document).on('popupafterclose', '#feedback-popup', function() {

    // thank the user for their feedback, after msg is sent
    if ($(this).data('feedback-sent')) {
        var popup = $('.ui-page-active #feedback-thanks');
        popup.popup('open');
    }
});


$(document).on('pagecreate', function() {

    // setup any autocomplete fields
    $('.field.autocomplete').mobileautocomplete();

});


// submit "quick row" form upon autocomplete selection
$(document).on('autocompleteitemselected', function(event, uuid) {
    var field = $(event.target);
    if (field.hasClass('quick-row')) {
        var form = field.parents('form:first');
        form.find('[name="quick_entry"]').val(uuid);
        form.submit();
    }
});


/**
 * Automatically set focus to certain fields, on various pages
 * TODO: should be letting the form declare a "focus spec" instead, to avoid
 * hard-coding these field names below!
 */
function setfocus() {
    var el = null;
    var queries = [
        '#username',
        '#new-purchasing-batch-vendor-text',
        '#new-receiving-batch-vendor-text',
    ];
    $.each(queries, function(i, query) {
        el = $(query);
        if (el.is(':visible')) {
            el.focus();
            return false;
        }
    });
}


$(document).on('pageshow', function() {

    setfocus();

    // if current page has form, which has declared a "focus spec", then try to
    // set focus accordingly
    var form = $('.ui-page-active form');
    if (form) {
        var spec = form.data('focus');
        if (spec) {
            var input = $(spec);
            if (input) {
                if (input.is(':visible')) {
                    input.focus();
                }
            }
        }
    }

});


// handle radio button value change for "simple" grid filter
$(document).on('change', '.simple-filter .ui-radio', function() {
    $(this).parents('form:first').submit();
});


// vendor validation for new purchasing batch
$(document).on('click', 'form[name="new-purchasing-batch"] input[type="submit"]', function() {
    var $form = $(this).parents('form');
    if (! $form.find('[name="vendor"]').val()) {
        alert("Please select a vendor");
        $form.find('[name="new-purchasing-batch-vendor-text"]').focus();
        return false;
    }
});


// disable datasync restart button when clicked
$(document).on('click', '#datasync-restart', function() {
    $(this).button('disable');
});


// TODO: this should go away in favor of quick_row approach
// handle global keypress on product batch "row" page, for sake of scanner wedge
var product_batch_routes = [
    'mobile.batch.inventory.view',
];
$(document).on('keypress', function(event) {
    var current_route = $('.ui-page-active [role="main"]').data('route');
    for (var route of product_batch_routes) {
        if (current_route == route) {
            var upc = $('.ui-page-active #upc-search');
            if (upc.length) {
                if (upc.is(':focus')) {
                    if (event.which == 13) {
                        if (upc.val()) {
                            $.mobile.navigate(upc.data('url') + '?upc=' + upc.val());
                        }
                    }
                } else {
                    if (event.which >= 48 && event.which <= 57) { // numeric (qwerty)
                        upc.val(upc.val() + event.key);
                        // TODO: these codes are correct for 'keydown' but apparently not 'keypress' ?
                        // } else if (event.which >= 96 && event.which <= 105) { // numeric (10-key)
                        //     upc.val(upc.val() + event.key);
                    } else if (event.which == 13) {
                        if (upc.val()) {
                            $.mobile.navigate(upc.data('url') + '?upc=' + upc.val());
                        }
                    }
                    return false;
                }
            }
        }
    }
});


// handle various keypress events for quick entry forms
$(document).on('keypress', function(event) {
    var quick_entry = $('.ui-page-active #quick_entry');
    if (quick_entry.length) {

        // if user hits enter with quick row input focused, submit form
        if (quick_entry.is(':focus')) {
            if (event.which == 13) { // ENTER
                if (quick_entry.val()) {
                    var form = quick_entry.parents('form:first');
                    form.submit();
                    return false;
                }
            }

        } else { // quick row input not focused

            // mimic keyboard wedge if we're so instructed
            if (quick_entry.data('wedge')) {

                if (event.which >= 48 && event.which <= 57) { // numeric (qwerty)
                    if (!event.altKey && !event.ctrlKey && !event.metaKey) {
                        quick_entry.val(quick_entry.val() + event.key);
                        return false;
                    }

                // TODO: these codes are correct for 'keydown' but apparently not 'keypress' ?
                // } else if (event.which >= 96 && event.which <= 105) { // numeric (10-key)
                //     upc.val(upc.val() + event.key);

                } else if (event.which == 13) { // ENTER
                    // submit form when ENTER is received via keyboard "wedge"
                    if (quick_entry.val()) {
                        var form = quick_entry.parents('form:first');
                        form.submit();
                        return false;
                    }
                }
            }
        }
    }
});


// when numeric keypad button is clicked, update quantity accordingly
$(document).on('click', '.quantity-keypad-thingy .keypad-button', function() {
    var keypad = $(this).parents('.quantity-keypad-thingy');
    var quantity = keypad.find('.keypad-quantity');
    var value = quantity.text();
    var key = $(this).text();
    var changed = keypad.data('changed');
    if (key == 'Del') {
        if (value.length == 1) {
            quantity.text('0');
        } else {
            quantity.text(value.substring(0, value.length - 1));
        }
        changed = true;
    } else if (key == '.') {
        if (value.indexOf('.') == -1) {
            if (changed) {
                quantity.text(value + '.');
            } else {
                quantity.text('0.');
                changed = true;
            }
        }
    } else {
        if (value == '0') {
            quantity.text(key);
            changed = true;
        } else if (changed) {
            quantity.text(value + key);
        } else {
            quantity.text(key);
            changed = true;
        }
    }
    if (changed) {
        keypad.data('changed', true);
    }
});


// show/hide expiration date per receiving mode selection
$(document).on('change', 'fieldset.receiving-mode input[name="mode"]', function() {
    var mode = $(this).val();
    if (mode == 'expired') {
        $('#expiration-row').show();
    } else {
        $('#expiration-row').hide();
    }
});


// handle inventory save button
$(document).on('click', '.inventory-actions button.save', function() {
    var form = $(this).parents('form:first');
    var uom = form.find('[name="keypad-uom"]:checked').val();
    var qty = form.find('.keypad-quantity').text();
    if (uom == 'CS') {
        form.find('input[name="cases"]').val(qty);
    } else { // units
        form.find('input[name="units"]').val(qty);
    }
    form.submit();
});
