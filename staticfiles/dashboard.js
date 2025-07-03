function toggleMenu() {
    let menu = document.querySelector(".side-menu");
    menu.classList.toggle("open");
}

function toggleTheme() {
    
    document.body.classList.toggle('dark-mode');
    const savedTheme = localStorage.getItem('theme');
    const isDark = savedTheme === 'dark';

    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = isDark ? '☀️' : '🌙';

}

// Auto-apply saved theme
window.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }
});
