import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';

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
      userName: ['', Validators.required],
      email: ['', Validators.required]
    });
  }

  onSubmit(): any {
    console.log("form data: ", this.formData);
    this.formData.username = this.loginForm.value.userName;
    this.formData.email = this.loginForm.value.email;
    console.log("form data: ", this.formData);
    this.apiService.submitData(this.formData).subscribe(
      (res: any): any => {
        this.response = res;
        console.log("response: ", JSON.stringify(this.response, null, 2));
        this.router.navigate(['/response'], { state: { responseData: res } }).then();
      },
      (err: any): any => console.error(err)
    );
  }
}
