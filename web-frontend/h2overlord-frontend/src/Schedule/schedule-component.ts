import cronstrue from 'cronstrue';
import {bindable, BindingMode} from "aurelia";
import cron from "cron-validate";

export class ScheduleComponent {
    public schedule: string = '0 18 * * *';
    public duration: number = 20;
    @bindable public newSchedule: string = '';
    @bindable public newDuration: number = 0;

    public getFormattedSchedule(cronText: string): string {
        if (this.isValidCron(cronText)) {
            return cronstrue.toString(cronText, {use24HourTimeFormat: true})
        } else {
            return "No valid cron";
        }
    }

    public isValidCron(cronText: string): boolean {
        return cron(cronText).isValid();
    }

    public newScheduleChanged(newVal: string, oldVal: string) {
       let isValid = this.isValidCron(newVal);
        document.getElementById('button-configure')["disabled"] = !isValid;
    }
}