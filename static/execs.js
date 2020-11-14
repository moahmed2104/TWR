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


/*document.querySelector("#mo").onclick = function() {
    mo_indicator = appear(mo_indicator, "mo_info")
}*/