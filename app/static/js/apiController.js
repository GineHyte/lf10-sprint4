import axios from "https://cdn.jsdelivr.net/npm/axios@latest/+esm";
import NotificationController from "/static/js/notificationController.js";

export class ApiError {
    constructor(apiRequest) {
        this.apiRequest = apiRequest;
    }

    async processError(error) {
        const notificationController = NotificationController.getInstance()
        if (error.response) {
            if (error.response.status === 401 ||
                error.response.data.status === 401 ||
                error.response.data.Status === 401) return this.process401();
        } else if (error.request) {
            notificationController.showError(error.message);
        } else {

        }
        await Promise.reject(error)
    }

    async process401(error) {

    }
}

export class ApiRequest {
    url;
    requestOptions;
    body;

    constructor(method) {
        this.method = method;
        this.requestOptions = this.#requestOptions;
    }

    set endpoint(endpoint) {
        // use relative URL so requests stay same-origin and cookies are sent reliably
        this.url = `/api/${endpoint}`;
    }

    async useAccessToken() {
        const token = await StorageController.getInstance().getAccessToken();
        this.requestOptions.headers.Authorization = `Bearer ${token}`; // TODO: backendisch not implemented
    }

    async send() {
        let response;
        try {
            switch (this.method) {
                case 'POST':
                    response = await axios.post(this.url, this.body, this.requestOptions).then(this.#afterRequest);
                    break;
                case 'PUT':
                    response = await axios.put(this.url, this.body, this.requestOptions).then(this.#afterRequest);
                    break;
                case 'DELETE':
                    response = await axios.delete(this.url, this.requestOptions).then(this.#afterRequest);
                    break;
                case 'GET':
                    response = await axios.get(this.url, this.requestOptions).then(this.#afterRequest);
                    break;
                default:
                    console.error('Wrong API method:', this.method);
                    break;
            }
        } catch (error) {
            await this.#catchError(error);
        }
        return response;
    }

    async #afterRequest(response) {
        return await response.data;
    }

    async #catchError(error) {
        await new ApiError(this).processError(error);
    }

    get #requestOptions() {
        let options = {};
        let headers = {};

        if (this.method === 'GET') {
            headers.Accept = 'application/json';
        }

        if (this.method === 'POST') {
            headers.Accept = 'application/json';
            headers['Content-Type'] = 'application/json';
        }

        // ensure cookies (session cookie) are sent with requests
        options.withCredentials = true;
        options.headers = headers;
        return options;
    }
}


export default class ApiController {
    static #instance;

    static getInstance() {
        if (!ApiController.#instance)
            ApiController.#instance = new ApiController()
        return ApiController.#instance
    }

    async apiRenderOnlineFormStage(stage) {
        let request = new ApiRequest('GET');
        request.endpoint = `components/online_form_stages/${stage}`;
        return await request.send();
    }
}