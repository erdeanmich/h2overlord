
export class StatusBoard {
    public isEnabled: boolean = false;
    public temperature: number = 20;
    public humidity: number = 0.8;
    public isPumping: boolean = false;

    public getEnabledText(): string {
        return this.isEnabled ? "enabled" : "disabled"
    }

    public getFormattedHumidity(): string {
        return this.humidity * 100 + "%"
    }

    public getFormattedTemperature(): string {
        return this.temperature + "°C"
    }

    public getPumpingText(): string {
        return this.isPumping ? "Water is flowing" : "Water chills in the container"
    }
}