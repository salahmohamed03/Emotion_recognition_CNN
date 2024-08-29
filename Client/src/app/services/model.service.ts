import { HttpClient } from '@angular/common/http';

import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { ImageDto } from '../interfaces/imageDto';


@Injectable({
  providedIn: 'root'
})
export class ModelService {
  apiUrl = environment.apiUrl;

  constructor(private http : HttpClient) { }

  detectFace(image64 : string){
    const img :ImageDto = {
      image64
    }
    return this.http.post<ImageDto>(this.apiUrl + '/detectFace64', img);
  }
}
