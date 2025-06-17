document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector('.search-bar input');
    const guideList = document.querySelector('.guides-list');

    const rawJson = document.getElementById('guides-data')?.textContent;
    const allGuides = rawJson ? JSON.parse(rawJson) : [];

    let debounceTimeout = null;

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            filterPage(event, allGuides, guideList);
        });
    }

    const searchForm = document.getElementsByClassName('search-bar')[0];
});

function filterPage(event, allGuides, guideList) {
    const query = event.target.value.trim().toLowerCase();

    if (query === "") {
        renderGuides(allGuides, guideList);
        return;
    }

    const filtered = allGuides.filter(guide =>
        guide.title.toLowerCase().includes(query)
    );

    renderGuides(filtered, guideList);

}

function renderGuides(guides, guideList) {
    guideList.innerHTML = "";

    if (guides.length === 0) {
        const noResult = document.createElement('div');
        noResult.textContent = "No guides found.";
        guideList.appendChild(noResult);
        return;
    }

    guides.forEach(guide => {
        const a = document.createElement('a');
        a.href = `/guides/${guide.slug}`;
        a.textContent = guide.title;
        guideList.appendChild(a);
    });
}

function api_call(event, debounceTimeout, guideList) {
    const query = event.target.value.trim();

    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(() => {
        if (query.length === 0) {
            console.log("Empty query.");
            return;
        }

        fetch(`/guides/search/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                updateGuideList(guideList, data.results);
            })
            .catch(error => {
                console.error("Search request failed:", error);
            });

    }, 300); // 300ms debounce
}

function updateGuideList(guideList, results) {
    guideList.innerHTML = ""; // Clear existing list

    if (results.length === 0) {
        const noResult = document.createElement('div');
        noResult.textContent = "No guides found.";
        guideList.appendChild(noResult);
        return;
    }

    results.forEach(guide => {
        const a = document.createElement('a');
        a.href = `/guides/${guide.slug}`;
        a.textContent = guide.title;
        guideList.appendChild(a);
    });

}