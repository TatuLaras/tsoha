// This script is for editing the multiple choice questions

let choices = [];

const choiceEditor = document.querySelector('#choice-editor');
const choicesData = document.querySelector('#choices-data');
const choiceLabelInput = document.querySelector('#choice-label-input');
const choiceIsCorrectInput = document.querySelector('#choice-iscorrect-input');

function choiceEntry(i, choice) {
    const contents = `
            <div class="label">${choice.label}</div>
            <button class="delete" onclick="deleteChoice(event, ${i})" title="Poista vaihtoehto">
                <i class="fa-solid fa-trash"></i>
            </button>
        `;

    const parent = document.createElement('div');
    parent.classList.add('choice');
    if (choice.is_correct) parent.classList.add('correct');
    parent.id = `choice-${i}`;

    parent.innerHTML = contents;
    return parent;
}

function refreshChoices() {
    if (!choiceEditor || !choicesData) return;

    choiceEditor.innerHTML = `<div class="text-disabled">Ei vaihtoehtoja.</div>`;

    choices.forEach((choice, i) => {
        if (i == 0) choiceEditor.innerHTML = '';

        choiceEditor.appendChild(choiceEntry(i, choice));
    });

    // Reset the form
    choicesData.value = JSON.stringify(choices);
    choiceIsCorrectInput.checked = false;
}

function addChoice(e) {
    e.preventDefault();
    if (!choiceLabelInput || choiceLabelInput.value.length == 0) return;

    choices.push({
        label: choiceLabelInput.value,
        is_correct: choiceIsCorrectInput.checked,
    });

    choiceLabelInput.value = '';

    refreshChoices();
}

function deleteChoice(e, i) {
    e.preventDefault();

    choices.splice(i, 1);

    refreshChoices();
}
