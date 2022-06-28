window.addEventListener('load', function () {
    // Countries dropdown
    document.getElementById('countries').addEventListener('change', countryFilters);
    // Medication Status
    document.getElementById('selfMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('likelyMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noMedCheck').addEventListener('click', checkboxStatus);
    // Documents Held
    document.getElementById('diagnosisCheck').addEventListener('click', checkboxStatus);
    document.getElementById('hrtCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noDocCheck').addEventListener('click', checkboxStatus);
    // GIC selector
    document.getElementById('referralCheck').addEventListener('click', revealContent);
    $("#gics option[id='Northern Ireland']").hide();
    $("#gics option[id='Scotland']").hide();
    $("#gics option[id='Wales']").hide();
    $("#gics option[id='England']").hide();
});


function checkboxStatus() {
    // set check boxes
    var selfMed = document.getElementById("selfMedCheck");
    var selfMedLikely = document.getElementById("likelyMedCheck");
    var bridgingDesired = document.getElementById("bridgingDesired");
    var noMed = document.getElementById("noMedCheck");
    var diagnosis = document.getElementById("diagnosisCheck");
    var hrt = document.getElementById("hrtCheck");
    var noDoc = document.getElementById("noDocCheck");

    // conditions for Documents held
    (diagnosis.checked || hrt.checked) ? (noDoc.disabled = true) : (noDoc.disabled = false);
    noDoc.checked ? (diagnosis.disabled = true, hrt.disabled = true) : (diagnosis.disabled = false, hrt.disabled = false);

    // conditions for bridging
    (selfMed.checked || selfMedLikely.checked) && !hrt.checked ? (bridgingDesired.disabled = false) : (bridgingDesired.disabled = true, bridgingDesired.checked = false);

    // conditions for medication status
    if (selfMed.checked) {
        selfMedLikely.disabled = true;
        noMed.disabled = true;
    }
    else if (selfMedLikely.checked) {
        selfMed.disabled = true;
        noMed.disabled = true;
    }
    else if (noMed.checked) {
        selfMed.disabled = true;
        selfMedLikely.disabled = true;
    }
    else {
        selfMed.disabled = false;
        selfMedLikely.disabled = false;
        noMed.disabled = false;
    }


}

function countryFilters() {
    var countriesSelect = document.getElementById("countries");
    // Only allow submission when a country is selected
    if (countriesSelect.value !== "Choose...") {
        document.getElementById("docx").disabled = false;
        document.getElementById("pdf").disabled = false;
    }
    else {
        document.getElementById("docx").disabled = true;
        document.getElementById("pdf").disabled = true;
    }
    // filter valid GICs based on country
    $("#gics").val(0).change();
    if (countriesSelect.value === "England") {
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='England']").show();
    }
    else if (countriesSelect.value === "Northern Ireland") {
        $("#gics option[id='England']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='Northern Ireland']").show();
    }
    else if (countriesSelect.value === "Scotland") {
        $("#gics option[id='England']").hide();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='Scotland']").show();
    }
    else if (countriesSelect.value === "Wales") {
        $("#gics option[id='England']").hide();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").show();
    }
    else {
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='England']").hide();
    }
    
    
}

function revealContent() {
    var referralCheck = document.getElementById("referralCheck");
    var gicSelector = document.getElementById("gicSelector")
    referralCheck.checked ? gicSelector.hidden = false : gicSelector.hidden = true;
}