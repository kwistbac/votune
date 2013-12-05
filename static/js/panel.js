$(function () {
    $(document).on('submit', ".modal form", function (e) {
        e.preventDefault();

        var form = $(this);
        var modal = form.closest('.modal');

        form.append('<input type="hidden" name="ok" value="1">');
        var values = (form.attr('method') && form.attr('method').toUpperCase() == 'POST' ? form.serializeArray() : form.serialize());

        modal.load(form.attr('action'), values, function (data, textStatus, xhr) {
            if (!data)
                modal.modal('hide');
            else
                $(this).trigger('loaded.bs.modal');
        });
    })
        .on('click', "#library", function (e) {
            e.preventDefault();

            var modal = $('<div>').attr('id', 'libraryModal')
                .addClass('modal')
                .addClass('fade');

            modal.on('hidden.bs.modal', function () {
                $(this).remove();
            })
                .modal()
                .load($(this).attr('href'), function () {
                    $(this).trigger('loaded.bs.modal');
                });

        })
        .on('click', "#libraryAdd", function (e) {
            e.preventDefault();

            var modal = $('<div>').attr('id', 'libraryAddModal')
                .addClass('modal')
                .addClass('fade');

            modal.on('hidden.bs.modal', function () {
                $('#libraryModal').load('/establishment/library/', function () {
                    $(this).trigger('loaded.bs.modal');
                });
                $.post('/establishment/library/upload/clean');
                $(this).remove();
            })
                .on('loaded.bs.modal', function () {
                    var el = modal.find('#uploader');
                    if (el.length) {
                        var uploader = new qq.FineUploader(
                            {
                                element: el.get(0),
                                multiple: true,
                                validation: { allowedExtensions: ['mp3'] },
                                request: { endpoint: '/establishment/library/upload' },
                                retry: { enableAuto: true },
                                chunking: { enabled: true },
                                deleteFile: { endpoint: '/establishment/library/upload', enabled: true, forceConfirm: true },
                                callbacks: { onError: function (id, name, reason) {
                                    alert(reason);
                                } }
                            });
                    }
                })
                .on('click', '#libraryAddSave', function () {
                    modal.find('form:first').submit();
                })
                .modal()
                .load($(this).attr('href'), function () {
                    $(this).trigger('loaded.bs.modal');
                });

        })
        .on('click', "#libraryEdit", function (e) {
            e.preventDefault();

            var modal = $('<div>').attr('id', 'libraryEditModal')
                .addClass('modal')
                .addClass('fade');

            modal.on('hidden.bs.modal', function () {
                $('#libraryModal').load('/establishment/library/', function () {
                    $(this).trigger('loaded.bs.modal');
                });
                $(this).remove();
            })
                .on('click', '#libraryEditSave', function () {
                    modal.find('form:first').submit();
                })
                .modal()
                .load($(this).attr('href'), function () {
                    $(this).trigger('loaded.bs.modal');
                });

        })
        .on('click', "#libraryRemove", function (e) {
            e.preventDefault();

            var modal = $('<div>').attr('id', 'libraryRemoveModal')
                .addClass('modal')
                .addClass('fade');

            modal.on('hidden.bs.modal', function () {
                $('#libraryModal').load('/establishment/library/', function () {
                    $(this).trigger('loaded.bs.modal');
                });
                $(this).remove();
            })
                .on('click', '#libraryRemoveConfirm', function () {
                    modal.find('form:first').submit();
                })
                .modal()
                .load($(this).attr('href'), function () {
                    $(this).trigger('loaded.bs.modal');
                });

        });


});

$(document).ready(function () {
    $(document).on('click', "#manage_qr", function (e) {
        e.preventDefault();
        var modal = $('<div>').attr('id', 'manageQR')
            .addClass('modal')
            .addClass('fade');

        modal.on('hidden.bs.modal', function () {
            $(this).remove();
        })
            .modal()
            .load($(this).attr('href'), function () {
                $(this).trigger('loaded.bs.modal');
            });

    });
});