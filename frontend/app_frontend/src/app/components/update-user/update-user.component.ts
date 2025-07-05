import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {UserModel} from '../../../models/user.model';
import {ApiService} from '../../services/api.service';
import {modalAnimation} from '../../animations/modal-animation';
import {getISTISOString} from '../../utility/date-converter.utility';

@Component({
  selector: 'app-update-user',
  standalone: false,
  templateUrl: './update-user.component.html',
  styleUrl: './update-user.component.css',
  animations: [modalAnimation]
})
export class UpdateUserComponent implements OnInit {

  userForm!: FormGroup;
  @Output() updateUser: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Input() user!: UserModel;

  modal_title: string = "Update User";

  constructor(private apiService: ApiService, public activeModal: NgbActiveModal) {
  }

  ngOnInit(): void {
    this.userForm = new FormGroup({
      id: new FormControl(this.user?.id || ""), //hidden field
      firstName: new FormControl(this.user?.firstName || "", [Validators.required]),
      lastName: new FormControl(this.user?.lastName || "", [Validators.required]),
      username: new FormControl(this.user?.username || "", [Validators.required]),
      email: new FormControl(this.user?.email || "", [Validators.required, Validators.email]),
      gender: new FormControl(this.user?.gender || "", [Validators.required]),
      createdAt: new FormControl(new Date().toISOString()),
      updatedAt: new FormControl(getISTISOString())
    });
  }

  onUpdate() {
    console.log("onUpdate method called");
    if (this.userForm.valid) {
      this.apiService.putById(this.userForm.value.id, this.userForm.value)
        .subscribe({
          next: (res: any) => {
            console.log("response: ", JSON.stringify(res, null, 2));
            this.updateUser.emit(true);
          },
          error: (err: any) => {
            console.error(false);
          },
          complete: (): void => {
            console.info('done');
          }
        });
    }
  }
}
