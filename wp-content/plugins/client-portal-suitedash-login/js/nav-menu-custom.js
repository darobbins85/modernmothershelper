jQuery(document).ready( function($) {
    console.log( wpNavMenu );

    $('#submit-wp_suitedash_logindiv').bind('click', function(e) {
        var url = 'javascript:void(0);',
            label = $('#wp_suitedash_login-item-name').val();

        if ( '' === label ) {
            $('#wp_suitedash_logindiv').addClass('form-invalid');
            return false;
        }

        // Show the ajax spinner
        $( '.wp_suitedash_logindiv .spinner' ).addClass( 'is-active' );

        wpNavMenu.addItemToMenu({
            '-1': {
                'menu-item-type': 'custom',
                'menu-item-url': '#',
                'menu-item-title': label,
                'menu-item-classes': 'sdl_load_form'
            }
        }, wpNavMenu.addMenuItemToBottom, function() {
            // Remove the ajax spinner
            $( '.wp_suitedash_logindiv .spinner' ).removeClass( 'is-active' );
            // Set custom link form back to defaults
            $('#wp_suitedash_login-item-name').val('').blur();
        } );
    });

    $('#wp_suitedash_login input[type="text"]').keypress(function(e){
        $('#wp_suitedash_logindiv').removeClass('form-invalid');
        if ( e.keyCode === 13 ) {
            e.preventDefault();
            $( '#submit-wp_suitedash_logindiv' ).click();
        }
    });
});