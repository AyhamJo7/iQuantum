/**
 * Main JavaScript for iQuantum
 * Handles UI interactions and rendering
 */

document.addEventListener('DOMContentLoaded', async () => {
    // UI Elements
    const resourcesContainer = document.getElementById('resources-container');
    const resourceCount = document.getElementById('resource-count');
    const searchInput = document.getElementById('search');
    const categoryFilter = document.getElementById('category-filter');
    const listFilter = document.getElementById('list-filter');
    const resetFiltersBtn = document.getElementById('reset-filters');
    const sortBySelect = document.getElementById('sort-by');
    const toggleViewBtn = document.getElementById('toggle-view');
    const pageSizeSelect = document.getElementById('page-size');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfoSpan = document.getElementById('page-info');
    
    // State
    let resources = [];
    let filteredResources = [];
    let categories = [];
    let listNames = [];
    let currentView = 'grid'; // 'grid' or 'list'
    let currentPage = 1;
    let pageSize = 25; // Default page size
    let totalPages = 1;
    let fuseInstance = null; // Fuse.js instance for fuzzy search
    
    // Initialize
    try {
        const data = await dataProcessor.init();
        resources = data.resources;
        filteredResources = [...resources];
        categories = data.categories;
        listNames = data.listNames;
        
        // Set initial page size from dropdown
        pageSize = parseInt(pageSizeSelect.value);
        
        // Initialize Fuse.js for fuzzy search
        initializeFuseSearch();
        
        // Populate filter dropdowns
        populateFilterDropdowns();
        
        // Initial pagination setup
        updatePagination();
        
        // Initial render
        renderResources();
        
        // Set up event listeners
        setupEventListeners();
        
        // Load and display last update time
        loadLastUpdateTime();
    } catch (error) {
        console.error('Error initializing app:', error);
        resourcesContainer.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error loading resources. Please try again later.
                </div>
            </div>
        `;
    }
    
    /**
     * Populate category and list filter dropdowns
     */
    function populateFilterDropdowns() {
        // Populate categories
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
        
        // Populate list names
        listNames.forEach(listName => {
            const option = document.createElement('option');
            option.value = listName;
            option.textContent = listName;
            listFilter.appendChild(option);
        });
    }
    
    /**
     * Set up event listeners for UI interactions
     */
    function setupEventListeners() {
        // Search input
        searchInput.addEventListener('input', filterResources);
        
        // Category filter
        categoryFilter.addEventListener('change', filterResources);
        
        // List filter
        listFilter.addEventListener('change', filterResources);
        
        // Reset filters
        resetFiltersBtn.addEventListener('click', resetFilters);
        
        // Sort by
        sortBySelect.addEventListener('change', sortResources);
        
        // Toggle view
        toggleViewBtn.addEventListener('click', toggleView);
        
        // Page size
        pageSizeSelect.addEventListener('change', changePageSize);
        
        // Pagination controls
        prevPageBtn.addEventListener('click', goToPreviousPage);
        nextPageBtn.addEventListener('click', goToNextPage);
    }
    
    /**
     * Change the number of resources displayed per page
     */
    function changePageSize() {
        pageSize = parseInt(pageSizeSelect.value);
        currentPage = 1; // Reset to first page when changing page size
        updatePagination();
        renderResources();
    }
    
    /**
     * Go to the previous page
     */
    function goToPreviousPage() {
        if (currentPage > 1) {
            currentPage--;
            renderResources();
        }
    }
    
    /**
     * Go to the next page
     */
    function goToNextPage() {
        if (currentPage < totalPages) {
            currentPage++;
            renderResources();
        }
    }
    
    /**
     * Update pagination controls and information
     */
    function updatePagination() {
        totalPages = Math.ceil(filteredResources.length / pageSize);
        
        // Update page info
        pageInfoSpan.textContent = `Page ${currentPage} of ${totalPages}`;
        
        // Update button states
        prevPageBtn.disabled = currentPage <= 1;
        nextPageBtn.disabled = currentPage >= totalPages;
    }
    
    /**
     * Initialize Fuse.js for fuzzy search
     */
    function initializeFuseSearch() {
        // Configure Fuse.js options
        const fuseOptions = {
            // Search in these fields
            keys: [
                { name: 'name', weight: 2 },      // Higher weight for name
                { name: 'description', weight: 1 },
                { name: 'tags', weight: 1.5 },    // Higher weight for tags
                { name: 'category', weight: 1 },
                { name: 'list', weight: 1 }
            ],
            // Fuzzy search settings
            includeScore: true,
            threshold: 0.4,        // Lower threshold = more strict matching
            distance: 100,         // How far to search for matching characters
            minMatchCharLength: 2, // Minimum characters that must match
            shouldSort: false,     // We'll handle sorting separately
            useExtendedSearch: true,
            ignoreLocation: true   // Search the entire string, not just from the beginning
        };
        
        // Create Fuse instance with resources and options
        fuseInstance = new Fuse(resources, fuseOptions);
    }
    
    /**
     * Filter resources based on search input and dropdown selections
     */
    function filterResources() {
        const searchTerm = searchInput.value.trim();
        const selectedCategory = categoryFilter.value;
        const selectedList = listFilter.value;
        
        // Start with all resources
        let results = [...resources];
        
        // Apply fuzzy search if there's a search term
        if (searchTerm) {
            // Use Fuse.js for fuzzy search
            const searchResults = fuseInstance.search(searchTerm);
            results = searchResults.map(result => result.item);
        }
        
        // Apply category and list filters
        filteredResources = results.filter(resource => {
            // Category filter
            const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory;
            
            // List filter
            const matchesList = selectedList === 'all' || resource.list === selectedList;
            
            return matchesCategory && matchesList;
        });
        
        // Reset to first page when filtering
        currentPage = 1;
        updatePagination();
        renderResources();
    }
    
    /**
     * Reset all filters to their default values
     */
    function resetFilters() {
        searchInput.value = '';
        categoryFilter.value = 'all';
        listFilter.value = 'all';
        sortBySelect.value = 'name';
        
        filteredResources = [...resources];
        currentPage = 1; // Reset to first page
        updatePagination();
        renderResources();
    }
    
    /**
     * Sort resources based on the selected sort option
     */
    function sortResources() {
        const sortBy = sortBySelect.value;
        
        filteredResources.sort((a, b) => {
            switch (sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'category':
                    return a.category.localeCompare(b.category);
                case 'list':
                    return a.list.localeCompare(b.list);
                default:
                    return 0;
            }
        });
        
        // Reset to first page when sorting
        currentPage = 1;
        updatePagination();
        renderResources();
    }
    
    /**
     * Toggle between grid and list views
     */
    function toggleView() {
        currentView = currentView === 'grid' ? 'list' : 'grid';
        
        // Update button icon
        toggleViewBtn.innerHTML = currentView === 'grid' 
            ? '<i class="fas fa-th-list"></i>' 
            : '<i class="fas fa-th"></i>';
        
        // Keep the same page when toggling view
        renderResources();
    }
    
    /**
     * Load and display the last update time from metadata
     */
    async function loadLastUpdateTime() {
        const lastUpdatedElement = document.getElementById('last-updated');
        try {
            const response = await fetch('data/metadata.json');
            if (response.ok) {
                const metadata = await response.json();
                if (metadata.last_updated) {
                    const date = new Date(metadata.last_updated);
                    const formattedDate = date.toLocaleString();
                    lastUpdatedElement.textContent = `Last updated: ${formattedDate}`;
                }
            } else {
                lastUpdatedElement.textContent = 'Last updated: Unknown';
            }
        } catch (error) {
            console.error('Error loading metadata:', error);
            lastUpdatedElement.textContent = 'Last updated: Unknown';
        }
    }
    
    /**
     * Highlight search matches in text
     * @param {string} text - The text to highlight
     * @param {string} searchTerm - The search term to highlight
     * @returns {string} - HTML with highlighted search matches
     */
    function highlightMatches(text, searchTerm) {
        if (!searchTerm || !text) return text;
        
        // Escape special characters in the search term for regex
        const escapedSearchTerm = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        
        // Create a regex that's case insensitive
        const regex = new RegExp(`(${escapedSearchTerm})`, 'gi');
        
        // Replace matches with highlighted spans
        return text.replace(regex, '<span class="highlight">$1</span>');
    }
    
    /**
     * Render resources in the container
     */
    function renderResources() {
        // Update resource count
        resourceCount.textContent = filteredResources.length;
        
        // Update pagination
        updatePagination();
        
        // Clear container
        resourcesContainer.innerHTML = '';
        
        // Add appropriate class for view type
        resourcesContainer.className = currentView === 'grid' ? 'row grid-view' : 'row list-view';
        
        if (filteredResources.length === 0) {
            resourcesContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <div class="alert alert-info" role="alert">
                        <i class="fas fa-info-circle me-2"></i>
                        No resources found matching your filters.
                    </div>
                </div>
            `;
            return;
        }
        
        // Calculate pagination indices
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = Math.min(startIndex + pageSize, filteredResources.length);
        
        // Get current page resources
        const currentPageResources = filteredResources.slice(startIndex, endIndex);
        
        // Get search term for highlighting
        const searchTerm = searchInput.value.trim();
        
        // Render each resource for the current page
        currentPageResources.forEach(resource => {
            const colClass = currentView === 'grid' ? 'col-md-4 mb-4' : 'col-12 mb-3';
            
            // Highlight matches if there's a search term
            const highlightedName = searchTerm ? highlightMatches(resource.name, searchTerm) : resource.name;
            const highlightedDescription = searchTerm ? highlightMatches(resource.description, searchTerm) : resource.description;
            
            const resourceElement = document.createElement('div');
            resourceElement.className = colClass;
            
            resourceElement.innerHTML = `
                <div class="card resource-card h-100">
                    <div class="card-header">
                        <h5 class="mb-0 gradient-text">${highlightedName}</h5>
                        <span class="badge">${resource.list}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text">${highlightedDescription}</p>
                        <p class="card-text"><a href="${resource.url}" target="_blank">${resource.url}</a></p>
                        <div class="mb-2">
                            ${resource.tags.map(tag => {
                                const highlightedTag = searchTerm ? highlightMatches(tag, searchTerm) : tag;
                                return `<span class="resource-tag">${highlightedTag}</span>`;
                            }).join('')}
                        </div>
                        <p class="mb-0"><strong>Category:</strong> ${resource.category}</p>
                    </div>
                    <div class="card-footer">
                        <a href="${resource.url}" class="btn" target="_blank">
                            <i class="fas fa-external-link-alt me-1"></i> Visit
                        </a>
                    </div>
                </div>
            `;
            
            resourcesContainer.appendChild(resourceElement);
        });
    }
});
