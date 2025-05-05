import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl: string = 'http://127.0.0.1:5000/process';

  constructor(private http: HttpClient) { }

  submitData(data: any): any {
    return this.http.post(this.apiUrl, data);
  }
}
