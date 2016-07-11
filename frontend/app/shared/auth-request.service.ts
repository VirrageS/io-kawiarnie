import { Injectable } from 'angular2/core';

import {Http, Response, RequestOptions, Headers, Request, RequestMethod} from 'angular2/http';

@Injectable()
export class AuthHttp {
  constructor(
    private http: Http) {
  }

  post(url: string, data: any) {
    var headers = new Headers();
    headers.append("Content-Type", 'application/json');
    headers.append("Authorization", 'Bearer ' + localStorage.getItem('id_token'));

    var requestoptions = new RequestOptions({
      method: RequestMethod.Post,
      url: url,
      headers: headers,
      body: JSON.stringify(data)
    });

    return this.http.request(new Request(requestoptions)).map(
      (res: Response) => {
        if (res) {
          return [{ status: res.status, json: res.json() }]
        }
      }
    );
  }

  get(url: string, data: any) {
    var headers = new Headers();
    headers.append("Content-Type", 'application/json');
    headers.append("Authorization", 'Bearer ' + localStorage.getItem('id_token'));

    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: url,
      headers: headers,
      body: JSON.stringify(data)
    });

    return this.http.request(new Request(requestoptions)).map(
      (res: Response) => {
        if (res) {
          return [{ status: res.status, json: res.json() }]
        }
      }
    );
  }
}
