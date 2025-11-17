class EventController {
    static #instance;
    webSocketClient;
    #pendingRequests = new Map();
    #requestIdCounter = 0;

    static getInstance() {
        if (!EventController.#instance)
            EventController.#instance = new EventController()
        return EventController.#instance
    }

    constructor() {
        if (!window) return
        this.webSocketClient = new WebSocket(`ws://${window.location.hostname}:${window.location.port}/event_loop`);

        this.#setupEventHandlers();
        console.log("WebSocket connection opened")
        window.addEventListener("beforeunload", () => this.#closeConnection())
    }

    #setupEventHandlers() {
        this.webSocketClient.onmessage = (event) => {
            try {
                const response = JSON.parse(event.data);
                const { requestId } = response;

                const pending = this.#pendingRequests.get(requestId);
                if (pending) {
                    clearTimeout(pending.timeoutId);
                    pending.resolve();
                    this.#pendingRequests.delete(requestId);
                }
            } catch (err) {
                console.error('Error processing WebSocket message:', err);
            }
        };

        this.webSocketClient.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.webSocketClient.onclose = () => {
            console.log('WebSocket connection closed');
            this.#pendingRequests.forEach((pending) => {
                clearTimeout(pending.timeoutId);
                pending.reject(new Error('WebSocket connection closed'));
            });
            this.#pendingRequests.clear();
        };
    }

    #closeConnection() {
        this.#sendMessage(3)
    }

    async setCreditSessionFrontendVariable(key, value, wait_for_response = false) {
        const type = 2;
        const payload = { key, value };

        return await this.#sendMessage(type, payload, wait_for_response);
    }

    /**
     * Send a message via WebSocket
     * @param {number} type - Message type
     * @param {object} payload - Message payload
     * @param {boolean} wait_for_response - Whether to wait for backend confirmation
     * @returns {Promise<void>} Resolves when message is sent (or confirmed if waiting)
     */
    #sendMessage(type, payload = undefined, wait_for_response = false) {
        if (!wait_for_response) {
            return new Promise((resolve, reject) => {
                const message = payload
                    ? JSON.stringify({ type, payload, wait_for_response: false })
                    : JSON.stringify({ type, wait_for_response: false });

                this.#sendToWebSocket(message, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });
        }

        return new Promise((resolve, reject) => {
            const requestId = ++this.#requestIdCounter;

            const timeoutId = setTimeout(() => {
                this.#pendingRequests.delete(requestId);
                reject(new Error(`Request ${requestId} timed out`));
            }, 5000);

            this.#pendingRequests.set(requestId, {
                resolve,
                reject,
                timeoutId
            });

            const message = payload
                ? JSON.stringify({ type, payload, wait_for_response: true, requestId })
                : JSON.stringify({ type, wait_for_response: true, requestId });

            this.#sendToWebSocket(message, (error) => {
                if (error) {
                    clearTimeout(timeoutId);
                    this.#pendingRequests.delete(requestId);
                    reject(error);
                }
            });
        });
    }

    /**
     * Internal helper to send message to WebSocket
     * @param {string} message - JSON stringified message
     * @param {function} callback - Callback(error) to handle send result
     */
    #sendToWebSocket(message, callback) {
        if (this.webSocketClient.readyState === WebSocket.OPEN) {
            try {
                this.webSocketClient.send(message);
                callback(null);
            } catch (err) {
                callback(new Error(`Failed to send message: ${err.message}`));
            }
        } else if (this.webSocketClient.readyState === WebSocket.CONNECTING) {
            this.webSocketClient.addEventListener('open', () => {
                try {
                    this.webSocketClient.send(message);
                    callback(null);
                } catch (err) {
                    callback(new Error(`Failed to send message: ${err.message}`));
                }
            }, { once: true });
        } else {
            callback(new Error('WebSocket is not connected'));
        }
    }
}

export default EventController