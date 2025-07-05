import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {OTHER_END_POINT, POST_END_POINT} from '../constants/ApiConstants';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // private apiUrl: string = 'http://backend:5000/api/submit';

  constructor(private http: HttpClient) { }

  submitData(data: any): any {
    return this.http.post(POST_END_POINT, data);
  }

  getAllData(): any{
    return this.http.get(OTHER_END_POINT);
  }

  getById(id: string): any{
    return this.http.get(`${OTHER_END_POINT}/` + String(id));
  }

  putById(id: number, data: any): any{
    return this.http.put(`${OTHER_END_POINT}/` + String(id), data);
  }

  deleteById(id: string): any{
    return this.http.delete(`${OTHER_END_POINT}/` + String(id));
  }
}
