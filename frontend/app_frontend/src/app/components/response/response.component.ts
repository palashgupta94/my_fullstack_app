import {Component, OnInit} from '@angular/core';
import {Navigation, Router} from '@angular/router';

@Component({
  selector: 'app-response',
  standalone: false,
  templateUrl: './response.component.html',
  styleUrl: './response.component.css'
})
export class ResponseComponent implements OnInit{
  response: any;

  constructor(private router:Router) {
    const nav: Navigation | null = this.router.getCurrentNavigation();
    this.response = nav?.extras.state?.[ 'responseData' ];
  }

  ngOnInit(): void {
    // Redirect to main page after 5 seconds
    setTimeout(() => {
      console.log("Auto-redirecting to main page after 5 seconds");
      this.goBack();
    }, 5000);
  }

  goBack(): void {
    console.log("Navigating back to main page");
    this.router.navigate([ '/' ]).then();
  }
}
