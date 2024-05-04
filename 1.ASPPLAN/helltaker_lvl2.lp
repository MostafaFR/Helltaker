%% clingo -n0 helltaker_lvl2.lp -c h=24

time(0..h-1).

%case(X,Y) = ligne(X) colonne(Y).
case(2,1).
case(3,1).
case(4,1).
case(5,1).
init(mob(2,2)).
case(2,2).
spike(4,2).
case(4,2).
spike(5,2).
case(5,2).
case(6,2).
case(7,2).
case(1,3).
spike(2,3).
case(2,3).
spike(5,3).
case(5,3).
init(block(5,3)).
spike(6,3).
case(6,3).
init(block(6,3)).
init(block(7,3)).
case(7,3).
case(1,4).
case(2,4).
case(5,4).
spike(6,4).
case(6,4).
case(7,4).
init(hero(1,5)).
case(1,5).
case(2,5).
case(5,5).
init(mob(6,5)).
case(6,5).
case(7,5).
case(6,6).
init(mob(7,6)).
case(7,6).


%%les directions :
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

fluent(F, 0) :- init(F).

goal(hero(5,5));
goal(hero(6,6)).

%les goals sont atteint au pas h
:- goal(F), not fluent(F, h).

%%% générateur d'actions..
{ action(Act, T): direction(Act) } = 1 :- time(T).


%%%les actions

%%action nop
% préconditions
:-  action(nop, T),
    fluent(hero(X, Y), T),
    not spike(X, Y).

:- action(A, T-1),
    A!=nop, 
    fluent(hero(X1, Y1), T-1),
    fluent(hero(X, Y), T),
    spike(X, Y),
    not action(nop, T).
    
% effets
fluent(hero(X, Y), T) :-
    action(nop, T),
    spike(X, Y),
    fluent(hero(X, Y), T).


%%action left
%précondition

:- action(left,T),
  fluent(hero(X,Y),T),
  fluent(block(X-1,Y),T).

:- action(left, T),
  fluent(hero(X, Y), T),
  fluent(mob(X-1, Y), T).

:-action(left,T),
  fluent(hero(X,Y), T),
  not case(X-1, Y).

%Effets
fluent(hero(X-1, Y), T + 1) :-
    action(left, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(left, T),
    fluent(hero(X, Y), T).

%%action right
%préconditions

:-  action(right, T),
    fluent(hero(X, Y), T),
    fluent(mob(X+1, Y), T).

:-  action(right, T),
    fluent(hero(X, Y), T),
    fluent(block(X+1, Y), T).

:-action(right,T),
  fluent(hero(X,Y), T),
  not case(X+1, Y).

%Effets
fluent(hero(X+1, Y), T + 1) :-
    action(right, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(right, T),
    fluent(hero(X, Y), T).

%%action up
%préconditions
:-  action(up, T),
    fluent(hero(X, Y), T),
    fluent(block(X, Y-1), T).

:-  action(up, T),
    fluent(hero(X, Y), T),
    fluent(mob(X, Y-1), T).

:- action(up,T),
   fluent(hero(X,Y), T),
   not case(X, Y-1).

%Effets
fluent(hero(X, Y-1), T + 1) :-
    action(up, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(up, T),
    fluent(hero(X, Y), T).

%%action down
%préconditions
:-  action(down, T),
    fluent(hero(X, Y), T),
    fluent(block(X, Y+1), T).

:-  action(down, T),
    fluent(hero(X, Y), T),
    fluent(mob(X, Y+1), T).

:- action(down,T),
   fluent(hero(X,Y), T),
   not case(X, Y+1).

%Effets
fluent(hero(X, Y+1), T + 1) :-
    action(down, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(down, T),
    fluent(hero(X, Y), T).

%%action push_right_block
% préconditions
:-  action(push_right_block, T),
    fluent(hero(X, Y), T),
    not fluent(block(X+1, Y), T).

:-  action(push_right_block, T),
    fluent(hero(X, Y), T),
    fluent(block(X+2, Y), T).

:-  action(push_right_block, T),
    fluent(hero(X, Y), T),
    fluent(mob(X+2, Y), T).

:-  action(push_right_block, T),
    fluent(hero(X, Y), T),
    not case(X+2, Y).


% effets

fluent(block(X+2, Y), T + 1) :-
    action(push_right_block, T),
    fluent(hero(X, Y), T).

del(block(X+1, Y), T) :-
    action(push_right_block, T),
    fluent(hero(X, Y), T).

%%action push_left_block
%préconditions
:-  action(push_left_block, T),
    fluent(hero(X, Y), T),
    not fluent(block(X-1, Y), T).

:-  action(push_left_block, T),
    fluent(hero(X, Y), T),
    fluent(mob(X-2, Y), T).

:-  action(push_left_block, T),
    fluent(hero(X, Y), T),
    fluent(block(X-2, Y), T).

:-  action(push_left_block, T),
    fluent(hero(X, Y), T),
    not case(X-2, Y).


% effets

fluent(block(X-2, Y), T + 1) :-
    action(push_left_block, T),
    fluent(hero(X, Y), T).

del(block(X-1, Y), T) :-
    action(push_left_block, T),
    fluent(hero(X, Y), T).

%%action push_down_block
%préconditions
:-  action(push_down_block, T),
    fluent(hero(X, Y), T),
    not fluent(block(X, Y+1), T).

:-  action(push_down_block, T),
    fluent(hero(X, Y), T),
    not case(X, Y+2).

:-  action(push_down_block, T),
    fluent(hero(X, Y), T),
    fluent(mob(X, Y+2), T).

:-  action(push_down_block, T),
    fluent(hero(X, Y), T),
    fluent(block(X, Y+2), T).

% effets

fluent(block(X, Y+2), T + 1) :-
    action(push_down_block, T),
    fluent(hero(X, Y), T).

del(block(X, Y+1), T) :-
    action(push_down_block, T),
    fluent(hero(X, Y), T).


%%action push_up_block
%préconditions
:-  action(push_up_block, T),
    fluent(hero(X, Y), T),
    not fluent(block(X, Y-1), T).

:-  action(push_up_block, T),
    fluent(hero(X, Y), T),
    not case(X, Y-2).

:-  action(push_up_block, T),
    fluent(hero(X, Y), T),
    fluent(mob(X, Y-2), T).

:-  action(push_up_block, T),
    fluent(hero(X, Y), T),
    fluent(block(X, Y-2), T).

% effets

fluent(block(X, Y-2), T + 1) :-
    action(push_up_block, T),
    fluent(hero(X, Y), T).

del(block(X, Y-1), T) :-
    action(push_up_block, T),
    fluent(hero(X, Y), T).


%%action push_right_mob
%préconditions
:- action(push_right_mob, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X+1, Y), T).


fluent(mob(X+2, Y), T + 1) :-
    action(push_right_mob, T),
    fluent(hero(X, Y), T).

del(mob(X+1, Y), T) :-
    action(push_right_mob, T),
    fluent(hero(X, Y), T).


%%action push_left_mob
:- action(push_left_mob, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X-1, Y), T).


fluent(mob(X-2, Y), T + 1) :-
    action(push_left_mob, T),
    fluent(hero(X, Y), T).

del(mob(X-1, Y), T) :-
    action(push_left_mob, T),
    fluent(hero(X, Y), T).


%%action push_down_mob
:- action(push_down_mob, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X, Y+1), T).

fluent(mob(X, Y+2), T + 1) :-
    action(push_down_mob, T),
    fluent(hero(X, Y), T).

del(mob(X, Y+1), T) :-
    action(push_down_mob, T),
    fluent(hero(X, Y), T).

%%action push_up_mob

:- action(push_up_mob, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X, Y-1), T).


fluent(mob(X, Y-2), T + 1) :-
    action(push_up_mob, T),
    fluent(hero(X, Y), T).

del(mob(X, Y-1), T) :-
    action(push_up_mob, T),
    fluent(hero(X, Y), T).

%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F, T + 1) :-
    fluent(F, T),
    T + 1 <= h,
    not del(F, T).

#show action/2.

