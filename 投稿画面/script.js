document.getElementById('color').addEventListener('input', function() {
    const color = this.value;
    document.querySelector('.input1').style.color = color;
    document.querySelector('.input2').style.color = color;
});

const decreaseBtn = document.getElementById('decrease');
const increaseBtn = document.getElementById('increase');
const fontSizeDisplay = document.getElementById('fontSize');
const input1 = document.querySelector('.input1');
const input2 = document.querySelector('.input2');

decreaseBtn.addEventListener('click', () => {
    let fontSize = parseInt(fontSizeDisplay.textContent);
    if (fontSize > 1) {
        fontSize--;
        fontSizeDisplay.textContent = fontSize;
        input1.style.fontSize = `${fontSize}px`;
        input2.style.fontSize = `${fontSize}px`;
    }
});

increaseBtn.addEventListener('click', () => {
    let fontSize = parseInt(fontSizeDisplay.textContent);
    fontSize++;
    fontSizeDisplay.textContent = fontSize;
    input1.style.fontSize = `${fontSize}px`;
    input2.style.fontSize = `${fontSize}px`;
});

document.getElementById('bold').addEventListener('click', () => {
    toggleStyle('fontWeight', 'bold');
});

document.getElementById('italic').addEventListener('click', () => {
    toggleStyle('fontStyle', 'italic');
});

document.getElementById('underline').addEventListener('click', () => {
    toggleStyle('textDecoration', 'underline');
});

document.getElementById('align-left').addEventListener('click', () => {
    setAlignment('left');
});

document.getElementById('align-center').addEventListener('click', () => {
    setAlignment('center');
});

document.getElementById('align-right').addEventListener('click', () => {
    setAlignment('right');
});

function toggleStyle(style, value) {
    if (input1.style[style] === value) {
        input1.style[style] = '';
        input2.style[style] = '';
    } else {
        input1.style[style] = value;
        input2.style[style] = value;
    }
}

function setAlignment(alignment) {
    input1.style.textAlign = alignment;
    input2.style.textAlign = alignment;
}
