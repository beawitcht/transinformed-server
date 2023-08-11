window.addEventListener('load', function () {
    revealContent();
    privateProviderConditions();
    countryFilters();
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

    // Private provider selector
    document.getElementById('sharedCareCheck').addEventListener('click', revealContent);
    // Private provider dropdown
    document.getElementById('privateProviderList').addEventListener('change', privateProviderConditions);

    // Immigration options
    document.getElementById('immigrationCheck').addEventListener('click', revealContent);
    document.getElementById('immigrationCheck').addEventListener('click', checkboxStatus);

    document.getElementById("docx").addEventListener('click', submitActionsDocx);
    document.getElementById("pdf").addEventListener('click', submitActionsPdf);

});

function checkboxStatus() {
    // set check boxes
    var selfMed = document.getElementById("selfMedCheck");
    var selfMedLikely = document.getElementById("likelyMedCheck");
    var bridgingDesired = document.getElementById("bridgingDesired");
    var bridgingDesiredLabel = document.getElementById("bridgingDesiredLabel");
    var noMed = document.getElementById("noMedCheck");
    var diagnosis = document.getElementById("diagnosisCheck");
    var hrt = document.getElementById("hrtCheck");
    var noDoc = document.getElementById("noDocCheck");
    var privMed = document.getElementById("privateMedCheck");
    var immMed = document.getElementById("foreignMedCheck");
    var immCheck = document.getElementById("immigrationCheck");
    var immLetter = document.getElementById("immigrationLetterCheck");

    if (noMed.checked) {
        bridgingDesired.disabled = true;
        bridgingDesired.innerHTML = 'I)';
    }
    
    // conditions for Documents held
    (diagnosis.checked || hrt.checked) ? (noDoc.disabled = true) : (noDoc.disabled = false);
    noDoc.checked ? (diagnosis.disabled = true, hrt.disabled = true) : (diagnosis.disabled = false, hrt.disabled = false);

    // conditions for bridging
    (selfMed.checked || selfMedLikely.checked) && !hrt.checked && !noMed.checked ? (bridgingDesired.disabled = false, bridgingDesiredLabel.innerHTML = 'I need a bridging prescription') : (bridgingDesired.disabled = true, bridgingDesired.checked = false, bridgingDesiredLabel.innerHTML = 'I need a bridging prescription (invalid medication status for bridging)');
    
    if (hrt.checked) {
        bridgingDesired.disabled = true;
        bridgingDesired.checked = false;
        bridgingDesiredLabel.innerHTML = 'I need a bridging prescription (invalid document status for bridging)';
    }

    if ($('.med-status-check:checked').length === 0 && !hrt.checked){
        bridgingDesired.disabled = true;
        bridgingDesired.checked = false;
        bridgingDesiredLabel.innerHTML = "I need a bridging prescription (select medication status)";
    }

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

    // conditions for immigration options
    if (!immCheck.checked){
        immLetter.checked = false;
    }
}

function disableButtonsLogic(){
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
}

function countryFilters() {
    var countriesSelect = document.getElementById("countries");
    var selectedCountry = countriesSelect.value;

    // Only allow submission when a country is selected
    disableButtonsLogic();

    // Define a mapping between countries and their corresponding GIC options
    var countryGICMapping = {
        "England": ["England"],
        "Northern Ireland": ["Northern Ireland"],
        "Scotland": ["Scotland"],
        "Wales": ["Wales"]
    };

    // Filter valid GICs based on country
    $("#gics").val(0).change();

    // Hide all country options initially
    $("#gics option[value='England'], #gics option[value='Northern Ireland'], #gics option[value='Scotland'], #gics option[value='Wales']").hide();

    // Show the options related to the selected country
    if (countryGICMapping[selectedCountry]) {
        countryGICMapping[selectedCountry].forEach(option => {
            $("#gics option[value='" + option + "']").show();
        });
    } else {
        $("#gics option[value='countryNeeded']").show();
    }
}

function revealContent() {
    var referralCheck = document.getElementById("referralCheck");
    var sharedCareCheck = document.getElementById("sharedCareCheck");
    var gicSelector = document.getElementById("gicSelector");
    var privateSelector = document.getElementById("privateSelector");
    var immigrationCheck = document.getElementById("immigrationCheck");
    var immigrationOption = document.getElementById("immigrationOption");
    referralCheck.checked ? gicSelector.hidden = false : gicSelector.hidden = true;
    sharedCareCheck.checked ? privateSelector.hidden = false : privateSelector.hidden = true;
    immigrationCheck.checked ? immigrationOption.hidden = false : immigrationOption.hidden = true;
}

function privateProviderConditions(){
    var privateProviderList = document.getElementById("privateProviderList");
    var privateProviderWarningMessage = document.getElementById("notUK")
    var privateProviderPreferredMessage = document.getElementById("preferred")
    if (privateProviderList.value === "GenderGP") {
        privateProviderList.classList.remove("is-valid");
        privateProviderList.classList.add("is-invalid");
        privateProviderWarningMessage.innerText =  "This provider is not based in the UK, which deters some GPs from agreeing to shared care."
    }
    else if (privateProviderList.value.includes("Other") || privateProviderList.value.includes("haven't chosen")) {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.remove("is-valid");
        privateProviderPreferredMessage.innerText = ""
        privateProviderWarningMessage.innerText = ""

    }
    else {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.add("is-valid");
        privateProviderPreferredMessage.innerText =  "This provider offers GMC registered and UK based specialists."
    }
}

// do these on submitting word
function submitActionsDocx(){
    $(this).append('<input type="hidden" name="docx" value="docx" /> ');
    $("#generationForm").removeProp("target");
    submitActions();
}

// do these on submitting pdf
function submitActionsPdf(){
    $(this).append('<input type="hidden" name="pdf" value="pdf" /> ');
    $("#generationForm").prop({"target": "_blank"});
    submitActions();
}

function submitActions(){
    if (gics.value !==  "0" ){
        if (gics.value !== "1"){
            $("#gics :selected").val($("#gics :selected").text());
        };
    };
    document.getElementById("generationForm").submit();
    
    const alertPlaceholder = document.getElementById('alertPlaceholder')
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-success alert-dismissible" role="alert">`,
        `   <div>Thank you for using our document generator, if you found this service useful please <a href="https://opencollective.com/beawitching/donate/" class="alert-link" target="_blank" >consider donating</a> so that we can maintain this service.</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')
    alertPlaceholder.append(wrapper)
    }
