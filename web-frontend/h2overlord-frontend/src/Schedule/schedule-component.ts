import {bindable, BindingMode, IEventAggregator, inject} from "aurelia";
import { IHttpClientService } from "../Services/HttpClientService";
import { StatusData } from "../Services/StatusData";

@inject(IHttpClientService, IEventAggregator)
export class ScheduleComponent {

    public schedule: string = '18:00';
    public duration: number = 20;
    @bindable({ mode: BindingMode.twoWay}) public newSchedule: string = '';
    @bindable({ mode: BindingMode.twoWay}) public newDuration: string = '0';

    constructor(private httpClientService: IHttpClientService, private ea : IEventAggregator) {
        ea.subscribe('status', (statusData: StatusData) => this.OnStatusReceived(statusData))
    }

    public isValidTime(timeText: string): boolean {
        let regex = /\d\d:\d\d/i;
        return regex.test(timeText);
    }

    public isValidDuration(durationText :string) {
        let durationAmount : number = Number(durationText)
        return durationAmount > 0;
    }

    public getFormattedSchedule(scheduleText : string, durationMinutes : number) : string {
        if(scheduleText == '' || scheduleText == undefined) {
            return "None"
        } else {
            return `Every day at ${scheduleText} for ${durationMinutes} minutes`
        }
    }

    public onSubmit() {
        this.httpClientService.pushNewSchedule(this.newSchedule, parseInt(this.newDuration))
    }

    public onClear() {
        this.httpClientService.pushNewSchedule('', 0)
    }

    public newScheduleChanged(newVal: string, oldVal: string) {
       let isValid = this.isValidTime(newVal) && this.isValidDuration(String(this.newDuration));
        document.getElementById('button-configure')["disabled"] = !isValid;
    }

    public newDurationChanged(newVal:string, oldVal: string) {
        let isValid = this.isValidTime(this.newSchedule) && this.isValidDuration(newVal);
        document.getElementById('button-configure')["disabled"] = !isValid;
    }

    private OnStatusReceived(statusData: StatusData) {
        this.schedule = statusData.currentSchedule
        this.duration = statusData.currentDuration
    }
}