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
    econ_indicator = appear(true,"econ")
    creative_indicator = appear(true,"creative")
    poetry_indicator = appear(true,"poem")
    free_indicator = appear(true,"free")
    poli_indicator = appear(poli_indicator, "poli")
}
            
document.querySelector("#poe").onclick = function() {
    econ_indicator = appear(true,"econ")
    creative_indicator = appear(true,"creative")
    poli_indicator = appear(true,"poli")
    free_indicator = appear(true,"free")
    poetry_indicator = appear(poetry_indicator, "poem")
}
document.querySelector("#bus").onclick = function() {
    creative_indicator = appear(true,"creative")
    poli_indicator = appear(true,"poli")
    free_indicator = appear(true,"free")
    poetry_indicator = appear(true,"poem")
    econ_indicator = appear(econ_indicator, "econ")
}

document.querySelector("#write").onclick = function() {
    econ_indicator =appear(true,"econ")
    creative_indicator = appear(true,"creative")
    poli_indicator = appear(true,"poli")
    poetry_indicator = appear(true,"poem")
    free_indicator = appear(free_indicator, "free")
}

document.querySelector("#creat").onclick = function() {
    econ_indicator = appear(true,"econ")
    free_indicator = appear(true,"free")
    poetry_indicator = appear(true,"poem")
    poli_indicator = appear(true,"poli")
    creative_indicator = appear(creative_indicator, "creative")
}