from dataclasses import dataclass


@dataclass
class PumpState:
    isEnabled: bool
    isRunning: bool
    temperature: float
    humidity: float
    currentSchedule: str
    currentDuration: int