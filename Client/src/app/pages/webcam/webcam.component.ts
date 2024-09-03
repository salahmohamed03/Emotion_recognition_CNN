import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ModelService } from '../../services/model.service';
import { Result } from '../../interfaces/result';
@Component({
  selector: 'app-webcam',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './webcam.component.html',
  styleUrl: './webcam.component.css'
})

export class WebcamComponent {
  videoRef: any;
  image: any;
  play: boolean = false;
  detectedFace : any;
  results: Array<Result> = [];

  constructor(
    private modelService: ModelService
  ) {}
  togglePlay(){
    this.play = !this.play;
    if(this.play){

      navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
        })
        .then(stream => {
          this.videoRef.style.backgroundImage = "url('https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg?s=612x612&w=0&k=20&c=qRydgCNlE44OUSSoz5XadsH7WCkU59-l-dwrvZzhXsI=')";
          this.videoRef.srcObject = stream;
        })
        .catch(err => {
          console.error('Error accessing the camera', err);
        })
        .finally(() => {
          if(!this.play){
            this.videoRef.srcObject.getTracks().forEach((track: any) => {
              track.stop();
            });
            this.videoRef.srcObject = null;

          }
        });
    }else{
      this.videoRef.srcObject.getTracks().forEach((track: any) => {
        track.stop();
      });
      this.videoRef.srcObject = null;
      this.image = null;
    }
  }
  ngOnInit(): void {
    this.videoRef = document.getElementById('webcam');
  }
  capture() {
    const canvas = document.createElement('canvas');
    canvas.width = this.videoRef.videoWidth;
    canvas.height = this.videoRef.videoHeight;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(this.videoRef, 0, 0, canvas.width, canvas.height);
    }
    const data = canvas.toDataURL('image/jpg');
    this.togglePlay();
    this.videoRef.style.backgroundImage = `url(${data})`;

    this.image = data;
  }
  uploadImage(event : any){
    const reader = new FileReader();
    reader.onload = (e) => {
      this.image = e.target?.result;
      this.videoRef.style.backgroundImage = `url(${this.image})`;
    }
    reader.readAsDataURL(event.target.files[0]);
  }
  // detectFace(){
  //   if(!this.image){
  //     alert('Please capture or upload an image');
  //     return;
  //   }
  //   this.modelService.detectFace(this.image).subscribe({
  //     next: (res) => {

  //       const result: Result = {
  //         emotion: 'happy',
  //         probability: 2,
  //         face64: `data:image/jpg;base64, ${res.image64}`
  //       }
  //       this.results.push(result);
  //     },
  //     error: (err) => {
  //       console.error(err);
  //     }
  //   });
  // }
  detectEmotion(){
    if(!this.image){
      alert('Please capture or upload an image');
      return;
    }
    this.modelService.detectEmotion(this.image).subscribe({
      next: (res) => {
        console.log(res);

        const result: Result = {
          emotion: res.emotion,
          position: res.position,
          image64: 'data:image/jpg;base64,'+res.image64
        }
      this.videoRef.style.backgroundImage = `url(${result.image64})`;

        this.results.push(result);
        this.image = null;
      },
      error: (err) => {
        console.error(err);
      }
    });
  }
  callResult(index : number){
    this.videoRef.style.backgroundImage = `url(${this.results[index].image64})`;
  }
}
