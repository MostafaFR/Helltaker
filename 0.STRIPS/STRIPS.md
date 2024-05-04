# Modelisation Helltaker STRIPS


NB: Les 2 premiers arguments x et y représentent les coordonnées, et le z un état actif si 1, et 0 si inactif.
Pour le "hero" l'état z est pour la détention d'une clé et pour "lock" si le cadena est verrouillé ou non.
Le z du "spike_dynamic" est actif si les piques sont sorties.

## Definition des termes utilisés
```
Fluents:  hero(x,y,z), mob(x,y), block(x,y), spike_dynamic(x,y,z), lock(x,y), time(t)
No Fluents: wall(x,y), goal(x,y), spike_static(x,y), key(x,y)


Etat initial: Spécifique au level
Etat final (goal) : hero(x,y,z) ∧ goal(x,y) ∧ time(t) ∧ (t!=0)


Successeur : succ(x1,x2) //Le successeur de la coordonnées x1 est x2
Suppression : clear(x) //Supprime l'élément x
```

## Directions :
```
Action(Direction_Up(x1,y1)):
    Préconditions : hero(x1,y1,0) ∧ ¬wall(x1,y2) ∧ ¬block(x1,y2) ∧ ¬mob(x1,y2) ∧ ¬lock(x1,y2) ∧ succ(y1,y2)  
    Effets : hero(x1,y2,0) ∧ time(t--) ∧ clear(hero(x1,y1,0))

Action(Direction_Down(x1,y1)):
    Préconditions : hero(x1,y1,0) ∧ ¬wall(x1,y2) ∧ ¬block(x1,y2) ∧ ¬mob(x1,y2) ∧ ¬lock(x1,y2) ∧ succ(y1,y2)   
    Effets : hero(x1,y2,0) ∧ time(t--) ∧ clear(hero(x1,y1,0))

Action(Direction_Left(x1,y1)):
    Préconditions : hero(x1,y1,0) ∧ ¬wall(x2,y1) ∧ ¬block(x2,y1) ∧ ¬mob(x2,y1) ∧ ¬lock(x2,y1) ∧ succ(x1,x2)  
    Effets : hero(x2,y1,0) ∧ time(t--) ∧ clear(hero(x1,y1,0))

Action(Direction_Right(x1,y1)):
    Préconditions : hero(x1,y1,0) ∧ ¬wall(x2,y1) ∧ ¬block(x2,y1) ∧ ¬mob(x2,y1) ∧ ¬lock(x2,y1) ∧ succ(x1,x2)   
    Effets : hero(x2,y1,0) ∧ time(t--) ∧ clear(hero(x1,y1,0))


## Déplacement block:

Action(Push_up_block(x1,y1)):
    Préconditions : hero(x1,y1,z) ∧ block(x1,y2) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ¬wall(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets : block(x1,y3) ∧ clear(block(x1,y2)) ∧ time(t--)

Action(Push_down_block(x1,y1)):
    Préconditions : hero(x1,y1,z) ∧ block(x1,y2) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ∧ ¬wall(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets : block(x1,y3) ∧ clear(block(x1,y2)) ∧ time(t--)

Action(Push_left_block(x1,y1)):
    Préconditions : hero(x1,y1,z) ∧ block(x2,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ ¬wall(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets : block(x3,y1) ∧ clear(block(x2,y1)) ∧ time(t--)

Action(Push_right_block(x1,y1)):
    Préconditions : hero(x1,y1,z) ∧ block(x2,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ ¬wall(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets : block(x3,y1) ∧ clear(block(x2,y1)) ∧ time(t--)
```

## Déplacement mob :
```
Action(Push_up_mob(x1,y1)):
    Préconditions 1 : hero(x1,y1,z) ∧ mob(x1,y2) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets 1: mob(x1,y3) ∧ clear(mob(x1,y2)) ∧ time(t--)

    //Si mur présent au dessus du mob
    Préconditions 2 : hero(x1,y1,z) ∧ mob(x1,y2) ∧  wall(x1,y3) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets 2 : clear(mob(x1,y2) ∧ time(t--))

Action(Push_down_mob(x1,y1)):
    Préconditions 1 : hero(x1,y1,z) ∧ mob(x1,y2) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets 1: mob(x1,y3) ∧ clear(mob(x1,y2)) ∧ time(t--)

    //Si mur présent en dessous du mob
    Préconditions 2 : hero(x1,y1,z) ∧ mob(x1,y2) ∧  wall(x1,y3) ∧ ¬lock(x1,y3) ∧ ¬mob(x1,y3) ∧ ¬block(x1,y3) ∧ succ(y1,y2) ∧ succ(y2,y3)
    Effets 2 : clear(mob(x1,y2) ∧ time(t--))

Action(Push_left_mob(x1,y1)):
    Préconditions 1 : hero(x1,y1,z) ∧ mob(x2,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets 1: mob(x3,y1) ∧ clear(mob(x2,y1)) ∧ time(t--)

    //Si mur présent à gauche du mob
    Préconditions 2 : hero(x1,y1,z) ∧ mob(x2,y1) ∧  wall(x3,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets 2 : clear(mob(x2,y1) ∧ time(t--))

Action(Push_right_mob(x1,y1)):
    Préconditions 1 : hero(x1,y1,z) ∧ mob(x2,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets 1: mob(x3,y1) ∧ clear(mob(x2,y1)) ∧ time(t--)

    //Si mur présent à droite du mob
    Préconditions 2 : hero(x1,y1,z) ∧ mob(x2,y1) ∧  wall(x3,y1) ∧ ¬lock(x3,y1) ∧ ¬mob(x3,y1) ∧ ¬block(x3,y1) ∧ succ(x1,x2) ∧ succ(x2,x3)
    Effets 2 : clear(mob(x2,y1) ∧ time(t--))
```

## Récupérer la clé :
```
Action(take_key_up(x1,y1):
    Préconditions : hero(x1,y1,0) ∧ key(x1,y2) ∧ succ(y1,y2) 
    Effets : hero(x1,y2,1) ∧ clear(key(x1,y2)) ∧ time(t--))

Action(take_key_down(x1,y1):
    Préconditions : hero(x1,y1,0) ∧ key(x1,y2) ∧ succ(y1,y2) 
    Effets : hero(x1,y2,1) ∧ clear(key(x1,y2)) ∧ time(t--))

Action(take_key_left(x1,y1):
    Préconditions : hero(x1,y1,0) ∧ key(x2,y1) ∧ succ(x1,x2) 
    Effets : hero(x2,y1,1) ∧ clear(key(x2,y1)) ∧ time(t--))

Action(take_key_right(x1,y1):
    Préconditions : hero(x1,y1,0) ∧ key(x2,y1) ∧ succ(x1,x2) 
    Effets : hero(x2,y1,1) ∧ clear(key(x2,y1)) ∧ time(t--))
```

## Déplacement sur piques:
```
Action(Move_Up_spike(x1,y1),
    Préconditions : hero(x1,y1,z) ∧ succ(y1,y2) ∧ ¬block(x1,y2) ∧ (spike_static(x1,y2) v spike_dynamic(x1,y2,1))
    Effets : hero(x1,y2,z) ∧ clear(hero(x1,y1,z)) ∧ time(t-2))

Action(Move_Down_spike(x1,y1),
    Préconditions : hero(x1,y1,z) ∧ succ(y1,y2) ∧ ¬block(x1,y2) ∧ (spike_static(x1,y2) v spike_dynamic(x1,y2,1))
    Effets : hero(x1,y2,z) ∧ clear(hero(x1,y1,z)) ∧ time(t-2))

Action(Move_Left_spike(x1,y1),
    Préconditions : hero(x1,y1,z) ∧ ¬block(x2,y1) ∧ (spike_static(x2,y1) v spike_dynamic(x2,y1,1)) ∧ succ(x1,x2) 
    Effets : hero(x2,y1,z) ∧ clear(hero(x1,y1,z)) ∧ time(t-2))

Action(Move_Right_spike(x1,y1),
    Préconditions : hero(x1,y1,z) ∧ ¬block(x2,y1) ∧ (spike_static(x2,y1) v spike_dynamic(x2,y1,1)) ∧ succ(x1,x2) 
    Effets : hero(x2,y1,z) ∧ clear(hero(x1,y1,z)) ∧ time(t-2))
```