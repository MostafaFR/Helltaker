%% clingo -c h=24 -n0 .\helltaker_lvl4.lp

time(0..h-1).


init(hero(1,1)).
case(1,1).
key(3,1).
case(3,1).
init(getkey(0)).
case(4,1).
init(block(5,1)).
case(5,1).
case(1,2).
init(block(2,2)).
case(2,2).
spike(3,2).
case(3,2).
spike(4,2).
case(4,2).
init(block(4,2)).
case(5,2).
init(lock(6,2)).
case(6,2).
case(7,2).
init(block(1,3)).
case(1,3).
case(2,3).
init(block(3,3)).
case(3,3).
case(4,3).
init(block(5,3)).
case(5,3).
init(block(6,3)).
case(6,3).
case(7,3).
case(1,4).
init(block(2,4)).
case(2,4).
case(3,4).
init(block(4,4)).
case(4,4).
case(5,4).
init(block(6,4)).
case(6,4).
init(block(7,4)).
case(7,4).
case(8,4).
case(2,5).
init(block(3,5)).
case(3,5).
case(4,5).
init(block(5,5)).
case(5,5).
case(6,5).


%%les actions :
direction(
  left;
  right;
  up;
  down;
  push_right_block;
  push_left_block;
  push_up_block;
  push_down_block;
  push_right_mob;
  push_left_mob;
  push_up_mob;
  push_down_mob;
  nop
).

fluent(F,0) :- init(F).
% goals
goal(hero(7,3)).

%les goals sont heroteint au pas h
:- goal(F),not fluent(F,h).

%%% générateur d'actions..
{ action(A,T): direction(A) } = 1 :- time(T).


%%%les actions
%%action left
%précondition

:- action(left,T),
  fluent(hero(X,Y),T),
  fluent(block(X-1,Y),T).

:- action(left,T),
  fluent(hero(X,Y),T),
  fluent(mob(X-1,Y),T).

:-action(left,T),
  fluent(hero(X,Y),T),
  not case(X-1,Y).

:-action(left,T),
  fluent(hero(X,Y),T),
  fluent(lock(X-1,Y),T),
  not fluent(getkey(1),T).

:-action(left,T),
  fluent(hero(X,Y),T),
  fluent(lock(X-1,Y),T),
  fluent(getkey(0),T).

%Effets
fluent(hero(X-1,Y),T +1) :-
    action(left,T),
    fluent(hero(X,Y),T).

fluent(hero(X-1,Y),T+1):-
    action(left,T),
    fluent(lock(X-1,Y),T),
    fluent(getkey(1),T),
    fluent(hero(X,Y),T).

fluent(getkey(1), T+1) :-
    action(left, T),
    fluent(hero(X,Y), T),
    key(X-1,Y).

removed(lock(X-1,Y),T +1) :-
    action(left,T),
    fluent(hero(X,Y),T),
    fluent(getkey(1),T).

removed(hero(X,Y),T) :-
    action(left,T),
    fluent(hero(X,Y),T).


%%action right
%préconditions

:- action(right,T),
    fluent(hero(X,Y),T),
    fluent(mob(X+1,Y),T).

:- action(right,T),
    fluent(hero(X,Y),T),
    fluent(block(X+1,Y),T).

:- action(right,T),
    fluent(hero(X,Y),T),
    not case(X+1,Y).

:-action(right,T),
  fluent(hero(X,Y),T),
  fluent(lock(X+1,Y),T),
  not fluent(getkey(1),T).

:-action(right,T),
  fluent(hero(X,Y),T),
  fluent(lock(X+1,Y),T),
  fluent(getkey(0),T).

%Effets
fluent(hero(X+1,Y),T+1) :-
    action(right,T),
    fluent(hero(X,Y),T).

fluent(getkey(1), T+1) :-
    action(right, T),
    fluent(hero(X,Y), T),
    key(X+1,Y).

fluent(hero(X+1,Y),T+1):-
    action(right,T),
    fluent(lock(X+1,Y),T),
    fluent(getkey(1),T),
    fluent(hero(X,Y),T).

removed(lock(X+1,Y),T +1) :-
    action(right,T),
    fluent(hero(X,Y),T),
    fluent(getkey(1),T).

removed(hero(X,Y),T) :-
    action(right,T),
    fluent(hero(X,Y),T).

%%action up
%préconditions
:-  action(up,T),
    fluent(hero(X,Y),T),
    fluent(block(X,Y-1),T).

:-  action(up,T),
    fluent(hero(X,Y),T),
    fluent(mob(X,Y-1),T).

:-action(up,T),
  fluent(hero(X,Y),T),
  fluent(lock(X,Y-1),T),
  not fluent(getkey(1),T).

:-action(up,T),
  fluent(hero(X,Y),T),
  fluent(lock(X,Y-1),T),
  fluent(getkey(0),T).

:- action(up,T),
   fluent(hero(X,Y),T),
   not case(X,Y-1).

%Effets
fluent(hero(X,Y-1),T +1) :-
    action(up,T),
    fluent(hero(X,Y),T).

fluent(hero(X,Y-1),T+1):-
    action(up,T),
    fluent(lock(X,Y-1),T),
    fluent(getkey(1),T),
    fluent(hero(X,Y),T).

fluent(getkey(1), T+1) :-
    action(up, T),
    fluent(hero(X,Y), T),
    key(X,Y-1).

removed(lock(X,Y-1),T +1) :-
    action(up,T),
    fluent(hero(X,Y),T),
    fluent(getkey(1),T).

removed(hero(X,Y),T) :-
    action(up,T),
    fluent(hero(X,Y),T).

%%action down
%préconditions
:-  action(down,T),
    fluent(hero(X,Y),T),
    fluent(block(X,Y+1),T).

:-  action(down,T),
    fluent(hero(X,Y),T),
    fluent(mob(X,Y+1),T).

:-action(down,T),
  fluent(hero(X,Y),T),
  fluent(lock(X,Y+1),T),
  not fluent(getkey(1),T).

:-action(down,T),
  fluent(hero(X,Y),T),
  fluent(lock(X,Y+1),T),
  fluent(getkey(0),T).

:- action(down,T),
   fluent(hero(X,Y),T),
   not case(X,Y+1).

%Effets
fluent(hero(X,Y+1),T +1) :-
    action(down,T),
    fluent(hero(X,Y),T).

fluent(hero(X,Y+1),T+1):-
    action(down,T),
    fluent(lock(X,Y+1),T),
    fluent(getkey(1),T),
    fluent(hero(X,Y),T).

fluent(getkey(1), T+1) :-
    action(down, T),
    fluent(hero(X,Y), T),
    key(X,Y+1).

removed(lock(X,Y+1),T +1) :-
    action(down,T),
    fluent(hero(X,Y),T),
    fluent(getkey(1),T).

removed(hero(X,Y),T) :-
    action(down,T),
    fluent(hero(X,Y),T).

%%action push_right_block
% préconditions
:-  action(push_right_block,T),
    fluent(hero(X,Y),T),
    not fluent(block(X+1,Y),T).

:-  action(push_right_block,T),
    fluent(hero(X,Y),T),
    fluent(block(X+2,Y),T).

:-  action(push_right_block,T),
    fluent(hero(X,Y),T),
    fluent(lock(X+2,Y),T).

:-  action(push_right_block,T),
    fluent(hero(X,Y),T),
    fluent(mob(X+2,Y),T).

:-  action(push_right_block,T),
    fluent(hero(X,Y),T),
    not case(X+2,Y).


% effets

fluent(block(X+2,Y),T +1) :-
    action(push_right_block,T),
    fluent(hero(X,Y),T).

removed(block(X+1,Y),T) :-
    action(push_right_block,T),
    fluent(hero(X,Y),T).

%%action push_left_block
%préconditions
:-  action(push_left_block,T),
    fluent(hero(X,Y),T),
    not fluent(block(X-1,Y),T).

:-  action(push_left_block,T),
    fluent(hero(X,Y),T),
    fluent(mob(X-2,Y),T).

:-  action(push_left_block,T),
    fluent(hero(X,Y),T),
    fluent(block(X-2,Y),T).

:-  action(push_left_block,T),
    fluent(hero(X,Y),T),
    fluent(lock(X-2,Y),T).

:-  action(push_left_block,T),
    fluent(hero(X,Y),T),
    not case(X-2,Y).


% effets

fluent(block(X-2,Y),T +1) :-
    action(push_left_block,T),
    fluent(hero(X,Y),T).

removed(block(X-1,Y),T) :-
    action(push_left_block,T),
    fluent(hero(X,Y),T).

%%action push_down_block
%préconditions
:-  action(push_down_block,T),
    fluent(hero(X,Y),T),
    not fluent(block(X,Y+1),T).

:-  action(push_down_block,T),
    fluent(hero(X,Y),T),
    not case(X,Y+2).

:-  action(push_down_block,T),
    fluent(hero(X,Y),T),
    fluent(mob(X,Y+2),T).

:-  action(push_down_block,T),
    fluent(hero(X,Y),T),
    fluent(lock(X,Y+2),T).

:-  action(push_down_block,T),
    fluent(hero(X,Y),T),
    fluent(block(X,Y+2),T).

% effets

fluent(block(X,Y+2),T +1) :-
    action(push_down_block,T),
    fluent(hero(X,Y),T).

removed(block(X,Y+1),T) :-
    action(push_down_block,T),
    fluent(hero(X,Y),T).


%%action push_up_block
%préconditions
:-  action(push_up_block,T),
    fluent(hero(X,Y),T),
    not fluent(block(X,Y-1),T).

:-  action(push_up_block,T),
    fluent(hero(X,Y),T),
    not case(X,Y-2).

:-  action(push_up_block,T),
    fluent(hero(X,Y),T),
    fluent(mob(X,Y-2),T).

:-  action(push_up_block,T),
    fluent(hero(X,Y),T),
    fluent(lock(X,Y-2),T).

:-  action(push_up_block,T),
    fluent(hero(X,Y),T),
    fluent(block(X,Y-2),T).

% effets

fluent(block(X,Y-2),T +1) :-
    action(push_up_block,T),
    fluent(hero(X,Y),T).

removed(block(X,Y-1),T) :-
    action(push_up_block,T),
    fluent(hero(X,Y),T).


%%action push_right_mob
%préconditions
:- action(push_right_mob,T),
    fluent(hero(X,Y),T),
    not fluent(mob(X+1,Y),T).


fluent(mob(X+2,Y),T +1) :-
    action(push_right_mob,T),
    fluent(hero(X,Y),T).

removed(mob(X+1,Y),T) :-
    action(push_right_mob,T),
    fluent(hero(X,Y),T).


%%action push_left_mob
:- action(push_left_mob,T),
    fluent(hero(X,Y),T),
    not fluent(mob(X-1,Y),T).


fluent(mob(X-2,Y),T +1) :-
    action(push_left_mob,T),
    fluent(hero(X,Y),T).

removed(mob(X-1,Y),T) :-
    action(push_left_mob,T),
    fluent(hero(X,Y),T).


%%action push_down_mob
:- action(push_down_mob,T),
    fluent(hero(X,Y),T),
    not fluent(mob(X,Y+1),T).

fluent(mob(X,Y+2),T +1) :-
    action(push_down_mob,T),
    fluent(hero(X,Y),T).

removed(mob(X,Y+1),T) :-
    action(push_down_mob,T),
    fluent(hero(X,Y),T).

%%action push_up_mob

:- action(push_up_mob,T),
    fluent(hero(X,Y),T),
    not fluent(mob(X,Y-1),T).


fluent(mob(X,Y-2),T +1) :-
    action(push_up_mob,T),
    fluent(hero(X,Y),T).

removed(mob(X,Y-1),T) :-
    action(push_up_mob,T),
    fluent(hero(X,Y),T).

%%%%%%%%action nop %%%%%%%%%%%%
% préconditions
:-  action(nop,T),
    fluent(hero(X,Y),T),
    not spike(X,Y).

:- action(up, T),
    fluent(hero(X, Y), T),
    spike(X , Y- 1),
    not action(nop, T + 1).
:- action(down, T),
    fluent(hero(X, Y), T),
    spike(X , Y+ 1),
    not action(nop, T + 1).
:- action(left, T),
    fluent(hero(X, Y), T),
    spike(X- 1, Y ),
    not action(nop, T + 1).
:- action(right, T),
    fluent(hero(X, Y), T),
    spike(X+ 1, Y ),
    not action(nop, T + 1).

:- action(push_up_mob, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_down_mob, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_left_mob, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_right_mob, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).

:- action(push_up_block, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_down_block, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_left_block, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).
:- action(push_right_block, T),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T + 1).

% effets
fluent(hero(X,Y),T) :-
    action(nop,T),
    spike(X,Y),
    fluent(hero(X,Y),T).

%%key et lock %%

removed(getkey(0),T):-
    fluent(getkey(1),T).

%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F,T +1) :-
    fluent(F,T),
    T +1 <= h,
    not removed(F,T).    
#show action/2.