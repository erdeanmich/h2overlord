import { DI, IEventAggregator, resolve } from "aurelia";
import { HttpClient } from "@aurelia/fetch-client";
import { StatusData } from "./StatusData";

export class HttpClientService {
    public httpClient = new HttpClient();
    private readonly ea : IEventAggregator = resolve(IEventAggregator);
    
    constructor() {
        this.httpClient.configure(config => {
            config
            .withDefaults({ 
                'mode': 'cors'
            })
            .withBaseUrl('http://h2overlord:8080')
        })
    }

    public getStatus() :void {
        this.httpClient.get('/status')
        .then(response => response.json())
        .then((statusData: StatusData) => {
            this.ea.publish('status', statusData)
        })
        .catch(error => console.error(error))
    }

    public enablePumpAction(): void {

        this.httpClient.post('/action/pump-enable')
        .then(response => response.json())
        .then((statusData: StatusData) => {
            this.ea.publish('status', statusData)
        })
        .catch(error => console.error(error))
    }
    
    public pumpRunningAction(): void {

        this.httpClient.post('/action/pump-running')
        .then(response => response.json())
        .then((statusData: StatusData) => {
            this.ea.publish('status', statusData)
        })
        .catch(error => console.error(error))
    }

    public pushNewSchedule(time: string, duration: number) {
        this.httpClient.post('/schedule', JSON.stringify({ time: time, duration: duration}))
            .then(response => response.json())
            .then((statusData: StatusData) => {
                this.ea.publish('status', statusData)
            })
            .catch(error => console.error(error))
    }
}


export const IHttpClientService = DI.createInterface<IHttpClientService>(
    'IHttpClientService',
    x => x.singleton(HttpClientService)
)
export type IHttpClientService = HttpClientService;
