import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {getISTISOString} from '../../utility/date-converter.utility';


@Component({
  selector: 'app-form',
  standalone: false,
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent implements OnInit {
  public loginForm!: FormGroup;
  formData: any = { username: "", email: "" };
  response: any;

  constructor(
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      userName: ['', Validators.required],
      email: ['', Validators.required],
      gender: ['', Validators.required],
      createdAt: [new Date().toISOString()],
      updatedAt: [new Date().toISOString()]
    });
    console.info("loginForm: ", this.loginForm);
  }

  onSubmit(): void {
    console.log("form data before: ", this.formData);
    this.formData.firstName = this.loginForm.value.firstName;
    this.formData.lastName = this.loginForm.value.lastName;
    this.formData.username = this.loginForm.value.userName;
    this.formData.email = this.loginForm.value.email;
    this.formData.gender = this.loginForm.value.gender;
    this.formData.createdAt = getISTISOString();
    // this.formData.updatedAt = new Date().toISOString().toString();
    this.formData.updatedAt = getISTISOString();
    console.log("form data after: ", this.formData);

    this.apiService.submitData(this.formData).subscribe(
      (res: any): void => {
        if (res && res.status === 'success') {
          this.response = res;
          console.log("Success response: ", JSON.stringify(this.response, null, 2));
          this.router.navigate(['/response'], { state: { responseData: res } }).then();
        } else {
          console.error("Unexpected response from server:", res);
          alert("Submission failed. Please try again.");
        }
      },
      (err: any): void => {
        console.error("Error occurred:", err);
        alert("Server error. Please try again later.");
      }
    );
  }




}
