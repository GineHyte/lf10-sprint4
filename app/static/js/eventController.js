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

        // Create and store the Promise
        this.#openPromise = new Promise((resolve, reject) => {
            // Register event handler for successful connection
            this.webSocketClient.onopen = (event) => {
                console.log('WebSocket connection established.');
                resolve(event); // Resolve the promise on successful open
            };

            // Register event handler for connection errors
            this.webSocketClient.onerror = (error) => {
                console.error('WebSocket error:', error);
                reject(error); // Reject the promise on error
            };
            
            // Optional: Handle clean closure
            this.webSocketClient.onclose = () => {
                this.#openPromise = null; // Clear promise on close
                console.log('WebSocket connection closed.');
            };
        });

        // The caller will now await this promise.
        return this.#openPromise;
    }

    async setCreditSessionFrontendVariable(key, value) {
        // 2. Await the function that checks and ensures the connection is ready
        await this.#checkOpennessOfWebSocket(); 

        const type = 2;
        const payload = { key, value }

        console.log('Sending payload:', payload);

        // At this point, the connection is guaranteed to be open (or an error was thrown)
        this.webSocketClient.send(JSON.stringify({ type, payload }))
    }

    // 3. Updated check to await the promise returned by 'open()'
    async #checkOpennessOfWebSocket() {
        // Check if the connection is already open (readyState 1)
        if (this.webSocketClient && this.webSocketClient.readyState === WebSocket.OPEN) {
            return;
        }

        // Check if the connection is currently connecting (readyState 0), and if so,
        // await the existing open promise without initiating a new connection.
        if (this.webSocketClient && this.webSocketClient.readyState === WebSocket.CONNECTING && this.#openPromise) {
            await this.#openPromise;
            return;
        }

        // If not open or connecting, call open() which initiates the connection and returns a promise to await.
        await this.open(); 
    } 

    #closeWebSocketConnection() {
        // alert("beforeunload") // Alerts are disruptive, often best left out of production code
        if (this.webSocketClient && this.webSocketClient.readyState === WebSocket.OPEN || this.webSocketClient.readyState === WebSocket.CONNECTING) {
            this.webSocketClient.close();
        }
    }
}

export default EventController