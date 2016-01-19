var year;
var month;
var day;
var hour;
var minute;


function pad(n,width,z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function getLastTenDates(startingdate) {
    var i = 10;
    hours = startingdate.getHours()
    minutes = startingdate.getMinutes()
    var timestamps = [];
    while (i > 0) {
        timestamps.push("" + pad(hours,2) + "" + pad(minutes,2))
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
    console.log(timestamps)
    return timestamps;
}

