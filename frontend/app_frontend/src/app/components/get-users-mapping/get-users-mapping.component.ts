import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {UserModel} from '../../../models/user.model';
import {NgbModal, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import {UpdateUserComponent} from '../update-user/update-user.component';
import {DeleteUserComponent} from '../delete-user/delete-user.component';
import {Router} from '@angular/router';
import {ShowUserComponent} from '../show-user/show-user.component';

@Component({
  selector: 'app-get-users-mapping',
  standalone: false,
  templateUrl: './get-users-mapping.component.html',
  styleUrl: './get-users-mapping.component.css'
})
export class GetUsersMappingComponent implements OnInit{

  users!: UserModel[];

  constructor(private apiService: ApiService,
              private modalService: NgbModal,
              private router: Router) {
  }

  ngOnInit(): void {
    this.fetchAllUsers();
  }

  private fetchAllUsers(){
    this.apiService.getAllData().subscribe({
      next: (res: any) => {
        this.users = res;
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

  onUpdate(user:UserModel){
    const modalReference: NgbModalRef = this.modalService.open(UpdateUserComponent, {"backdrop": "static"});
    modalReference.componentInstance.user = user;
    console.info("user to be updated: ", user);
    modalReference.componentInstance.updateUser.subscribe((isDone: boolean): any => {
      console.info("isDone: ", isDone);
      if(isDone){
        this.fetchAllUsers();
      }else{
        alert("Unable to update the user")
      }
      modalReference.close();
    });
  }

  onDelete(id: string){
    const modalReference: NgbModalRef = this.modalService.open(DeleteUserComponent, { "backdrop" : "static" });
    console.info("id to be deleted: ", id);
    modalReference.componentInstance.userId = id;
    modalReference.componentInstance.deleteUser.subscribe((isDone: boolean): any => {
      console.info("isDone: ", isDone);
      if(isDone){
        this.fetchAllUsers();
      }else{
        alert("Unable to delete the user")
      }
      modalReference.close();
    });

  }

  onAdd() {
    console.info("add user function called");
    this.router.navigate(['/add']).then();
  }

  showUser(id: string) {
    const modalReference: NgbModalRef = this.modalService.open(ShowUserComponent,
      { "backdrop" : "static",
        "size" : "xl"
      });
    modalReference.componentInstance.userId = id;
  }
}
