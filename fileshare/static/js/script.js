jQuery(function ($) {
    $('.btn-shared').hover(function () {
        $(this).find('.dropdown-shared').first().stop(true, true).delay(100).slideDown();
    }, function () {
        $(this).find('.dropdown-shared').first().stop(true, true).delay(300).slideUp();
    });
});

$(function() {
  $('tr.parent td button.admin-btn')
    .on("click", function(){
    var idOfParent = $(this).parents('tr').attr('id');
    $('tr.child-'+idOfParent).toggle('fast');
  });
  $('tr[class^=child-]').hide().children('td');
});


$(document).on('click', '.confirm-delete', function () {
  $("#confirmDeleteModal").attr('caller-id', $(this).attr('id'));
  console.log()
});

$(document).on('click', '#confirmDeleteButtonModal', function () {
  var caller = $("#confirmDeleteButtonModal").closest(".modal").attr('caller-id');
  window.location = $("#".concat(caller)).attr('href');
});


(function ($) {

    "use strict";


})(jQuery);
