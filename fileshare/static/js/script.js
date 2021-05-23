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


document.getElementById('dlt-button').addEventListener('click', function () {
    document.querySelector('.dlt-modal').style.display = 'flex';
});

document.querySelector('.dlt-close').addEventListener('click', function () {
    document.querySelector('.dlt-modal').style.display = 'none'
})


(function ($) {

    "use strict";


})(jQuery);
