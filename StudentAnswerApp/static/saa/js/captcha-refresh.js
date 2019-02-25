/**
 * Created by ww on 2018/2/21.
 */

$('.captcha').click(function () {
    $form = $(this).parents('form');
    $.getJSON($(this).data('url'), {}, function (json) {
        // this should update your captcha image src and captcha hidden input
    });
    return false;
});
