import cronstrue from 'cronstrue';
import {bindable, BindingMode} from "aurelia";
import cron from "cron-validate";

export class ScheduleComponent {

    public schedule: string = '18:00';
    public duration: number = 20;
    @bindable public newSchedule: string = '';
    @bindable public newDuration: number = 0;

    public isValidTime(timeText: string): boolean {
        let regex = /\d\d:\d\d/i;
        return regex.test(timeText);
    }

    public isValidDuration(durationText :string) {
        let durationAmount : number = Number(durationText)
        return durationAmount > 0;
    }

    public newScheduleChanged(newVal: string, oldVal: string) {
       let isValid = this.isValidTime(newVal) && this.isValidDuration(String(this.newDuration));
        document.getElementById('button-configure')["disabled"] = !isValid;
    }

    public newDurationChanged(newVal:string, oldVal: string) {
        let isValid = this.isValidTime(this.newSchedule) && this.isValidDuration(newVal);
        document.getElementById('button-configure')["disabled"] = !isValid;
    }
}