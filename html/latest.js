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
        startingDate.setMinutes(startingDate.getMinutes()-10)
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

/*
    * From http://dd.weather.gc.ca/radar/doc/README_radar.txt
    * 
    * 1. PRECIP-ET
    * Images for regional composites (5 regions of Canada) and individual radar are
    * available.  Two intensities scale (8 and 14 colors) are also available for each
    * image. 
    * 
    * Composites with 14 colors intensity scale:
    *   YYYMMDDHHmm_XXX_PRECIPET_RAIN_WT.gif 
    *   YYYMMDDHHmm_XXX_PRECIPET_SNOW_WT.gif 
    *   ex: 201409201350_ATL_PRECIPET_RAIN_WT.gif
    * 
    *   Composites with 8 colors intensity scale:
    *   - YYYMMDDHHmm_XXX_PRECIPET_RAIN_A11Y.gif 
    *   - YYYMMDDHHmm_XXX_PRECIPET_SNOW_A11Y.gif 
    *   - ex: 201409201350_ATL_PRECIPET_RAIN_A11Y.gif
    * 
    *   Individual radar with 14 colors intensity scale:
    *   - YYYMMDDHHmm_XXX_PRECIPET_RAIN.gif 
    *   - YYYMMDDHHmm_XXX_PRECIPET_SNOW.gif (14 colors for Snow)
    *   -  ex: 201409201400_XFT_PRECIPET_RAIN.gif
    * 
    *   Individual radar with 8 colors intensity scale:
    *   - YYYMMDDHHmm_XXX_PRECIPET_RAIN_A11Y.gif 
    *   - YYYMMDDHHmm_XXX_PRECIPET_SNOW_A11Y.gif (14 colors for Snow)
    *   - ex: 201409201400_XFT_PRECIPET_RAIN_A11Y.gif
    * 
    *   2. CAPPI
    *   - YYYMMDDHHmm_XXX_CAPPI_1.5_RAIN_AGL.gif
    *   - YYYMMDDHHmm_XXX_CAPPI_1.0_SNOW_AGL.gif
    *   - ex: 200806191550_WHK_CAPPI_1.5_RAIN_AGL.gif
    * 
    *   3. 24_HR_ACCUM (based on the PRECIP product)
    *   - YYYMMDDHHmm_XXX_24_HR_ACCUM_MM.gif
    *   - ex: 200806161900_WBI_24_HR_ACCUM_MM.gif
    * 
    * 
    *   Product times are in universal time (UTC).
    *   XXX is the 3 letter radar identifier.
    * 
    */


    var overview = document.getElementById("overview")
    for (i=0;i<dates.length;i++) {
        /*
         * We should really build this semantically but for now #fuckit
         *
         * */
        var next_image = "\n<img src=\"http://dd.weather.gc.ca/radar/PRECIPET/GIF/XSM/"
        next_image += dates[i]+"_XSM_PRECIPET_SNOW.gif\" id=\"frame"+i+"\">";
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

    document.getElementById("frame").innerHTML = document.dates[document.frame]
}

function start() {
    document.frame = 0;
    document.dates = getLastTenDates(new Date())
    makeImageRoster(document.dates)
    window.setInterval(animate,500)
}
