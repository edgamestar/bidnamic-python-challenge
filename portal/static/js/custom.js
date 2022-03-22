function activate_ajax_form() {
    $('.ajax-form').each(function () {
        $(this).validate({
            ignore: '.ignore, .select2-input',
            focusInvalid: false,

            errorPlacement: function (error, element) {
                error.addClass("ui red pointing label transition");
                error.insertAfter(element.parent());
            },
            highlight: function (element, errorClass, validClass) {
                $(element).parents(".field").addClass(errorClass);
            },
            unhighlight: function (element, errorClass, validClass) {
                $(element).parents(".field").removeClass(errorClass);
            },

            submitHandler: function (form) {
                $(form).submit(function (e) {
                    e.preventDefault();
                });
                try {
                    $(form).find('.ui.button.submit').toggleClass('loading');
                } catch (e) {
                }

                let data = new FormData($(form)[0]);
                data.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());

                call_api($(form).attr('method'), $(form).attr('action'), {}, data, form);

            }
        });
    });
}

$.validator.addMethod('filesize', function (value, element, param) {
    return this.optional(element) || (element.files[0].size <= param)
}, 'File size must be less than or equal to {0} MB');

$('.ui.dropdown').dropdown({
    clearable: false,
    forceSelection: true,
});

$('.ui.button.submit:not(.form-submit)').each(function () {
    $(this).on('click', function () {
        $(this).closest('form').submit();
    })
});

function call_api(method, url, headers, data, form) {
    $.ajax({
        type: method,
        url: url,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (success) {
            if (!success.hasOwnProperty('no-reset')) {
                $(form)[0].reset();
            }

            if (success.hasOwnProperty('details')) {
                notify('success', success.details);
            }

            try {
                $(form).find('.ui.button.submit').toggleClass('loading');
            } catch (e) {
            }

            if (success.hasOwnProperty('results')) {
                $('.results-holder').html(success.results);
                let results_table = $('#results_table').DataTable({
                    buttons: [
                        'copy', 'print', 'csv', 'pdf', 'excel'
                    ],
                    order: [[3, 'desc']],
                    lengthMenu: [[25, 50, 100, -1], [25, 50, 100, "All"]],
                });
                results_table.buttons().container().appendTo($('div.eight.column:eq(0)', results_table.table().container()));
            }

            if (success.hasOwnProperty('redirect')) {
                setTimeout(function () {
                    navigate(success.redirect);
                }, 2500);
            }
        },
        error: function (error) {
            let content = "";
            if (error.status === 500) {
                content = 'Something went wrong. Reload and try again. 😊'
            } else if (error.status === 400) {
                if (error.responseJSON.hasOwnProperty('redirect')) {
                    navigate(error.responseJSON.redirect);
                } else if (error.responseJSON.hasOwnProperty('details')) {
                    content = error.responseJSON.details;
                }
            }
            notify('error', content);
            try {
                $(form).find('.ui.button.submit').toggleClass('loading');
            } catch (e) {
            }
        }
    });
}

function notify(type, content) {
    let types = {
        "success": {
            icon: "fa fa-check-circle",
            timeout: 2500
        },
        "error": {
            icon: "fa fa-ban",
            timeout: false
        },
        "info": {
            icon: "fa fa-info",
            timeout: false
        },
    };
    new Noty({
        type: type,
        text: '<div style="text-align: center">' + content + '</div>',
        // text: content,
        layout: 'bottomCenter',
        theme: 'semanticui',
        animation: {
            open: 'animated bounceInUp',
            close: 'animated bounceOutDown'
        },
        timeout: types[type].timeout
    }).show()
}

function navigate(url) {
    window.location.href = url;
}

function scroll_to_bottom(element) {
    element.animate({scrollTop: element.prop("scrollHeight")}, 50);
}

activate_ajax_form();