

function mapPostTraumaticStressSymptoms() {

    // Counters for intrusion symptoms, negative mood symptoms, dissociation symptoms and avoidance symptoms

    let intrusionSymptomsCount = 0;
    let negativeMoodCount = 0;
    let dissociationSymptomsCount = 0;
    let avoidanceSymptomsCount = 0;

    const intrusionSymptoms = document.querySelectorAll('#intrusion_symptoms1, #intrusion_symptoms2, #intrusion_symptoms3');
    
    // Count checked intrusion symptoms
    intrusionSymptoms.forEach(function(symptom) {
        if (symptom.checked) {
            intrusionSymptomsCount++;
        }
    });

    // Get all checkboxes for negative mood
    const negativeMoodSymptoms = document.querySelectorAll('#negative_mood1, #negative_mood2','#negative_mood3');
    
    // Count checked negative mood symptoms
    negativeMoodSymptoms.forEach(function(symptom) {
        if (symptom.checked) {
            negativeMoodCount++;
        }
    });

    // Get all checkboxes for dissociation
    const dissociationSymptoms = document.querySelectorAll('#dissociative_symptom1, #dissociative_symptom2', '#dissociative_symptom3');

    // Count checked dissociation symptoms
    dissociationSymptoms.forEach(function(symptom) {
        if (symptom.checked) {
            dissociationSymptomsCount++;
        }
    });


    // Get all checkboxes for avoidance
    const avoidanceSymptoms = document.querySelectorAll('#avoidance_symptoms1, #avoidance_symptoms3', '#avoidance_symptoms3');

    // Count checked avoidance symptoms
    avoidanceSymptoms.forEach(function(symptom) {
        if (symptom.checked) {
            avoidanceSymptomsCount++;
        }
    });
    
    return fetch('/symptoms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            intrusionSymptoms: intrusionSymptomsCount,
            negativeMoodSymptoms: negativeMoodCount,
            dissociationSymptoms: dissociationSymptomsCount,
            avoidanceSymptoms: avoidanceSymptomsCount
        })
    })
}


function mapTraumaticEvents() {
    const selectedEvents = [];
    const checkboxes = document.querySelectorAll('.form-check-input');

    checkboxes.forEach(checkbox => {
        if (checkbox.checked && checkbox.value !== 'True' && checkbox.value !== 'False') {
            selectedEvents.push(checkbox.value);
        }
    });

    return fetch('/traumatic-events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedEvents: selectedEvents
        })
    })
}

function mapPsycoactiveSubstances() {
    const psychoactiveOptions = document.getElementsByName('consumes_psychoactive_substances')

    let selectedValue = null;

    for (let option of psychoactiveOptions) {
        if (option.checked) {
            selectedValue = option.value;
            break;
        }
    }

    return fetch('/psychoactive_substances', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedValue: selectedValue
        })
    })
}

function agressiveImpulses () {
    
    const selectedOptions = document.getElementsByName('agressive_impulses');

    let selectedValue = null;

    for (let option of selectedOptions) {
        if (option.checked) {
            selectedValue = option.value;
            break;
        }
    }

    return fetch('/agressive_impulses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedValue: selectedValue
        })
    })
}

function depresionandAnxietyState () {
    
    const selectedOptions = document.getElementsByName('depresion');

    let selectedValue = null;

    for (let option of selectedOptions) {
        if (option.checked) {
            selectedValue = option.value;
            break;
        }
    }

    const selectedOptionsAnx = document.getElementsByName('anxiety');

    let selectedValueAnx = null;

    for (let option of selectedOptionsAnx) {
        if (option.checked) {
            selectedValueAnx = option.value;
            break;
        }
    }

    return fetch('/depresion_anxiety_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedValue: selectedValue,
            selectedValueAnx: selectedValueAnx
        })
    })
}

/**
 * Reset the page on load and when reset button is pressed
 */

function onSumbit() {
    
    const promises = [
        mapPostTraumaticStressSymptoms(),
        mapPsycoactiveSubstances(),
        agressiveImpulses(),
        depresionandAnxietyState(),
        mapTraumaticEvents(),
    ]

    Promise.all(promises).then(() => {
        window.location.href = '/chat/recommendations';
    })

}

function cleanProject() {
    fetch("/initialize")
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log(text);
    })
}