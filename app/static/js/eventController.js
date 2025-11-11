class EventController {
    static #instance;
    webSocketClient;
    #openPromise = null; // 👈 New property to hold the connection promise

    static getInstance() {
        if (!EventController.#instance)
            EventController.#instance = new EventController()
        return EventController.#instance
    }

    constructor() {
        if (!window) return
        // Note: You need to bind 'this' or use an arrow function here, 
        // otherwise, '#closeWebSocketConnection' will run in the window context.
        window.addEventListener('beforeunload', () => this.#closeWebSocketConnection()); 
    }

    // 1. Modified 'open' to return a Promise that resolves on 'open'
    async open() {
        // If an open attempt is already in progress, return its promise
        if (this.#openPromise) {
            return this.#openPromise;
        }

        console.log('Opening WebSocket connection...');
        this.webSocketClient = new WebSocket(`ws://${window.location.hostname}:${window.location.port}/event_loop`);
    }

    async setCreditSessionFrontendVariable(key, value) {
        const type = 2;
        const payload = { key, value };

        this.webSocketClient.send(JSON.stringify({ type, payload }))
    }


}

export default EventController