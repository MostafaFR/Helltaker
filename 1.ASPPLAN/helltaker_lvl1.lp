%% clingo -n0 helltaker_lvl1.lp -c h=23

time(0..h-1).

%case(X, Y) = ligne(X) colonne(Y).
case(5,1).
case(6,1).
case(2,2).
case(3,2).
case(4,2).
case(5,2).
case(6,2).
case(2,3).
case(3,3).
case(4,3).
case(5,3).
case(1,4).
case(2,4).
case(1,5).
case(2,5).
case(3,5).
case(4,5).
case(5,5).
case(6,5).
case(1,6).
case(2,6).
case(3,6).
case(4,6).
case(5,6).
case(6,6).

%%les directions :
direction(
  left;
  right;
  up;
  down;
  push_right_p;
  push_left_p;
  push_up_p;
  push_down_p;
  push_right_d;
  push_left_d;
  push_up_d;
  push_down_d
).

%initialisation :
init(hero(6,1)).
init(mob(4,2)).
init(mob(3,3)).
init(mob(5,3)).
init(block(2,5)).
init(block(5,5)).
init(block(2,6)).
init(block(4,6)).



fluent(F, 0) :- init(F).

%les buts :
goal(hero(6,6)).

%les goals sont atteint au pas h
:- goal(F), not fluent(F, h).

%%% générateur d'directions..
{ action(A, T): direction(A) } = 1 :- time(T).


%%%les directions

%%direction left
%précondition
:- action(left,T),
    fluent(hero(X, Y),T),
    fluent(block(X-1,Y),T).

:- action(left, T),
    fluent(hero(X, Y), T),
    fluent(mob(X-1,Y), T).

:-action(left,T),
    fluent(hero(X, Y), T),
    not case(X-1,Y).

%Effets
fluent(hero(X-1,Y), T+1) :-
    action(left, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(left, T),
    fluent(hero(X, Y), T).

%%direction right
%préconditions
:-  action(right, T),
    fluent(hero(X, Y), T),
    fluent(mob(X+1,Y), T).

:-  action(right, T),
    fluent(hero(X, Y), T),
    fluent(block(X+1,Y), T).

:-action(right,T),
    fluent(hero(X, Y), T),
    not case(X+1,Y).

%effets
fluent(hero(X+1,Y), T+1) :-
    action(right, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(right, T),
    fluent(hero(X, Y), T).

%%direction up
%préconditions
:-  action(up, T),
    fluent(hero(X, Y), T),
    fluent(block(X,Y-1), T).

:-  action(up, T),
    fluent(hero(X, Y), T),
    fluent(mob(X-1,Y), T).

:- action(up,T),
    fluent(hero(X, Y), T),
    not case(X,Y-1).

%Effets
fluent(hero(X,Y-1), T+1) :-
    action(up, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(up, T),
    fluent(hero(X, Y), T).

%%direction down
%préconditions
:-  action(down, T),
    fluent(hero(X, Y), T),
    fluent(block(X,Y+1), T).

:-  action(down, T),
    fluent(hero(X, Y), T),
    fluent(mob(X,Y+1), T).

:- action(down,T),
    fluent(hero(X, Y), T),
    not case(X,Y+1).

%effets
fluent(hero(X,Y+1), T+1) :-
    action(down, T),
    fluent(hero(X, Y), T).

del(hero(X, Y), T) :-
    action(down, T),
    fluent(hero(X, Y), T).

%%direction push_right_p
% préconditions
:-  action(push_right_p, T),
    fluent(hero(X, Y), T),
    not fluent(block(X+1,Y), T).

:-  action(push_right_p, T),
    fluent(hero(X, Y), T),
    fluent(block(X+2,Y), T).

:-  action(push_right_p, T),
    fluent(hero(X, Y), T),
    fluent(mob(X+2,Y), T).

:-  action(push_right_p, T),
    fluent(hero(X, Y), T),
    not case(X+2,Y).


% effets
fluent(block(X+2,Y), T+1) :-
    action(push_right_p, T),
    fluent(hero(X, Y), T).

del(block(X+1,Y), T) :-
    action(push_right_p, T),
    fluent(hero(X, Y), T).

%%direction push_left_p
%préconditions
:-  action(push_left_p, T),
    fluent(hero(X, Y), T),
    not fluent(block(X-1,Y), T).

:-  action(push_left_p, T),
    fluent(hero(X, Y), T),
    fluent(mob(X-2,Y), T).

:-  action(push_left_p, T),
    fluent(hero(X, Y), T),
    fluent(block(X-2,Y), T).

:-  action(push_left_p, T),
    fluent(hero(X, Y), T),
    not case(X-2,Y).


% effets
fluent(block(X-2,Y), T+1) :-
    action(push_left_p, T),
    fluent(hero(X, Y), T).

del(block(X-1,Y), T) :-
    action(push_left_p, T),
    fluent(hero(X, Y), T).

%%direction push_down_p
%préconditions
:-  action(push_down_p, T),
    fluent(hero(X, Y), T),
    not fluent(block(X,Y+1), T).

:-  action(push_down_p, T),
    fluent(hero(X, Y), T),
    not case(X,Y+2).

:-  action(push_down_p, T),
    fluent(hero(X, Y), T),
    fluent(mob(X,Y+2), T).

:-  action(push_down_p, T),
    fluent(hero(X, Y), T),
    fluent(block(X,Y+2), T).

% effets
fluent(block(X,Y+2), T+1) :-
    action(push_down_p, T),
    fluent(hero(X, Y), T).

del(block(X,Y+1), T) :-
    action(push_down_p, T),
    fluent(hero(X, Y), T).


%%direction push_up_p
%préconditions
:-  action(push_up_p, T),
    fluent(hero(X, Y), T),
    not fluent(block(X,Y-1), T).

:-  action(push_up_p, T),
    fluent(hero(X, Y), T),
    not case(X,Y-2).

:-  action(push_up_p, T),
    fluent(hero(X, Y), T),
    fluent(mob(X,Y-2), T).

:-  action(push_up_p, T),
    fluent(hero(X, Y), T),
    fluent(block(X,Y-2), T).

% effets
fluent(block(X,Y-2), T+1) :-
    action(push_up_p, T),
    fluent(hero(X, Y), T).

del(block(X,Y-1), T) :-
    action(push_up_p, T),
    fluent(hero(X, Y), T).


%%direction push_right_d
%préconditions
:- action(push_right_d, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X+1,Y), T).

% effets
fluent(mob(X+2,Y), T+1) :-
    action(push_right_d, T),
    fluent(hero(X, Y), T).

del(mob(X+1,Y), T) :-
    action(push_right_d, T),
    fluent(hero(X, Y), T).


%%direction push_left_d
%préconditions
:- action(push_left_d, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X-1,Y), T).

% effets
fluent(mob(X-2,Y), T+1) :-
    action(push_left_d, T),
    fluent(hero(X, Y), T).

del(mob(X-1,Y), T) :-
    action(push_left_d, T),
    fluent(hero(X, Y), T).


%%direction push_down_d
%préconditions
:- action(push_down_d, T),
    fluent(hero(X, Y), T),
    not fluent(mob(X,Y+1), T).

% effets
fluent(mob(X,Y+2), T+1) :-
    action(push_down_d, T),
    fluent(hero(X, Y), T).

del(mob(X,Y+1), T) :-
    action(push_down_d, T),
    fluent(hero(X, Y), T).

%%direction push_up_d
%préconditions
:- action(push_up_d, T),
    fluent(hero(X,Y-1), T),
    not fluent(mob(X,Y-1), T).

% effets
fluent(mob(X,Y-2), T+1) :-
    action(push_up_d, T),
    fluent(hero(X, Y), T).

del(mob(X,Y-1), T) :-
    action(push_up_d, T),
    fluent(hero(X, Y), T).


%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F, T+1) :- fluent(F, T), T+1 <= h, not del(F, T).

#show action/2.
