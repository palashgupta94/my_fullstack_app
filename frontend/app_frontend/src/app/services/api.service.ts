import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl: string = 'http://backend:5000/api/submit';

  constructor(private http: HttpClient) { }

  submitData(data: any): any {
    return this.http.post(this.apiUrl, data);
  }
}
