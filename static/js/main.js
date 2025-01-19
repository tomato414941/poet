// API endpoints
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const latestThoughtElement = document.getElementById('latestThought');
const thoughtHistoryElement = document.getElementById('thoughtHistory');
const lastUpdateTimeElement = document.getElementById('lastUpdateTime');

// Constants
const UPDATE_INTERVAL = 10 * 60 * 1000; // 10 minutes in milliseconds
const POLLING_INTERVAL = 30 * 1000;     // 30 seconds in milliseconds

// Debug mode
const DEBUG = true;
function debug(message) {
    if (DEBUG) {
        console.log(`[DEBUG] ${message}`);
    }
}

// Format date and time
function formatDateTime(dateTimeStr) {
    try {
        const date = new Date(dateTimeStr.replace(' ', 'T'));
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            hour12: false
        }).format(date);
    } catch (error) {
        debug(`Error formatting date: ${error.message}`);
        return dateTimeStr;
    }
}

// Create HTML for a thought item
function createThoughtElement(thought) {
    return `
        <div class="thought-item border-l-4 border-blue-500 pl-4 py-4 mb-6">
            <div class="flex justify-between items-center mb-3">
                <time class="text-sm text-gray-500">${formatDateTime(thought.timestamp)}</time>
            </div>
            <div class="text-lg mb-3">${thought.thought}</div>
        </div>
    `;
}

// API Endpoints
const ENDPOINTS = {
    LATEST: `${API_BASE_URL}/thoughts/latest`,
    ALL: `${API_BASE_URL}/thoughts`
};

// Fetch and display the latest thought
async function fetchLatestThought() {
    try {
        debug('Fetching latest thought...');
        const response = await fetch(ENDPOINTS.LATEST);
        debug(`Latest thought response status: ${response.status}`);
        
        if (response.status === 404) {
            debug('No thoughts available yet');
            latestThoughtElement.innerHTML = `
                <p class="text-gray-600 italic">No thoughts generated yet</p>
            `;
            lastUpdateTimeElement.textContent = '';
            return;
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const thought = await response.json();
        debug(`Latest thought data: ${JSON.stringify(thought, null, 2)}`);
        
        latestThoughtElement.innerHTML = `
            <p class="text-xl mb-4">${thought.thought}</p>
            <div class="text-sm text-gray-500">
                <p>Previous Thought: ${thought.input}</p>
            </div>
        `;
        lastUpdateTimeElement.textContent = `Updated: ${formatDateTime(thought.timestamp)}`;
    } catch (error) {
        debug(`Error fetching latest thought: ${error.message}`);
        latestThoughtElement.innerHTML = `
            <p class="text-red-500">Failed to fetch latest thought</p>
            <p class="text-sm text-gray-500">${error.message}</p>
        `;
    }
}

// Fetch and display thought history
async function fetchThoughtHistory() {
    try {
        debug('Fetching thought history...');
        const response = await fetch(ENDPOINTS.ALL);
        debug(`History response status: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const thoughts = await response.json();
        debug(`Thought history data: ${JSON.stringify(thoughts, null, 2)}`);
        
        if (thoughts.length === 0) {
            thoughtHistoryElement.innerHTML = '<p class="text-gray-600 italic">No thoughts generated yet</p>';
            return;
        }
        
        // Display thought history in reverse chronological order, excluding the latest thought
        thoughtHistoryElement.innerHTML = thoughts
            .slice(0, -1) // Exclude the latest thought as it's shown in the latest thought section
            .reverse() // Sort in reverse chronological order
            .map(createThoughtElement)
            .join('');
    } catch (error) {
        debug(`Error fetching thought history: ${error.message}`);
        thoughtHistoryElement.innerHTML = `
            <p class="text-red-500">Failed to fetch thought history</p>
            <p class="text-sm text-gray-500">${error.message}</p>
        `;
    }
}

// Initialize the page
async function initialize() {
    debug('Initializing page...');
    await Promise.all([
        fetchLatestThought(),
        fetchThoughtHistory()
    ]);
}

// Auto-update functionality
let lastKnownThought = null;

async function checkForUpdates() {
    try {
        const response = await fetch(ENDPOINTS.LATEST);
        if (!response.ok) return;
        
        const latest = await response.json();
        if (!lastKnownThought || latest.id !== lastKnownThought.id) {
            debug('New thought detected, updating display...');
            lastKnownThought = latest;
            await Promise.all([
                fetchLatestThought(),
                fetchThoughtHistory()
            ]);
        }
    } catch (error) {
        debug(`Error checking for updates: ${error.message}`);
    }
}

// Start periodic updates
function startPeriodicUpdates() {
    // Check for updates every 30 seconds
    setInterval(checkForUpdates, POLLING_INTERVAL);
    // Update every 10 minutes
    setInterval(() => {
        initialize();
    }, UPDATE_INTERVAL);
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initialize();
    startPeriodicUpdates();
});
