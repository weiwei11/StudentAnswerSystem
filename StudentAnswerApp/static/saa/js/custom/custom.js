/**
 * Created by ww on 2018/3/21.
 */

String.prototype.format = function (args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if (args[key] != undefined) {
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    var reg = new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
};

function custom_notification_list_callback(data) {
    var notifications = $(".notification > li");
    notifications.remove(".notification-item");
    for (var i = 0; i < data.unread_list.length; i++) {
        var msg = data.unread_list[i];
        var text = '<li class="notification-item">\
                        <a href="#"><span class="label label-{0}">\
                            <i class="fa fa-bolt"></i></span>\
                            {1} {2} {3} --> {4}.\
                            <span class="pull-right small italic">{5}</span>\
                        </a>\
                    </li>'.format(msg.level, msg.actor, msg.verb, msg.action, msg.target, msg.timestamp);
        notifications.last().before(text);
        // console.log(msg);
    }
}


$(document).ready(function ($) {

    var scroll_top = null;
    var opacity = null;
    $(window).scroll(function () {
        scroll_top = $(window).scrollTop();
        console.log(scroll_top);
        if (scroll_top <= 100) {
            $("#nav").css({"opacity": 1 - scroll_top / 200})
        } else {
            $("nav").css({"opacity": 0.5})
        }
    });


    $("#comment_form").submit(function () {

        if ($("#id_honeypot").val().length != 0) {
            alert("Stop! comment spam!");
            return false;
        }

        var id_comment = $("#id_comment");
        if (id_comment.val().length == 0) {
            alert("Error: please write your comment!");
            id_comment.focus();
            return false;
        }
        return true;
    });

    $(".emojione-area").emojioneArea({
        search: false,
        filtersPosition: "bottom"
    });

    $(".emoji-used").each(function () {
        var value = $(this).text();
        var code = $('<div/>').text(value).html(); //html转义

        console.log("emoji-used");

        $(this).html(emojione.toImage(code));
    });


    $("select[multiple=multiple]").addClass("multiselect");
    $(".multiselect").multiselect({
        buttonWidth: "100%",
        maxHeight: 200,
        buttonClass: "btn btn-white",
        includeSelectAllOption: true,
        enableFiltering: true,
        templates: {
            filterClearBtn: '<span class="input-group-btn"><button class="btn multiselect-clear-filter" type="button"><i class="glyphicon glyphicon-remove-circle"></i></button></span>',
        }
    });
});