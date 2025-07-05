import {Component, EventEmitter, Input, Output} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {modalAnimation} from '../../animations/modal-animation';

@Component({
  selector: 'app-delete-user',
  standalone: false,
  templateUrl: './delete-user.component.html',
  styleUrl: './delete-user.component.css',
  animations: [modalAnimation]
})
export class DeleteUserComponent {

  @Input() userId!: string;
  @Output() deleteUser: EventEmitter<boolean> = new EventEmitter<boolean>();
  modal_title:string  = "Delete User";

  constructor(private apiService: ApiService, public activeModal: NgbActiveModal) { }

  onDelete(){
    this.apiService.deleteById(this.userId).subscribe({
      next: (res: any) => {
        console.log("response: ", JSON.stringify(res, null, 2));
        this.deleteUser.emit(true);
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
