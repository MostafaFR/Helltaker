import sys
import clingo

import helltaker_utils as helltaker_utils
filename = sys.argv

plan = helltaker_utils.grid_from_file(filename)


def on_model(m):
    print (m)

Tab = ""
for i in range(len(plan["grid"])):
    for j in range(len(plan["grid"][i])):
        if plan["grid"][i][j] == ' ':
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'D':
            Tab =+ "goal(hero("+j+","+i+"))."
        if plan["grid"][i][j] == 'H':
            Tab =+ "init(hero("+j+","+i+"))."
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'K':
            Tab =+ "key("+j+","+i+")."
            Tab =+ "case("+j+","+i+")."
            Tab =+ "init(getkey(0))."
        if plan["grid"][i][j] == 'L':
            Tab =+ "init(lock("+j+","+i+"))."
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'M':
            Tab =+ "init(mob("+j+","+i+"))."
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'B':
            Tab =+ "init(block("+j+","+i+"))."
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'S':
            Tab =+ "spike("+j+","+i+")."
            Tab =+ "case("+j+","+i+")."
        if plan["grid"][i][j] == 'O':
            Tab =+ "spike("+j+","+i+")."
            Tab =+ "case("+j+","+i+")."
            Tab =+ "init(block("+j+","+i+"))."

N=plan["max_steps"]
pb = (
    f"#const h={N}.\n"
    + Tab
    + """\
time(0..h-1).
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
:- goal(F),not fluent(F,h).
{ action(A,T): direction(A) } = 1 :- time(T).

%%action left
%préconditions
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

%%action nop
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

%%key

removed(getkey(0),T):-
    fluent(getkey(1),T).

%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F,T +1) :-
    fluent(F,T),
    T +1 <= h,
    not removed(F,T).    
#show action/2.
"""
)
ctl = clingo.Control(["-n 0"])
ctl.add("base", [], pb)

ctl.ground([("base", [])])

ctl.solve(on_model=on_model)