// Custom Cursor
const cursor = document.getElementById('cursor');
const trails = [
    document.getElementById('trail1'),
    document.getElementById('trail2'),
    document.getElementById('trail3')
];

let mouseX = 0, mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    cursor.style.left = (mouseX - 10) + 'px';
    cursor.style.top = (mouseY - 10) + 'px';
    
    trails.forEach((trail, index) => {
        setTimeout(() => {
            trail.style.left = (mouseX - 4) + 'px';
            trail.style.top = (mouseY - 4) + 'px';
            trail.style.opacity = 1 - (index * 0.25);
        }, (index + 1) * 50);
    });
});

// Hover effects
document.querySelectorAll('button, a, input').forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursor.classList.add('hovering');
    });
    el.addEventListener('mouseleave', () => {
        cursor.classList.remove('hovering');
    });
});

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
}
