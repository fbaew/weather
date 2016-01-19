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
    minutes = Math.round(startingdate.getMinutes()/10)*10
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

function makeImageRoster(dates) {
    var overview = document.getElementById("overview")
    for (i=0;i<dates.length;i++) {
        /*
         * We should really build this semantically but for now #fuckit
         *
         * */
        var next_image = "\n<img src=\"http://dd.weather.gc.ca/radar/PRECIPET/GIF/XSM/20160117"
        next_image += dates[i]+"_XSM_PRECIPET_RAIN.gif\" id=\"frame"+i+"\">";
        overview.innerHTML += next_image;
    }
}

function animate() {
    console.log("Frame " + document.frame);
    var animation = document.getElementById("animation")
    var framecell = document.getElementById("frame"+document.frame)
    console.log("anim: " + animation.src + " framecell: " + framecell.src);
    animation.src = framecell.src;
    document.frame += 1;
    if (document.frame >= document.dates.length) {
        document.frame = 0;
    }
}

function start() {
    document.frame = 0;
    document.dates = getLastTenDates(new Date())
    makeImageRoster(document.dates)
    window.setInterval(animate,1000)
}
