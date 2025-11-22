function giftup_set_code(code) {
    var actionElement = document.querySelector('giftup-cart-subtotal-td-form');
    var action = actionElement ? actionElement.dataset.action : "";
    
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", action);

    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "giftup_gift_card_code");
    input.setAttribute("value", code);

    form.appendChild(input);

    document.body.appendChild(form);
    form.submit();
}

function giftup_code_entry_input(e) {
    var elem = null;

    // Try to locate the code entry input by searching locally to the e.target element
    if (e && e.target && e.target.closest) {
        var container = e.target.closest(".giftup-cart-subtotal-td-form");

        if (container) {
            elem = container.querySelector(".giftup-cart-subtotal-td-form-input")
        }
    }

    // If that fails, try to locate the code entry input from the one (possibly duplicated) inputs that has a value...
    if (!elem) {
        var elements = document.querySelectorAll(".giftup-cart-subtotal-td-form-input");

        if (elements.length == 1) {
            elem = elements[0];
        } else {
            elem = Array.from(elements).find(function(element) { return !!element.value; });
        }
    }

    // If that fails, just look it up by id
    if (!elem) {
        elem = document.getElementById('giftup-giftcard-code');
    }

    // If that fails, just look it up by class name
    if (!elem) {
        var elems = document.getElementsByClassName('giftup-cart-subtotal-td-form-input');

        if (elems) {
            elem = elems[0];
        }
    }

    return elem;
}

function giftup_submit_code(e) {
    var elem = giftup_code_entry_input(e);

    if (elem) {
        giftup_set_code(elem.value);
    }
}

function giftup_code_keypress(e) {
    var characterCode;

    if (e && e.which) {
        characterCode = e.which;
    }
    else {
        characterCode = event.keyCode;
    }

    if (characterCode == 13) {
        giftup_submit_code(e);
        e.preventDefault();
        return false;
    } else {
        return true;
    }
}

function giftup_hide_apply_gift_card(e) {
    document.querySelectorAll('.giftup-cart-subtotal-td-apply-gc').forEach(elem => { elem.style.display='none'; });
    document.querySelectorAll('.giftup-cart-subtotal-td-form').forEach(elem => { elem.style.display='grid'; });
    document.querySelectorAll('.giftup-cart-subtotal-td-form br').forEach(elem => { elem.style.display='none'; });
    document.querySelectorAll('.giftup-cart-subtotal-td p').forEach(elem => { elem.style.display='none'; });
    
    var input = giftup_code_entry_input();

    if (input) {
        input.focus();
    }

    //e.preventDefault();

    return false;
}