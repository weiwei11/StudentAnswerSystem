/**
 * Created by ww on 2018/3/20.
 */

$(document).ready(
    function () {
        $('#sidebar-trigger').click(
            function () {
                var sidebar_menu = $('#sidebar');
                sidebar_menu.toggle();
            }
        );
    }
);