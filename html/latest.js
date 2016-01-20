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

function getLastTenDates(startingDate) {
    var i = 10;
    console.log("Getting timestamps from " + startingDate)
    if (Math.round(startingDate.getMinutes()/10) *10 == 60) {
        startingDate.setMinutes(00)
        startingDate.setHours(startingDate.getHours()+1)
    } else {
        startingDate.setMinutes(Math.round(startingDate.getMinutes()/10)*10)
    }

    dateCursor = new Date(startingDate);

    var timestamps = [];
    while (i > 0) {
      
        timestamps.push(dateCursor.getFullYear() +
                        pad(dateCursor.getMonth()+1,2) + 
                        pad(dateCursor.getDate(),2) +
                        pad(dateCursor.getUTCHours(),2) + 
                        pad(dateCursor.getMinutes(),2))
        i -= 1
        dateCursor.setMinutes(dateCursor.getMinutes()-10)
    }
    console.log(timestamps)
    return timestamps.sort();
}

function makeImageRoster(dates) {
    var overview = document.getElementById("overview")
    for (i=0;i<dates.length;i++) {
        /*
         * We should really build this semantically but for now #fuckit
         *
         * */
        var next_image = "\n<img src=\"http://dd.weather.gc.ca/radar/PRECIPET/GIF/XSM/"
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
