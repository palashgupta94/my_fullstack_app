import {animate, AnimationTriggerMetadata, style, transition, trigger} from '@angular/animations';


export const modalAnimation: AnimationTriggerMetadata = trigger('modalAnimation', [
  transition(':enter', [
    style({transform: 'translateY(-100%)', opacity: 0}),
    animate('300ms ease-out', style({transform: 'translateY(0)', opacity: 1}))
  ]),
  transition(':leave', [
    animate('300ms ease-in', style({transform: 'translateY(-100%)', opacity: 0}))
  ])
]);
