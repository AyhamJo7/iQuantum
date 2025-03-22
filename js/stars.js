/**
 * Stars background effect
 * Generates a starry night sky with parallax effect
 */

document.addEventListener('DOMContentLoaded', () => {
    // Generate stars for each layer
    generateStars('stars', 700, 1);
    generateStars('stars2', 200, 2);
    generateStars('stars3', 100, 3);
    
    // Add animation to stars
    animateStars();
});

/**
 * Generate stars for a specific layer
 * @param {string} elementId - The ID of the element to add stars to
 * @param {number} count - Number of stars to generate
 * @param {number} size - Size of stars in pixels
 */
function generateStars(elementId, count, size) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Set element style
    element.style.width = size + 'px';
    element.style.height = size + 'px';
    element.style.background = 'transparent';
    
    // Check if light theme is active
    const isLightTheme = document.body.classList.contains('light-theme');
    const starColor = isLightTheme ? '#000' : '#FFF';
    
    // Generate box shadow for stars
    let boxShadow = '';
    for (let i = 0; i < count; i++) {
        const x = Math.floor(Math.random() * 2000);
        const y = Math.floor(Math.random() * 2000);
        
        boxShadow += `${x}px ${y}px ${starColor}`;
        if (i < count - 1) {
            boxShadow += ', ';
        }
    }
    
    // Apply box shadow
    element.style.boxShadow = boxShadow;
    
    // Create after element with same box shadow
    const style = document.createElement('style');
    style.setAttribute('data-stars-style', elementId);
    style.textContent = `
        #${elementId}:after {
            content: " ";
            position: absolute;
            top: 2000px;
            width: ${size}px;
            height: ${size}px;
            background: transparent;
            box-shadow: ${boxShadow};
        }
    `;
    document.head.appendChild(style);
}

/**
 * Add animation to stars
 */
function animateStars() {
    const stars1 = document.getElementById('stars');
    const stars2 = document.getElementById('stars2');
    const stars3 = document.getElementById('stars3');
    
    if (stars1) stars1.style.animation = 'animStar 50s linear infinite';
    if (stars2) stars2.style.animation = 'animStar 100s linear infinite';
    if (stars3) stars3.style.animation = 'animStar 150s linear infinite';
}
