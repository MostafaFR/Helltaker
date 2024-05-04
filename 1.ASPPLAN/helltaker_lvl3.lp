%% clingo -c h=32 -n0 helltaker_lvl3.lp

time(0..h-1).

%case(X,Y) :- ligne(X),col(Y).

case(7,1).
init(lock(7,2)).
case(7,2).
case(3,3).
spike(4,3).
case(4,3).
spike(5,3).
case(5,3).
case(6,3).
case(7,3).
init(hero(8,3)).
case(8,3).
spike(3,4).
case(3,4).
spike(5,4).
case(5,4).
case(7,4).
case(8,4).
case(3,5).
case(4,5).
init(mob(5,5)).
case(5,5).
spike(6,5).
case(6,5).
spike(7,5).
case(7,5).
key(1,6).
case(1,6).
init(getkey(0)).
spike(3,6).
case(3,6).
spike(5,6).
case(5,6).
case(7,6).
case(1,7).
case(2,7).
case(3,7).
case(4,7).
case(5,7).
init(mob(6,7)).
case(6,7).
case(7,7).

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

%les buts :
goal(hero(7,1)).

%les goals sont heroteint au pas h
:- goal(F),not fluent(F,h).

%%% générateur d'actions..
{ action(Act,T): direction(Act) } = 1 :- time(T).


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

%Effets
fluent(hero(X-1,Y),T +1) :-
    action(left,T),
    fluent(hero(X,Y),T).

fluent(hero(X-1,Y),T+1):-
    action(left,T),
    fluent(lock(X-1,Y),T),
    fluent(getkey(1),T),
    fluent(hero(X,Y),T).

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

%Effets
fluent(hero(X+1,Y),T+1) :-
    action(right,T),
    fluent(hero(X,Y),T).

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

:- action(A,T-1),
    A!=nop,
    fluent(hero(X1,Y1),T-1),
    fluent(hero(X,Y),T),
    spike(X,Y),
    not action(nop,T).

% effets
fluent(hero(X,Y),T) :-
    action(nop,T),
    spike(X,Y),
    fluent(hero(X,Y),T).

%%key et lock %%

removed(getkey(0),T):-
    fluent(getkey(1),T).

fluent(getkey(1), T) :-
    fluent(getkey(0), T-1),
    action(A, T-1),
    fluent(hero(X,Y), T),
    key(X,Y).

%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F,T +1) :-
    fluent(F,T),
    T +1 <= h,
    not removed(F,T).

#show action/2.