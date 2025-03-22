// Define the DataProcessor class
class DataProcessor {
    constructor() {
        this.awesomeLists = [];
        this.processedData = [];
        this.categories = new Set();
        this.listNames = new Set();
    }

    async init() {
        try {
            this.awesomeLists = await this.fetchData();
            this.processData();
            return {
                resources: this.processedData,
                categories: Array.from(this.categories).sort(),
                listNames: Array.from(this.listNames).sort()
            };
        } catch (error) {
            console.error('Error initializing data:', error);
            throw error;
        }
    }

    processData() {
        this.processedData = [];
        this.awesomeLists.forEach(list => {
            if (!list.name || !list.categories) {
                console.warn("List data missing required fields", list);
                return;
            }
            this.listNames.add(list.name);
            list.categories.forEach(category => {
                if (!category.name || !category.resources) {
                    console.warn("Category missing required fields", category);
                    return;
                }
                this.categories.add(category.name);
                category.resources.forEach(resource => {
                    if (!resource.name || !resource.url) {
                        console.warn("Resource missing name or URL", resource);
                        return;
                    }
                    this.processedData.push({
                        id: this.generateId(resource.name, resource.url),
                        name: resource.name,
                        description: resource.description || '',
                        url: resource.url,
                        category: category.name,
                        list: list.name,
                        tags: resource.tags || []
                    });
                });
            });
        });
    }

    generateId(name, url) {
        // Deterministic hash based on name and URL
        const data = name + url;
        let hash = 0;
        for (let i = 0; i < data.length; i++) {
            hash = ((hash << 5) - hash) + data.charCodeAt(i);
            hash |= 0;
        }
        return `${name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${Math.abs(hash)}`;
    }

    async fetchData() {
        try {
            const response = await fetch('data/awesome-lists.json');
            if (!response.ok) {
                throw new Error(`Failed to fetch data: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }
}

// Create a global instance of DataProcessor
const dataProcessor = new DataProcessor();
