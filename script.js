let colorIndex = 0; // Start from the first color

function getNextColor() {
    const colors = ['#287eb8', '#284cb8', '#28a7b8'];
    const color = colors[colorIndex];
    colorIndex = (colorIndex + 1) % colors.length; // Loop back to the first color when we reach the end
    return color;
}

function toggleBox() {
            const box = document.getElementById('box');
            if (box.style.maxHeight === '0px') {
                box.style.maxHeight = box.scrollHeight + 'px';  // Show the box
                box.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                box.style.maxHeight = '0';  // Hide the box
            }
        }

// Set the cyclic color on each note element
colorIndex = 0;
document.querySelectorAll('note').forEach(note => {
    const nextColor = getNextColor();
    note.style.color = nextColor;  // Apply cyclic color
});
colorIndex = 0;
document.querySelectorAll('note').forEach(note => {
    const nextColor = getNextColor();
    note.style.color = nextColor;  // Apply cyclic color
    
});
document.getElementById('box').style.maxHeight = '0px';