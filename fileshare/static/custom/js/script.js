// Modal Delete confirm handler
$(document).ready(function () {
    $('.mdel-modal').click(function () {
        var fileUrl = $(this).attr('url');
        var fileData = $(this).attr('id');
        console.log(fileData, fileUrl)
        $.ajax({
            url: fileUrl,
            data: {fileData: fileData},
            success: function (data) {
                $('#file_delete').html(data)
                $('#deletemodal').modal('show');
            }
        });
    });
});


//Modal Update file handler
$(document).ready(function () {
    $('.mu-modal').click(function () {
        var fileUrl = $(this).attr('url');
        var fileData = $(this).attr('id');
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: fileUrl,
            method: 'GET',
            headers: {'X-CSRFToken': csrftoken},
            data: {fileData: fileData},
            success: function (data) {
                $('#file_update').html(data);
                $('#updatemodal').modal('show');
            }
        });
    });
});


//Modal Upload file handler
$(document).ready(function () {
    $('.mf-modal').click(function () {
        var fileUrl = $(this).attr('url');
        var fileData = $(this).attr('id');
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: fileUrl,
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {fileData: fileData},
            success: function (data) {
                $('#file_upload').html(data);
                $('#uploadmodal').modal('show');
            },
        });
    });
});


//Modal Detail file handler
$(document).ready(function () {
    $('.md-modal').click(function () {
        var fileData = $(this).attr('id');
        var fileUrl = $(this).attr('url');
        $.ajax({
            url: fileUrl,
            method: 'GET',
            data: {fileData: fileData},
            success: function (data) {
                $('#file_detail').html(data);
                $('#detailmodal').modal('show')
            }
        });
    });
});


//Modal Multi-selected file Delete confirm handler
$('#multi-delete').on('shown.bs.modal', function (e) {
    var checkedValues = $('.file-check:checked').map(function () {
        return $(this).val();
    }).get();

    $('p, .multi-delete-text').html('Are you sure you want to delete <strong>' +
        checkedValues.length +
        '</strong> file' +
        (checkedValues.length === 1 ? '' : 's') + '?')

    $('#hidden_checkedinput').val(checkedValues.join());
});

$(".file-all-check").on('change', function () {
    $(".file-check").prop('checked', $(this).is(":checked"));
});


$(function () {
    $(".file-all-check").change(function () {
        var len = $(".file-all-check:checked").length;
        if (len == 0)
            $(".multi-delete-button").prop("disabled", true);
        else
            $(".multi-delete-button").removeAttr("disabled");
    });
    $(".file-all-check").trigger('change');


    $(".file-check").change(function () {
        var len = $(".file-check:checked").length;
        if (len == 0)
            $(".multi-delete-button").prop("disabled", true);
        else
            $(".multi-delete-button").removeAttr("disabled");
    });
    $(".file-check").trigger('change');
});


//Table collapse handler on user and admin page
$(function () {

    var active = true;

    $('#collapse-init').click(function () {
        if (active) {
            active = false;
            $('.multi-collapse').collapse('show');
            $('.panel-title').attr('data-bs-toggle', '');
            $(this).html('<div class="faa-parent animated-hover">' +
                '<i class="fas fa-angle-double-up faa-bounce faa-fast"></i> Close' +
                '</div>');
        } else {
            active = true;
            $('.multi-collapse').collapse('hide');
            $('.panel-title').attr('data-bs-toggle', 'collapse');
            $(this).html('<div class="faa-parent animated-hover">' +
                '<i class="fas fa-angle-double-down faa-bounce faa-reverse faa-fast"></i> Expand' +
                '</div>');
        }
    });

    $('#accordion').on('show.bs.collapse', function () {
        if (active) $('#accordion .in').collapse('hide');
        console.log('accordion working')
    });

});
