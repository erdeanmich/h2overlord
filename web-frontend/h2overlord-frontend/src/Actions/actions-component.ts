import { batch, bindable, BindingMode, IEventAggregator, inject } from "aurelia";
import { IHttpClientService } from "../Services/HttpClientService";
import { StatusData } from "../Services/StatusData";

@inject(IHttpClientService, IEventAggregator)
export class ActionsComponent {
    @bindable({ mode: BindingMode.toView}) public isEnabled : boolean;
    @bindable({ mode: BindingMode.toView}) public isPumping : boolean;

    private isInitialUpdate: boolean = true;

    constructor(private httpClientService: IHttpClientService, private ea : IEventAggregator) {
        ea.subscribe('status', (statusData: StatusData) => this.OnStatusReceived(statusData))
    }

    private OnStatusReceived(statusData: StatusData) {
        this.isEnabled = statusData.isEnabled;
        this.isPumping = statusData.isRunning;
        this.isInitialUpdate = false;
    }

    public onToggleEnable() {
        if(this.isInitialUpdate) {
            return;
        }
        this.httpClientService.enablePumpAction();
    }

    public onToggleRunning() {
        if(this.isInitialUpdate) {
            return;
        }
        this.httpClientService.pumpRunningAction();
    }
}