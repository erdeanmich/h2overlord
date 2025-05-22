import { bindable, IEventAggregator, inject } from "aurelia";
import { IHttpClientService } from "../Services/HttpClientService";
import { StatusData } from "../Services/StatusData";

@inject(IHttpClientService, IEventAggregator)
export class ActionsComponent {
    @bindable public isEnabled : boolean = false;
    @bindable public isPumping : boolean = false;

    constructor(private httpClientService: IHttpClientService, private ea : IEventAggregator) {
        ea.subscribe('status', this.OnStatusReceived)
    }

    private OnStatusReceived(statusData: StatusData) {
        this.isEnabled = statusData.isEnabled
        this.isPumping = statusData.isRunning
    }

    public isEnabledChanged(newVal: boolean, oldVal: boolean) {
        console.log('hey')
        this.httpClientService.enablePumpAction();
    }

    public isPumpingChanged(newVal: boolean, oldVal: boolean) {
        this.httpClientService.pumpRunningAction();
    }
}