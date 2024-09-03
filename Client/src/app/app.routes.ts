import { Routes } from '@angular/router';
import { WebcamComponent } from './pages/webcam/webcam.component';
import { OurWorkComponent } from './pages/our-work/our-work.component';


export const routes: Routes = [
  {
    path: '',
    component: WebcamComponent
  },
  {
    path: 'ourWork',
    component: OurWorkComponent
  }

];
