
DeleteAction = function (params) {

    var $container = params.$container,
        selector = params.selector,
        onDelete = params.onDelete;

    function handleDeleteClick() {
        var $btn = $(this);

        $btn.prop('disabled', true);

        $.post(
            $btn.data('url'),
            function (response) {
                onDelete($btn.data('item-id'), response);

                $.notify({
                    message: response.message
                }, {
                    type: 'success'
                });
            }
        ).error(function (response) {
            $.notify({
                message: response.responseText
            }, {
                type: 'danger'
            });
        });
    }

    $container.on('click', selector, handleDeleteClick);

};
