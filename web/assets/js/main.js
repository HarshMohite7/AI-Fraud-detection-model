// Main JS file
console.log("Fund Detection System Loaded");

// Load components
async function loadComponent(id, url) {
    const response = await fetch(url);
    const text = await response.text();
    document.getElementById(id).innerHTML = text;
}

loadComponent('header-container', '../components/header.html');
loadComponent('footer-container', '../components/footer.html');
