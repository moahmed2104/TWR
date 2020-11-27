var poli_indicator = false
var creative_indicator = false
var econ_indicator = false
var free_indicator = false




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
    free_indicator = appear(true,"free")
    poli_indicator = appear(poli_indicator, "poli")
}
            
document.querySelector("#creat").onclick = function() {
    econ_indicator = appear(true,"econ")
    poli_indicator = appear(true,"poli")
    free_indicator = appear(true,"free")
    creative_indicator = appear(creative_indicator, "creative")
}
document.querySelector("#bus").onclick = function() {
    creative_indicator = appear(true,"creative")
    poli_indicator = appear(true,"poli")
    free_indicator = appear(true,"free")
    econ_indicator = appear(econ_indicator, "econ")
}

document.querySelector("#write").onclick = function() {
    econ_indicator =appear(true,"econ")
    creative_indicator = appear(true,"creative")
    poli_indicator = appear(true,"poli")
    free_indicator = appear(free_indicator, "free")
}
