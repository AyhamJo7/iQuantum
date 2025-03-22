/**
 * Dark theme functionality
 * Handles stars generation for dark theme
 */

document.addEventListener('DOMContentLoaded', () => {
    // Always use dark theme
    localStorage.setItem('theme', 'dark');
    
    // Generate stars on initial load
    regenerateStars();
});

/**
 * Regenerate stars for dark theme
 */
function regenerateStars() {
    // Clear existing stars
    const starsElements = ['stars', 'stars2', 'stars3'];
    starsElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.boxShadow = '';
        }
    });
    
    // Remove existing after elements
    const oldStyles = document.querySelectorAll('style[data-stars-style]');
    oldStyles.forEach(style => style.remove());
    
    // Regenerate stars
    generateStars('stars', 700, 1);
    generateStars('stars2', 200, 2);
    generateStars('stars3', 100, 3);
}
