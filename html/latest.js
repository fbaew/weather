var year;
var month;
var day;
var hour;
var minute;

var timestamps = [];

function getLastTenDates(startingdate) {
    var i = 10;
    hours = startingdate.getHours()
    minutes = startingdate.getMinutes()

    while (i > 0) {
        timestamps.push("" + hours + "" + minutes)
        i -= 1
        if (minutes >= 10) {
            minutes -= 10
        }
        else {
            minutes = 50
            if (hours > 0) {
                hours -= 1
            }
        }
    }
}
