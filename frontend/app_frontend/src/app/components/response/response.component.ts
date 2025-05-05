import { Component } from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-response',
  standalone: false,
  templateUrl: './response.component.html',
  styleUrl: './response.component.css'
})
export class ResponseComponent {
  response: any;

  constructor(private router:Router) {
    const nav = this.router.getCurrentNavigation();
    this.response = nav?.extras.state?.[ 'responseData' ];
  }

  goBack(): void {
    console.log("Navigating back to main page");
    this.router.navigate([ '/' ]).then();
  }
}
