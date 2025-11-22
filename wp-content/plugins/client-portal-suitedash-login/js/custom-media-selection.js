jQuery(document).ready( function($) {

    jQuery('input#media_manager').click(function(e) {

        e.preventDefault();
        var image_frame;
        if(image_frame){
            image_frame.open();
        }
        // Define image_frame as wp.media object
        image_frame = wp.media({
            title: 'Select Media',
            multiple : false,
            library : {
                type : 'image',
            }
        });

        image_frame.on('close',function() {
            // On close, get selections and save to the hidden input
            // plus other AJAX stuff to refresh the image preview
            var selection =  image_frame.state().get('selection');
            var id = 0;
            selection.each(function(attachment) {
                id = attachment['id'];
            });

            jQuery('input#logo_id').val(id);

            if (selection.models && selection.models[0]) {
                jQuery('#preview-logo').show();
                jQuery('#preview-logo').attr('src', selection.models[0].attributes.url);
            } else {
                jQuery('#preview-logo').hide();
            }
        });

        image_frame.on('open',function() {
            // On open, get the id from the hidden input
            // and select the appropiate images in the media manager
            var selection =  image_frame.state().get('selection');
            var id = jQuery('input#logo_id').val();
            var attachment = wp.media.attachment(id);
            attachment.fetch();
            selection.add( attachment ? [ attachment ] : [] );

        });

        image_frame.open();
    });

});