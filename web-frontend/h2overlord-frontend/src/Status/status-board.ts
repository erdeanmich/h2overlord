import { bindable, BindingMode, IEventAggregator, inject } from "aurelia";
import { IHttpClientService } from "../Services/HttpClientService";
import { StatusData } from "../Services/StatusData";

@inject(IHttpClientService, IEventAggregator)
export class StatusBoard {
    @bindable({mode: BindingMode.toView}) public enabledText: string
    @bindable({mode: BindingMode.toView}) public temperatureText: string
    @bindable({mode: BindingMode.toView}) public humidityText: string
    @bindable({mode: BindingMode.toView}) public pumpingText: string
    @bindable({mode: BindingMode.toView}) public isPumping: boolean = false;

    private isEnabled: boolean = false;
    private temperature: number = 20;
    private humidity: number = 0.8;

    constructor(private httpClientService: IHttpClientService, private ea : IEventAggregator) {
        ea.subscribe('status', (statusData: StatusData) => this.OnStatusReceived(statusData))
    }

    private formatEnabled(): string {
        let text = this.isEnabled ? "enabled" : "disabled";
        return "Pump is: " + text;
    }

    private formatHumidity(): string {
        let text = new Intl.NumberFormat('de-DE', {style: 'percent' })
        .format(this.humidity / 100);
        return "Humidity: " + text;
    }

    private formatTemperature(): string {
        let text = new Intl.NumberFormat('de-DE', {style: 'unit', unit: 'celsius' })
        .format(this.temperature);
        return "Temperature: " + text;
    }

    private formatPumping(): string {
        return this.isPumping ? "Water is flowing" : "Water chills in the container";
    }

    private OnStatusReceived(statusData: StatusData) {
        this.isEnabled = statusData.isEnabled;
        this.isPumping = statusData.isRunning;
        this.temperature = statusData.temperature;
        this.humidity = statusData.humidity;

        this.enabledText = this.formatEnabled();
        this.humidityText = this.formatHumidity();
        this.pumpingText = this.formatPumping();
        this.temperatureText = this.formatTemperature();
    }
}