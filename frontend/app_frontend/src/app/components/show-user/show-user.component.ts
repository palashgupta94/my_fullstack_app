import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {UserModel} from '../../../models/user.model';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {ApiService} from '../../services/api.service';
import {modalAnimation} from '../../animations/modal-animation';

@Component({
  selector: 'app-show-user',
  standalone: false,
  templateUrl: './show-user.component.html',
  styleUrl: './show-user.component.css',
  animations: [modalAnimation]
})
export class ShowUserComponent implements OnInit{

  userForm!: FormGroup;
  user!: UserModel;
  @Input() userId!: string;

  modal_title:string  = "Show User";

  constructor(private apiService: ApiService, public activeModal: NgbActiveModal ) { }

  ngOnInit(): void {
    console.log("userId: ", this.userId);

    this.apiService.getById(this.userId).subscribe({
      next: (res: any) => {
        this.user = res;
        console.log("response: ", JSON.stringify(res, null, 2));
        console.log("user: ", this.user);

        this.userForm = new FormGroup({
          id: new FormControl(this.user?.id|| ""), //hidden field
          username: new FormControl(this.user?.username || "", [Validators.required]),
          email: new FormControl(this.user?.email || "", [Validators.required, Validators.email]),
          firstName: new FormControl(this.user?.firstName || "", [Validators.required]),
          lastName: new FormControl(this.user?.lastName || "", [Validators.required]),
          dateOfBirth: new FormControl(this.user?.dateOfBirth || "", [Validators.required]),
          createdAt: new FormControl(this.user?.createdAt || "", [Validators.required]),
          updatedAt: new FormControl(this.user?.updatedAt || "", [Validators.required]),
          gender: new FormControl(this.user?.gender || "", [Validators.required])
        });

        console.info("userForm: ", this.userForm);

      },
      error: (err: any) => {
        console.error(err);
      },
      complete: (): void => {
        console.info('done');
      },
      status: (): void => {
        console.info('status');
      }
    });

  }

}
