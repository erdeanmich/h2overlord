import { inject } from "aurelia";
import { IHttpClientService } from "./Services/HttpClientService";

@inject(IHttpClientService)
export class RootComponent {
    constructor(private httpClientService: IHttpClientService) {
        httpClientService.getStatus();
    }
}

