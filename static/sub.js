var poli_indicator = false
var poetry_indicator = false
var econ_indicator = false
var free_indicator = false
var creative_indicator = false



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


document.querySelector("#polit").onclick = function() {
    poli_indicator = appear(poli_indicator, "poli")
}
            
document.querySelector("#poe").onclick = function() {
    poetry_indicator = appear(poetry_indicator, "poem")
}
document.querySelector("#bus").onclick = function() {
    econ_indicator = appear(econ_indicator, "econ")
}

document.querySelector("#write").onclick = function() {
    free_indicator = appear(free_indicator, "free")
}

document.querySelector("#creat").onclick = function() {
    creative_indicator = appear(creative_indicator, "creative")
}