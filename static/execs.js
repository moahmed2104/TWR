var mo_indicator = false
var alaz_indicator = false
var usf_indicator = false
var lava_indicator = false
var mo_indicator = false
var mo_indicator = false
var mo_indicator = false



function appear(indicator, info_div_tag){
    if (indicator == false) {
        document.querySelector("#".concat(info_div_tag)).className = "shown";
        return true
    }
    else {
        document.querySelector("#".concat(info_div_tag)).className = "ghost";
        return false
    }
}


document.querySelector("#mo").onclick = function() {
    mo_indicator = appear(mo_indicator, "mo_info")
}
            
document.querySelector("#alaz").onclick = function() {
    alaz_indicator = appear(alaz_indicator, "alaz_info")
}
document.querySelector("#lava").onclick = function() {
    lava_indicator = appear(lava_indicator, "lava_info")
}

document.querySelector("#usf").onclick = function() {
    mo_indicator = appear(usf_indicator, "usf_info")
}