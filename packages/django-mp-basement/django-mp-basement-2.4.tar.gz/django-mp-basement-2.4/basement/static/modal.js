
Modal = function (params) {

    var $target = params.$target,
        onSuccess = params.onSuccess,
        focusOn = params.focusOn,
        url = $target.data('url');

    $target.click(function () {

        $.get(url, function (response) {

            var $modal = $(response).modal();

            function toggleSubmitBtn(isActive) {
                $modal.find('[data-role=submit-btn]').prop('disabled', !isActive);
            }

            function handleFormSubmit(event) {

                event.preventDefault();

                toggleSubmitBtn(false);

                $(this).ajaxSubmit({
                    method: 'POST',
                    url: url,
                    success: handleFormSubmitSuccess,
                    error: handleFormSubmitError,
                    complete: function () {
                        toggleSubmitBtn(true);
                    }
                });

            }

            function handleSubmitBtnClick() {
                $modal.find('form').submit();
            }

            function removeModal() {
                $modal.remove();
            }

            function handleFormSubmitSuccess(response) {

                $modal.modal('hide');

                if ($.notify && response.message) {
                    $.notify({message: response.message}, {type: 'success'});
                }

                if (response.url) {
                    window.location = response.url
                }

                if (onSuccess) {
                    onSuccess(response);
                }
            }

            function handleFormSubmitError(response) {
                $modal.find('form').replaceWith(response.responseText);
            }

            if (focusOn) {
                $modal.find(focusOn).focus();
            }

            $modal.on('submit', 'form', handleFormSubmit);

            $modal.on('click', '[data-role=submit-btn]', handleSubmitBtnClick);

            $modal.on('hidden.bs.modal', removeModal);

        });

    });

};
