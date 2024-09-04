import { Routes } from '@angular/router';
import { WebcamComponent } from './pages/webcam/webcam.component';
import { OurWorkComponent } from './pages/our-work/our-work.component';
import { AboutComponent } from './pages/about/about.component';


export const routes: Routes = [
  {
    path: '',
    component: WebcamComponent
  },
  {
    path: 'ourWork',
    component: OurWorkComponent
  },
  {
    path:'about',
    component: AboutComponent
  }
];
