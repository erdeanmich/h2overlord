import Aurelia, {StyleConfiguration} from 'aurelia';
import { RootComponent } from './root-component';
import {StatusBoard} from "./Status/status-board";
import {CardComponent} from "./Reusable/card-component";
import {ScheduleComponent} from "./Schedule/schedule-component";
import {ActionsComponent} from "./Actions/actions-component";

Aurelia
    .register(StatusBoard)
    .register(CardComponent)
    .register(ScheduleComponent)
    .register(ActionsComponent)
    .app(RootComponent)
    .start();
