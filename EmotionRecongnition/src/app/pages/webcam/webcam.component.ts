import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
@Component({
  selector: 'app-webcam',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './webcam.component.html',
  styleUrl: './webcam.component.css'
})
export class WebcamComponent {
  videoRef: any;
  imageref: any;
  play: boolean = false;
  constructor() { }
  togglePlay(){
    this.play = !this.play;
    if(this.play){
      navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
        })
        .then(stream => {
          this.videoRef.srcObject = stream;
        })
        .catch(err => {
          console.error('Error accessing the camera', err);
        });
    }else{
      this.videoRef.srcObject.getTracks().forEach((track: any) => {
        track.stop();
      });
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
    const data = canvas.toDataURL('image/png');
    this.imageref = document.getElementById('capturedImage');
    this.imageref.src = data;
  }

}
