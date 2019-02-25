/**
 * Created by ww on 2018/3/25.
 */
$(
    function ($) {
        $("input[daterangepicker=daterangepicker]").daterangepicker({
            "showDropdowns": true,
            "showWeekNumbers": true,
            "timePicker24Hour": true,
            "locale": {
                "format": "YYYY-MM-DD",
                "separator": " -- ",
                "applyLabel": "Apply",
                "cancelLabel": "Cancel",
                "fromLabel": "From",
                "toLabel": "To",
                "customRangeLabel": "Custom",
                "weekLabel": "W",
                "daysOfWeek": [
                    "Su",
                    "Mo",
                    "Tu",
                    "We",
                    "Th",
                    "Fr",
                    "Sa"
                ],
                "monthNames": [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"
                ],
                "firstDay": 1
            },
            "startDate": Date.today().add({ days: -29 }),
            "endDate": Date.today(),
            "ranges": {
                'Today': [Date.today(), Date.today()],
                'Yesterday': [Date.today().add({ days: -1 }), Date.today().add({ days: -1 })],
                'Last 7 Days': [Date.today().add({ days: -6 }), Date.today()],
                'Last 30 Days': [Date.today().add({ days: -29 }), Date.today()],
                'This Month': [Date.today().moveToFirstDayOfMonth(), Date.today().moveToLastDayOfMonth()],
                'Last Month': [Date.today().moveToFirstDayOfMonth().add({ months: -1 }), Date.today().moveToFirstDayOfMonth().add({ days: -1 })]
            }
            // "startDate": "03/18/2018",
            // "endDate": "03/24/2018"
        }, function (start, end, label) {
            console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
        });
        console.log('jjjjj');
    }
);