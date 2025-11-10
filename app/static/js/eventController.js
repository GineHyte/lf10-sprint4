class EventController {
    static #instance;
    webSocketClient;

    static getInstance() {
        if (!EventController.#instance)
            EventController.#instance = new EventController()
        return EventController.#instance
    }

    constructor() {
        if (!window) return
        this.webSocketClient = new WebSocket(`ws://${window.location.hostname}:${window.location.port}/event_loop`);
    }

    async setCreditSessionFrontendVariable(key, value) {
        const type = 2;
        const payload = { key, value }

        this.webSocketClient.send(JSON.stringify({ type, payload }))
    }


}

export default EventController