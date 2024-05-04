import itertools
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict, Union, Optional
from helltaker_utils import grid_from_file

StageData: dict
StepCoord = Tuple[int, int, int]


class Litteral:
    """
    Représente un littéral en logique propositionnel
    """

    nom: str
    signe: bool

    def __init__(self, nom_lit, signe_lit):
        self.nom = nom_lit
        self.signe = signe_lit

    def neg(self):
        """
        Renvoit un litteral négatif
        """
        return Litteral(self.nom, not self.signe)

    def pos(self):
        """
        Renvoit un litteral positif
        """
        return self


class Variable:
    """
    Représente un variable en logique propositionnel
    """

    nom: str

    def __init__(self, nomVar):
        self.nom = nomVar

    def pos(self):
        """
        Renvoit un variable positif
        """
        return Litteral(self.nom, True)

    def neg(self):
        """
        Renvoit un variable negatif
        """
        return Litteral(self.nom, False)


def regle_ou_condition(conds: List[Litteral], actions: List[Litteral]):
    """
    Génére les règles si la condition est une clause. "Si conds, alors actions"
    :param conds: Lists de littéraux
    :param actions: List de littéraux
    :return:
    """
    res = []

    for action in actions:
        clause = tuple([cond.neg() for cond in conds] + [action.pos()])
        res.append(clause)

    return res


def regle_et_condition(conds: List[Litteral], action: Litteral):
    """
    Génère pour chaque condition une règle l'associant à l'action
    :param conds : List de littéraux
    :param action: Littéral
    """
    res = []
    list_positif_condition = []
    for cond in conds:
        res.append(tuple([cond.neg(), action.pos()]))
        list_positif_condition.append(
            cond
        ) if cond.signe else list_positif_condition.append(cond.neg())

    list_positif_condition.append(action.neg())
    res.append(tuple(list_positif_condition))

    return res


def regle_horn(litteraux: List[Litteral]):
    """
    Seulement un seul littéral peut être vrai
    :param litteraux: Liste de littéraux
    :return: Tableau correspondant à une clause de horn postiif
    """
    return [
        tuple([lit1.neg(), lit2.neg()])
        for (lit1, lit2) in itertools.product(litteraux, repeat=2)
        if lit1 != lit2
    ]


def regle_unique_statut(litteraux: List[Litteral]):
    """
    Génère les clauses appliquant la contrainte unique
    :param litteraux: Liste de Littéral
    :return: Tableau de clauses
    """
    au_moins_un_statut = []
    for litteral in litteraux:
        au_moins_un_statut.append(
            litteral
        ) if litteral.signe else au_moins_un_statut.append(litteral.neg())
    au_plus_un_statut = regle_horn(litteraux)
    return [tuple(au_moins_un_statut)] + au_plus_un_statut


def compatible_position(stepcoord: StepCoord, stage_data):
    """
    Vérifie si la possible est légal
    :param stepcoord: Coordonnées et pas
    :param stage_data: Dictionnaire représentant le monde
    :return: Booléen
    """
    step_pb, x_coord, y_coord = stepcoord
    return (
            0 <= step_pb <= stage_data["max_steps"]
            and 0 <= x_coord < stage_data["n"]
            and 0 <= y_coord < stage_data["m"]
    )


def suiv_coord(setpcoord: StepCoord):
    """
    Retourne la prochaine état
    :param setpcoord: Coordonnées et pas
    :return: Coordonnées et pas suivant
    """
    step_pb, x_coord, y_coord = setpcoord
    return step_pb - 1, x_coord, y_coord


def prec_coord(setpcoord: StepCoord):
    """
    Retourne la précédante état
    :param setpcoord: Coordonnées et pas
    :return: Coordonnées et pas précédant
    """
    step_pb, x_coord, y_coord = setpcoord
    return step_pb + 1, x_coord, y_coord


def get_lock_positions(stage_data):
    """
    Recherche les coordonnées du coffre
    :param stage_data: Représentation dictionnaire du monde
    :return: Tous les couples de coordonnées où se trouve un coffre
    """
    res = []
    for y_coord in range(stage_data["m"]):
        for x_coord in range(stage_data["n"]):
            if stage_data["grid"][y_coord][x_coord] == "L":
                res.append(tuple([x_coord, y_coord]))
    return res


def get_close_cells(
        step_pb: int,
        current_x: int,
        current_y: int,
        stage_data,
        gap: int = 1,
        self_cell: bool = True,
):
    """
    Retourne toutes les cases adjacentes
    :param step_pb: Nombre réprésentant le pas
    :param current_x: Position x actuel
    :param current_y: Position y actuel
    :param stage_data: Représentation du monde
    :param gap: Delta autour de la case actuel
    :param self_cell: Booléen pour inclure ou non la case actuel
    :return: Tableau de coordonnées
    """
    pos_list = [
        (current_x - gap, current_y),
        (current_x, current_y - gap),
        (current_x + gap, current_y),
        (current_x, current_y + gap),
    ]
    if self_cell:
        pos_list.append((current_x, current_y))

    res = []
    for x_coord, y_coord in pos_list:
        pos = (step_pb, x_coord, y_coord)
        if compatible_position(pos, stage_data):
            res.append(pos)
    return res


def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8"):
    """
    Exécute le solveur SAT sur le fichier
    :param filename:
    :param cmd:
    :param encoding:
    :return:
    """
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return "UNSAT"

    model = lines[2][2:].split(" ")

    return [int(x) for x in model]


def write_cnf(file_name, variables, cnf, comment=""):
    """
    Ecrit le fichier DMACS et execute le solveur
    Requirement : Avoir glophersat dans les variables environnement
    :param file_name: Nom du fichier
    :param variables: Nombre de variables
    :param cnf: Liste clauses
    :param comment: Commentaire à ajouter au fichier
    :return: Modèle donné par le solveur
    """

    def write_file(name, content, newlines=True, mode="a"):
        """
        Écrit dans un fichier
        :param name: Nom du fichier
        :param content: Contenu
        :param newlines: Rajoute \n à la fin si vrai
        :param mode: Write mode
        :return:
        """
        fichier = open(name + ".cnf", mode)
        fichier.write(content)
        if newlines:
            fichier.write("\n")
        fichier.close()

    array_clauses = cnf
    comment = "c " + comment
    write_file(file_name, comment, mode="w")
    write_file(file_name, "p cnf %s %s 0" % (variables, len(cnf)))

    for close in array_clauses:
        for lit in close:
            write_file(file_name, str(lit) + " ", newlines=False)
        write_file(file_name, "0")
    return exec_gophersat(file_name + ".cnf")


class SatProblem:
    """
    Classe contenant les variables et les clauses
    """

    variables: Set[Variable]
    clauses: List[Tuple[Litteral]]

    def __init__(self):
        self.variables = set()
        self.clauses = []

    def add_variable(self, nom: str):
        """
        Ajoute une variable à la liste des variables
        :param nom: Nom de la variable
        :return: Objet Variable avec le nom donné en paramètre
        """
        var = Variable(nom)
        if var in self.variables:
            raise ValueError("Duplication")

        self.variables.add(var)
        return var

    def add_clauses(self, clauses: List[Tuple[Litteral]]):
        """
        Ajoute les clauses à la liste des clauses
        :param clauses: List de clauses (Clause = tuple[Litteral])
        :return: None
        """
        self.clauses.extend(clauses)

    def solve(self):
        """
        Utilise les variables et les clauses pour résoudre en appelant le solver
        :return: Soit un string, soit un dictionnaire de variable
        """

        variable2id = {
            v.nom: _id for _id, v in enumerate(sorted(self.variables, key=str), start=1)
        }
        id2variable = {v: k for k, v in variable2id.items()}
        variable = len(id2variable)
        cnf = self.convert_cnf(variable2id)

        # Utiliser pycosat permet de meilleures performances
        # solution = pycosat.solve(cnf)

        # Utiliser glophersat requiert d'écrire dans un fichier impliquant
        # une perte très conséquente de performances.
        # Décommenter la ligne ci-dessus pour l'utiliser
        solution = write_cnf("solution", variable, cnf)

        if solution == "UNSAT":
            return "UNSAT"
        return {id2variable[abs(s)]: s > 0 for s in solution[:-1]}

    def convert_cnf(self, variable2id: Dict):
        """
        Convertit les clauses en CNF en associant à chaque var son signe
        :param variable2id: Tableau de correspondace variable et id
        :return: Tableau de variable transformé en id avec leur signe
        """
        res = []
        for i in self.clauses:
            res.append([(1 if sv.signe else -1) * variable2id[sv.nom] for sv in i])

        return res


@dataclass(frozen=True)
class CaseState:
    """
    Représentation de la state d'une case avec tous les status
    """

    step_position: StepCoord

    est_monstre: Variable
    est_coffre: Variable
    est_hero: Variable
    est_bloquer: Variable
    est_pas_poussable: Variable
    est_mur: Variable
    est_but: Variable
    est_proche_coffre: Variable
    est_piege: Variable
    est_piege_active: Variable
    est_monstre_dif: Variable
    est_vide: Variable
    est_bloc: Variable

    @classmethod
    def create(cls, step_position, problem: SatProblem):
        """
        Retourne une case avec les règles associés
        :param step_position: Tuple contenant la step, et les coordonnées
        :param problem: Modélisation du problem SAT
        :return: CaseState objet
        """
        step_case, x_coord, y_coord = step_position
        prefix = f"S{step_case}:X{x_coord}Y{y_coord}"
        return cls(
            step_position=step_position,
            est_vide=problem.add_variable(f"{prefix}:vide"),
            est_bloc=problem.add_variable(f"{prefix}:bloc"),
            est_monstre=problem.add_variable(f"{prefix}:monstre"),
            est_hero=problem.add_variable(f"{prefix}:hero"),
            est_mur=problem.add_variable(f"{prefix}:mur"),
            est_but=problem.add_variable(f"{prefix}:but"),
            est_coffre=problem.add_variable(f"{prefix}:coffre"),
            est_proche_coffre=problem.add_variable(f"{prefix}:proche_coffre"),
            est_bloquer=problem.add_variable(f"{prefix}:bloquer"),
            est_pas_poussable=problem.add_variable(f"{prefix}:pas_poussable"),
            est_piege=problem.add_variable(f"{prefix}:piege"),
            est_piege_active=problem.add_variable(f"{prefix}:piege_active"),
            est_monstre_dif=problem.add_variable(f"{prefix}:enemy_dif"),
        )

    def regle_init(self):
        """
        Initialisaiton des règles pour une case
        :return: None
        """
        return (
                regle_unique_statut(
                    [
                        self.est_vide.pos(),
                        self.est_bloc.pos(),
                        self.est_monstre.pos(),
                        self.est_hero.pos(),
                        self.est_mur.pos(),
                        self.est_but.pos(),
                        self.est_proche_coffre.pos(),
                    ]
                )
                + regle_et_condition(
            [
                Litteral(self.est_proche_coffre.nom, True),
                Litteral(self.est_but.nom, True),
                Litteral(self.est_monstre.nom, True),
                Litteral(self.est_bloc.nom, True),
                Litteral(self.est_mur.nom, True),
            ],
            Litteral(self.est_bloquer.nom, True),
        )
                + self.regle_pousssable()
                + self.regle_monstre_dif()
        )

    def regle_pousssable(self):
        """
        Initialisation des règles pour les blocs poussables
        :return: void
        """
        return regle_et_condition(
            [Litteral(self.est_mur.nom, True), Litteral(self.est_but.nom, True)],
            Litteral(self.est_pas_poussable.nom, True),
        )

    def regle_piege(self):
        """
        Initialisation des règles pour les pièges
        :return: void
        """
        return regle_ou_condition(
            [Litteral(self.est_piege.nom, False)],
            [Litteral(self.est_piege_active.nom, False)],
        )

    def regle_monstre_dif(self):
        """
        Initialisation des règles sur la positionnement des monstres
        :return: void
        """
        return (
                regle_ou_condition(
                    [
                        Litteral(self.est_piege_active.nom, True),
                        Litteral(self.est_piege.nom, True),
                        Litteral(self.est_monstre_dif.nom, True),
                    ],
                    [Litteral(self.est_monstre.nom, False)],
                )
                + regle_ou_condition(
            [
                Litteral(self.est_piege_active.nom, False),
                Litteral(self.est_piege.nom, True),
                Litteral(self.est_monstre_dif.nom, True),
            ],
            [Litteral(self.est_monstre.nom, True)],
        )
                + regle_ou_condition(
            [
                Litteral(self.est_piege.nom, False),
                Litteral(self.est_monstre_dif.nom, False),
            ],
            [Litteral(self.est_monstre.nom, False)],
        )
                + regle_ou_condition(
            [
                Litteral(self.est_piege.nom, False),
                Litteral(self.est_monstre_dif.nom, True),
            ],
            [Litteral(self.est_monstre.nom, True)],
        )
        )


@dataclass(frozen=True)
class UserControl:
    """
    Classe représentant les actions possibles dans le jeu
    """

    step: int

    is_left: Variable
    is_up: Variable
    is_right: Variable
    is_down: Variable
    skip: Variable  # Représente la perte d'action via un piège

    def init_rules(self):
        """
        Seulement une action possible par input (Contrainte unique)
        :return: Liste de littéraux
        """
        return regle_unique_statut(
            [
                Litteral(self.is_left.nom, True),
                self.is_up.pos(),
                self.is_right.pos(),
                self.is_down.pos(),
                self.skip.pos(),
            ]
        )

    @classmethod
    def create(cls, user_step: int, problem: SatProblem):
        """
        Génére la classe selon les pas et l'ajoute au pb
        :param user_step: Nombre représentant le pas
        :param problem: SAT problem objet contenant tous les variables
        :return: UserInput objet
        """
        return cls(
            step=user_step,
            is_down=problem.add_variable(f"S{user_step}:C:down"),
            is_left=problem.add_variable(f"S{user_step}:C:left"),
            is_right=problem.add_variable(f"S{user_step}:C:right"),
            is_up=problem.add_variable(f"S{user_step}:C:up"),
            skip=problem.add_variable(f"S{user_step}:C:skip"),
        )


StageStates: Dict[StepCoord, CaseState]
ControlStates: Dict[int, UserControl]


@dataclass(frozen=True)
class KeyState:
    """
    Classe représentant la possession ou non de la clé
    """

    cle: Dict[int, Variable]

    @classmethod
    def create(cls, steps: int, problem: SatProblem):
        """
        Génere la classe selon les pas et l'ajoute au pb
        :param steps: Nombre représentant le pas
        :param problem: SAT problem objet contenant tous les variables
        :return: KeyState objet
        """
        res = {}
        for step_user in range(steps + 1):
            res[step_user] = problem.add_variable(f"S{step_user}:Aux:cle")
        return cls(
            cle=res,
        )


class HelltakerProblem:
    """
    Classe représentant le problem Helltaker
    """

    stage_data: dict
    stage_states: Dict[StepCoord, CaseState]
    input_states: Dict[int, UserControl]
    key_states: KeyState
    problem: SatProblem
    solution: Optional[Union[Dict[str, bool], str]]

    def __init__(
            self,
            stage_data: dict,
            stage_states: Dict[StepCoord, CaseState],
            control_states: Dict[int, UserControl],
            key_states: KeyState,
            problem: SatProblem,
    ):
        self.stage_data = stage_data
        self.stage_states = stage_states
        self.input_states = control_states
        self.key_states = key_states
        self.problem = problem
        self.solution = None

    def solve(self):
        """
        Appelle la résolution via solver
        :return: void
        """
        self.solution = self.problem.solve()

    def get_solution(self):
        """
        Récupère les solutions
        :return: Tableau de str représentant les actions à réaliser
        """
        if self.solution == "UNSAT":
            return "UNSAT"
        return [
            (self.convert_format_ctl(step_pb))
            for step_pb in range(self.stage_data["max_steps"], -1, -1)
        ]

    def convert_format_ctl(self, user_step: int):
        """
        Convertit en str
        :param user_step: Nombre représentant le pas
        :return: Action en str
        """
        if user_step == 0:
            return "\n"
        control_state: UserControl = self.input_states[user_step]
        if self.solution[control_state.is_up.nom]:
            return "H"
        if self.solution[control_state.is_down.nom]:
            return "B"
        if self.solution[control_state.is_left.nom]:
            return "G"
        if self.solution[control_state.is_right.nom]:
            return "D"
        if self.solution[control_state.skip.nom]:
            return ""
        return "-----"

    def format_key_state(self, step_user):
        """
        Convertit en str l'état clé
        :param step_user: Nombre représentant le pas
        :return: Action en str
        """
        cle = self.key_states.cle[step_user]
        if self.solution[cle.nom]:
            return "clé"
        return ""


def generate_problem(stage_data):
    """
    Génére toutes les rgèles du monde
    :param stage_data: Modélisation du niveau
    :return: Objet HelltakerProblem
    """
    sat_problem = SatProblem()
    helltaker_problem = HelltakerProblem(
        stage_data,
        add_stage_rules(stage_data, sat_problem),
        add_control_rules(stage_data, sat_problem),  # Possède
        KeyState.create(stage_data["max_steps"], sat_problem),  # Possède la clé
        sat_problem,
    )
    add_init_state_rules(helltaker_problem)
    add_final_state_rules(helltaker_problem)
    add_movement_rules(helltaker_problem)
    add_spike_rules(helltaker_problem)
    add_skip_rules(helltaker_problem)
    add_stone_rules(stage_data, helltaker_problem)
    add_key_rules(helltaker_problem)
    add_kick_rules(helltaker_problem)
    add_monster_rules(stage_data, helltaker_problem)
    add_lock_rules(helltaker_problem)
    add_stone_static_rules(helltaker_problem)

    return helltaker_problem


def add_stage_rules(stage_data: dict, problem: SatProblem):
    """
    Génére les règles concernant les states possibles du monde
    :param stage_data: Dictionnaire représentant le monde
    :param problem: Sat problem objet
    :return: Retourne l'état initial du monde
    """
    stage_states = {}
    height = stage_data["m"]
    width = stage_data["n"]

    # Initialisation de chaque state pour chaque case
    for step_case in range(stage_data["max_steps"] + 1):
        for y_coord in range(height):
            for x_coord in range(width):
                steppos = (step_case, x_coord, y_coord)
                state = CaseState.create(steppos, problem)
                stage_states[steppos] = state

                problem.add_clauses(state.regle_init())
    for step_case in range(stage_data["max_steps"] + 1):
        # Un seul joueur peut seulement exister
        rules = regle_unique_statut(
            [
                Litteral(stage_states[(step_case, x_coord, y_coord)].est_hero.nom, True)
                for y_coord in range(height)
                for x_coord in range(width)
            ]
        )
        problem.add_clauses(rules)

    return stage_states


def add_control_rules(stage_data: dict, problem: SatProblem):
    """
    Génére les règles concernant les actions utilisateurs
    :param stage_data: Dictionnaire représentant le monde
    :param problem: Sat problem objet
    :return: Retourne le control states
    """
    control_states = {}
    for user_step in range(1, stage_data["max_steps"] + 1):
        state = UserControl.create(user_step, problem)
        control_states[user_step] = state

        problem.add_clauses(state.init_rules())

    return control_states


def add_init_state_rules(helltaker_problem: HelltakerProblem):
    """
    Génére les règles initiaux du monde
    :param helltaker_problem: Modélisation du problem
    :return: Void
    """
    problem: SatProblem = helltaker_problem.problem
    stage_data = helltaker_problem.stage_data
    stage_states = helltaker_problem.stage_states
    initial_step = stage_data["max_steps"]

    clauses: List[Tuple[Litteral]] = []
    for y_coord in range(stage_data["m"]):
        for x_coord in range(
                stage_data["n"]
        ):  # Pour chaque case, attribue le bon statut
            state: CaseState = stage_states[(initial_step, x_coord, y_coord)]
            cell = stage_data["grid"][y_coord][x_coord]

            if cell == "H":
                clauses.append(tuple([state.est_hero.pos()]))
            if cell in ["B", "O", "P", "Q"]:
                clauses.append(tuple([state.est_bloc.pos()]))
            else:
                clauses.append(tuple([state.est_bloc.neg()]))
            if cell == "M":
                clauses.append(tuple([state.est_monstre.pos()]))
            else:
                clauses.append(tuple([state.est_monstre.neg()]))
            if cell == "L":
                clauses.append(tuple([state.est_coffre.pos()]))
            if cell == "U":
                clauses.append(tuple([state.est_piege.pos()]))
                clauses.append(tuple([state.est_piege_active.pos()]))
            elif cell in ["P", "T"]:
                clauses.append(tuple([state.est_piege.pos()]))
                clauses.append(tuple([state.est_piege_active.neg()]))

            # Génére tous les états possibles pour les cases
            # immobiles pour chaque pas
            for step_pb in range(stage_data["max_steps"] + 1):
                state = stage_states[(step_pb, x_coord, y_coord)]
                if cell == "#":
                    clauses.append(tuple([state.est_mur.pos()]))
                else:
                    clauses.append(tuple([state.est_mur.neg()]))
                if cell == "D":
                    clauses.append(tuple([state.est_but.pos()]))
                else:
                    clauses.append(tuple([state.est_but.neg()]))
                if cell != "L":
                    clauses.append(tuple([state.est_coffre.neg()]))
                if cell in ["S", "T", "O", "P", "Q", "U"]:
                    clauses.append(tuple([state.est_piege.pos()]))
                    if cell == "S":
                        clauses.append(tuple([state.est_piege_active.pos()]))
                else:
                    clauses.append(tuple([state.est_piege.neg()]))
                    clauses.append(tuple([state.est_piege_active.neg()]))
    problem.add_clauses(clauses)


def add_final_state_rules(helltaker_problem: HelltakerProblem):
    """
    Génére les règles pour terminer le niveau
    :param helltaker_problem: Modélisation du probleme
    :return: Void
    """
    problem: SatProblem = helltaker_problem.problem
    stage_data = helltaker_problem.stage_data
    stage_states = helltaker_problem.stage_states

    res = []
    for y_coord in range(stage_data["m"]):
        for x_coord in range(stage_data["n"]):
            cell = stage_data["grid"][y_coord][x_coord]
            # Pour chaque démon, attribue les conditions de victors autour d'elle.
            if cell == "D":
                for variable in [
                    stage_states[steppos].est_hero
                    for steppos in get_close_cells(
                        0, x_coord, y_coord, stage_data, self_cell=False
                    )
                ]:
                    res.append(variable.pos())
    problem.add_clauses([tuple(res)])


def add_movement_rules(helltaker_problem: HelltakerProblem):
    """
    Génére tous les règles de mouvements
    :param helltaker_problem: Modélisation du probleme
    :return: Void
    """
    problem: SatProblem = helltaker_problem.problem
    control_states = helltaker_problem.input_states
    stage_states = helltaker_problem.stage_states
    stage_data = helltaker_problem.stage_data

    clauses = []

    for step_coord, state in stage_states.items():
        (step, x_coord, y_coord) = step_coord
        if step <= 0:
            continue

        control: UserControl = control_states[step]
        y1 = max(y_coord - 1, 0)
        y2 = min(y_coord + 1, stage_data["m"] - 1)
        x1 = max(x_coord - 1, 0)
        x2 = min(x_coord + 1, stage_data["n"] - 1)

        pos_up = (step, x_coord, y1)
        pos_down = (step, x_coord, y2)
        pos_right = (step, x2, y_coord)
        pos_left = (step, x1, y_coord)
        clauses.extend(
            [
                # Reste sur place si déplacement haut impossible
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_up).est_bloquer.nom, True),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_up.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_hero.nom, True
                        )
                    ],
                ),
                # Déplacement haut
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_up).est_bloquer.nom, False),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_up.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_vide.nom, True
                        ),
                        Litteral(
                            stage_states.get(suiv_coord(pos_up)).est_hero.nom, True
                        ),
                    ],
                ),
                # Reste sur place si déplacement bas impossible
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_down).est_bloquer.nom, True),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_down.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_hero.nom, True
                        )
                    ],
                ),
                # Déplacement vers le bas
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_down).est_bloquer.nom, False),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_down.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_vide.nom, True
                        ),
                        Litteral(
                            stage_states.get(suiv_coord(pos_down)).est_hero.nom, True
                        ),
                    ],
                ),
                # Reste sur place si déplacement gauche impossible
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_left).est_bloquer.nom, True),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_left.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_hero.nom, True
                        )
                    ],
                ),
                # Déplacement vers la gauche
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_left).est_bloquer.nom, False),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_left.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_vide.nom, True
                        ),
                        Litteral(
                            stage_states.get(suiv_coord(pos_left)).est_hero.nom, True
                        ),
                    ],
                ),
                # Déplacement vers la droite bloqué
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_right).est_bloquer.nom, True),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_right.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_hero.nom, True
                        )
                    ],
                ),
                # Déplacement vers la droite
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(pos_right).est_bloquer.nom, False),
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.is_right.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_vide.nom, True
                        ),
                        Litteral(
                            stage_states.get(suiv_coord(pos_right)).est_hero.nom, True
                        ),
                    ],
                ),
                # Le héros reste sur place si l'action skip est invoqué
                regle_ou_condition(
                    [
                        Litteral(stage_states.get(step_coord).est_hero.nom, True),
                        control.skip.pos(),
                    ],
                    [
                        Litteral(
                            stage_states.get(suiv_coord(step_coord)).est_hero.nom, True
                        )
                    ],
                ),
            ]
        )

    res = []
    for i in clauses:
        res += i

    problem.add_clauses(res)


def add_kick_rules(helltaker_problem: HelltakerProblem):
    """
    Génère tous les règles de pousse
    :param helltaker_problem: Modélisation du probleme
    :return: Void
    """
    stage_states = helltaker_problem.stage_states
    control_states = helltaker_problem.input_states
    stage_data = helltaker_problem.stage_data
    problem: SatProblem = helltaker_problem.problem

    def init_rules(
            step_pos: StepCoord, ctl: Variable, adj_steppos: StepCoord
    ):
        if compatible_position(adj_steppos, stage_data):
            return (
                regle_ou_condition(  # Action illégal si pousse un objet non poussable
                    [
                        Litteral(stage_states.get(step_pos).est_hero.nom, True),
                        Litteral(
                            stage_states.get(adj_steppos).est_pas_poussable.nom, True
                        ),
                    ],
                    [ctl.neg()],
                )
            )
        else:
            return regle_ou_condition(  # Action illégal si ne pousse pas
                [Litteral(stage_states.get(step_pos).est_hero.nom, True)],
                [ctl.neg()],
            )

    for step_coord, cell_state in stage_states.items():
        step, x_coord, y_coord = step_coord
        control = control_states.get(step)
        if control is None:
            continue

        step_coord_le = (step, x_coord - 1, y_coord)
        step_coord_do = (step, x_coord, y_coord + 1)
        step_coord_ri = (step, x_coord + 1, y_coord)
        step_coord_up = (step, x_coord, y_coord - 1)

        problem.add_clauses(init_rules(step_coord, control.is_up, step_coord_up))
        problem.add_clauses(init_rules(step_coord, control.is_left, step_coord_le))
        problem.add_clauses(init_rules(step_coord, control.is_right, step_coord_ri))
        problem.add_clauses(init_rules(step_coord, control.is_down, step_coord_do))


def add_skip_rules(helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour l'action skip ("Action réduit à cause des pièges)
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    stage_states = helltaker_problem.stage_states
    control_states = helltaker_problem.input_states

    clauses = []
    for steppos, cell_state in stage_states.items():
        step, x_coord, y_coord = steppos
        control = control_states.get(step)
        prev_control = control_states.get(step + 1)
        if control is None:
            continue
        clauses.extend(
            # L'action skip n'est pas fait si le piège est désactivé
            regle_ou_condition(
                [
                    Litteral(cell_state.est_hero.nom, True),
                    Litteral(cell_state.est_piege_active.nom, False),
                ],
                [control.skip.neg()],
            )
        )
        if prev_control is not None:
            # Il n'est pas possible de skip 2 fois de suite
            clauses.extend(
                regle_horn(
                    [
                        Litteral(prev_control.skip.nom, True),
                        Litteral(control.skip.nom, True),
                    ]
                )
            )
            clauses.extend(
                # L'action skip n'est pas refaite si la personne a pris un piège actif
                # sur la meme case durant la précedente action (Dynamique piège)
                regle_ou_condition(
                    [
                        prev_control.skip.pos(),
                        cell_state.est_hero.pos(),
                        cell_state.est_piege_active.pos(),
                    ],
                    [control.skip.neg()],
                )
            )
            clauses.extend(
                # L'action skip est faite si la personne n'a pas pris un piège actif
                # sur la même case durant la précedente action (Dynamique piège)
                regle_ou_condition(
                    [
                        prev_control.skip.neg(),
                        cell_state.est_hero.pos(),
                        cell_state.est_piege_active.pos(),
                    ],
                    [control.skip.pos()],
                )
            )
    helltaker_problem.problem.add_clauses(clauses)


def add_spike_rules(helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour les pièges
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    problem: SatProblem = helltaker_problem.problem
    stage_data = helltaker_problem.stage_data
    stage_states = helltaker_problem.stage_states
    control_states = helltaker_problem.input_states

    for steppos, cell_state in stage_states.items():
        step, x_coord, y_coord = steppos
        cell_type = stage_data["grid"][y_coord][x_coord]

        if cell_type in ["S", "O"]:
            # Associe le statut piège et actif pour les pièges statiques
            problem.add_clauses(
                [
                    tuple([Litteral(cell_state.est_piege.nom, True)]),
                    tuple([Litteral(cell_state.est_piege_active.nom, True)]),
                ]
            )

        elif cell_type in ["T", "U", "Q", "P"]:
            # Associe le statut piège pour les pièges dynamiques
            problem.add_clauses([tuple([Litteral(cell_state.est_piege.nom, True)])])
            if step == 0:
                continue
            control: UserControl = control_states[step]
            problem.add_clauses(
                regle_ou_condition(
                    [cell_state.est_piege_active.pos(), control.skip.pos()],
                    [stage_states[suiv_coord(steppos)].est_piege_active.pos()],
                )
            )

            problem.add_clauses(
                regle_ou_condition(
                    [cell_state.est_piege_active.neg(), control.skip.pos()],
                    [stage_states[suiv_coord(steppos)].est_piege_active.neg()],
                )
            )
            # Les pièges dynamique activés sont désactivés à la prochaine action
            problem.add_clauses(
                regle_ou_condition(
                    [cell_state.est_piege_active.pos(), control.skip.neg()],
                    [stage_states[suiv_coord(steppos)].est_piege_active.neg()],
                )
            )
            # Les pièges dynamique désactivés sont activés à la prochaine action
            problem.add_clauses(
                regle_ou_condition(
                    [cell_state.est_piege_active.neg(), control.skip.neg()],
                    [stage_states[suiv_coord(steppos)].est_piege_active.pos()],
                )
            )

        else:
            # Autre chose qu'un piège
            problem.add_clauses([tuple([Litteral(cell_state.est_piege.nom, False)])])
            problem.add_clauses(
                [tuple([Litteral(cell_state.est_piege_active.nom, False)])]
            )


def add_stone_static_rules(helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour les blocs
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    problem: SatProblem = helltaker_problem.problem
    stage_states = helltaker_problem.stage_states
    stage_data = helltaker_problem.stage_data

    clauses = []
    for steppos, state in stage_states.items():
        (step, x_coord, y_coord) = steppos
        if stage_data["max_steps"] > step:
            clauses.extend(
                # Si une case n'était pas précedemment un bloc ou aux alentours,
                # il n'est pas possible de devenir un bloc
                regle_ou_condition(
                    [
                        stage_states.get(c).est_bloc.neg()
                        for c in get_close_cells(step + 1, x_coord, y_coord, stage_data)
                    ],
                    [stage_states.get(steppos).est_bloc.neg()],
                )
            )
    problem.add_clauses(clauses)


def add_monster_rules(stage_data, helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour les monstres
     :param stage_data: Modélisation du monde en dictionnaire
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    problem: SatProblem = helltaker_problem.problem
    control_states = helltaker_problem.input_states
    stage_states = helltaker_problem.stage_states

    def init_rules(
            ctrl: Variable,
            steppos_from: StepCoord,
            steppos_player: StepCoord,
            steppos_to: StepCoord,
    ):
        clauses_tab = []

        next_steppos_from = suiv_coord(steppos_from)
        next_steppos_player = suiv_coord(steppos_player)
        next_steppos_to = suiv_coord(steppos_to)
        if (
                not compatible_position(steppos_from, stage_data)
                or not compatible_position(steppos_player, stage_data)
                or not compatible_position(next_steppos_from, stage_data)
                or not compatible_position(next_steppos_player, stage_data)
        ):
            return []

        move_conditions: List[Litteral] = [
            ctrl.pos(),
            stage_states.get(steppos_from).est_hero.pos(),
            stage_states.get(steppos_player).est_monstre.pos(),
        ]
        # Ennemi supprimé si il est poussé dans une case bloqué
        clauses_tab.extend(
            regle_ou_condition(
                move_conditions,
                [stage_states.get(next_steppos_player).est_monstre_dif.neg()],
            )
        )
        # Ennemi déplacé si case vide
        if compatible_position(steppos_to, stage_data):
            clauses_tab.extend(
                regle_ou_condition(
                    move_conditions + [stage_states.get(steppos_to).est_vide.pos()],
                    [stage_states.get(next_steppos_to).est_monstre_dif.pos()],
                )
            )

        # Ennemi reste sur place si action illégal
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_from).est_hero.pos(),
                    stage_states.get(steppos_player).est_monstre.pos(),
                ],
                [stage_states.get(next_steppos_player).est_monstre_dif.pos()],
            )
        )
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_from).est_hero.pos(),
                    stage_states.get(steppos_player).est_monstre.neg(),
                ],
                [stage_states.get(next_steppos_player).est_monstre_dif.neg()],
            )
        )

        # Si action illégale, la case joueur ne fusionne pas avec l'état monstre
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_from).est_hero.pos(),
                    stage_states.get(steppos_player).est_monstre.neg(),
                ],
                [stage_states.get(next_steppos_player).est_monstre_dif.neg()],
            )
        )
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_from).est_hero.pos(),
                    stage_states.get(steppos_player).est_monstre.pos(),
                ],
                [stage_states.get(steppos_player).est_monstre_dif.pos()],
            )
        )
        if compatible_position(steppos_to, stage_data):
            # Reste sur place si action illégal
            clauses_tab.extend(
                regle_ou_condition(
                    [
                        ctrl.neg(),
                        stage_states.get(steppos_from).est_hero.pos(),
                        stage_states.get(steppos_to).est_monstre.neg(),
                    ],
                    [stage_states.get(next_steppos_to).est_monstre_dif.neg()],
                )
            )
            clauses_tab.extend(
                regle_ou_condition(
                    [
                        ctrl.pos(),
                        stage_states.get(steppos_from).est_hero.pos(),
                        stage_states.get(steppos_player).est_monstre.neg(),
                        stage_states.get(steppos_to).est_monstre.neg(),
                    ],
                    [stage_states.get(next_steppos_to).est_monstre_dif.neg()],
                )
            )

        return clauses_tab

    clauses = []
    for steppos, state in stage_states.items():
        (step, x_coord, y_coord) = steppos
        next_steppos = (step - 1, x_coord, y_coord)
        if step == 0:
            continue

        # Si une monstre n'existe pas aux alentours,
        # alors impossible que la case possède un monstre à l'avenir
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_monstre.neg()
                    for c in get_close_cells(*steppos, stage_data)
                ],
                [
                    stage_states.get(next_steppos).est_monstre_dif.neg(),
                    stage_states.get(next_steppos).est_monstre.neg(),
                ],
            )
        )

        # Un ennemi reste sur place
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_hero.neg()
                    for c in get_close_cells(*steppos, stage_data)
                ]
                + [Litteral(stage_states.get(steppos).est_monstre.nom, True)],
                [Litteral(stage_states.get(next_steppos).est_monstre_dif.nom, True)],
            )
        )
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_hero.neg()
                    for c in get_close_cells(*steppos, stage_data, 2)
                ]
                + [stage_states.get(steppos).est_monstre.neg()],
                [stage_states.get(next_steppos).est_monstre_dif.neg()],
            )
        )
        step_up = (step, x_coord, y_coord - 1)
        step_down = (step, x_coord, y_coord + 1)
        control = control_states[step]

        step_left = (step, x_coord - 1, y_coord)
        step_right = (step, x_coord + 1, y_coord)

        clauses.extend(init_rules(control.is_right, step_left, steppos, step_right))
        clauses.extend(init_rules(control.is_left, step_right, steppos, step_left))
        clauses.extend(init_rules(control.is_down, step_up, steppos, step_down))
        clauses.extend(init_rules(control.is_up, step_down, steppos, step_up))

    problem.add_clauses(clauses)


def add_stone_rules(stage_data, helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour les blocs
     :param stage_data: Modélisation du monde en dictionnaire
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    problem: SatProblem = helltaker_problem.problem
    control_states = helltaker_problem.input_states
    stage_states = helltaker_problem.stage_states

    def init_rules(
            ctrl: Variable,
            steppos_current: StepCoord,
            steppos_player: StepCoord,
            steppos_next: StepCoord,
    ):
        clauses_tab = []

        next_steppos_current = suiv_coord(steppos_current)
        next_steppos_player = suiv_coord(steppos_player)
        next_steppos_next = suiv_coord(steppos_next)
        if (
                not compatible_position(steppos_current, stage_data)
                or not compatible_position(steppos_player, stage_data)
                or not compatible_position(next_steppos_current, stage_data)
                or not compatible_position(next_steppos_player, stage_data)
        ):
            return []

        #
        move_conditions: List[Litteral] = [
            ctrl.pos(),
            stage_states.get(steppos_current).est_hero.pos(),
            stage_states.get(steppos_player).est_bloc.pos(),
        ]
        if compatible_position(steppos_next, stage_data):
            # Déplacement si la case suivante vide
            clauses_tab.extend(
                regle_ou_condition(
                    move_conditions + [stage_states.get(steppos_next).est_vide.pos()],
                    [stage_states.get(next_steppos_next).est_bloc.pos()],
                )
            )
            # Reste sur place si case non vide
            clauses_tab.extend(
                regle_ou_condition(
                    move_conditions + [stage_states.get(steppos_next).est_vide.neg()],
                    [stage_states.get(next_steppos_player).est_bloc.pos()],
                )
            )
        else:
            # Reste sur place si pas d'actions concernant le bloc
            clauses_tab.extend(
                regle_ou_condition(
                    move_conditions,
                    [stage_states.get(next_steppos_player).est_bloc.pos()],
                )
            )

        # Reste sur place si action illégal
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_current).est_hero.pos(),
                    stage_states.get(steppos_player).est_bloc.pos(),
                ],
                [stage_states.get(next_steppos_player).est_bloc.pos()],
            )
        )
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_current).est_hero.pos(),
                    stage_states.get(steppos_player).est_bloc.neg(),
                ],
                [stage_states.get(next_steppos_player).est_bloc.neg()],
            )
        )

        # Ne fusionne pas avec la case joueur si action illégale
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_current).est_hero.pos(),
                    stage_states.get(steppos_player).est_bloc.neg(),
                ],
                [stage_states.get(next_steppos_player).est_bloc.neg()],
            )
        )
        clauses_tab.extend(
            regle_ou_condition(
                [
                    ctrl.neg(),
                    stage_states.get(steppos_current).est_hero.pos(),
                    stage_states.get(steppos_player).est_bloc.pos(),
                ],
                [stage_states.get(steppos_player).est_bloc.pos()],
            )
        )
        if compatible_position(steppos_next, stage_data):
            # Reste statique si action illégale
            clauses_tab.extend(
                regle_ou_condition(
                    [
                        ctrl.neg(),
                        stage_states.get(steppos_current).est_hero.pos(),
                        stage_states.get(steppos_next).est_bloc.neg(),
                    ],
                    [stage_states.get(next_steppos_next).est_bloc.neg()],
                )
            )
            clauses_tab.extend(
                regle_ou_condition(
                    [
                        ctrl.pos(),
                        stage_states.get(steppos_current).est_hero.pos(),
                        stage_states.get(steppos_player).est_bloc.neg(),
                        stage_states.get(steppos_next).est_bloc.neg(),
                    ],
                    [stage_states.get(next_steppos_next).est_bloc.neg()],
                )
            )

        return clauses_tab

    clauses = []
    for steppos, state in stage_states.items():
        (step, x_coord, y_coord) = steppos
        next_steppos = (step - 1, x_coord, y_coord)
        if step == 0:
            continue

        #  Une case ne peut être une roche si elle ou les cases proches ne le sont pas
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_bloc.neg()
                    for c in get_close_cells(*steppos, stage_data)
                ],
                [stage_states.get(next_steppos).est_bloc.neg()],
            )
        )

        # Un bloc reste immobile durant les pas
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_hero.neg()
                    for c in get_close_cells(*steppos, stage_data)
                ]
                + [stage_states.get(steppos).est_bloc.pos()],
                [stage_states.get(next_steppos).est_bloc.pos()],
            )
        )
        clauses.extend(
            regle_ou_condition(
                [
                    stage_states.get(c).est_hero.neg()
                    for c in get_close_cells(*steppos, stage_data, 2)
                ]
                + [stage_states.get(steppos).est_bloc.neg()],
                [stage_states.get(next_steppos).est_bloc.neg()],
            )
        )

        control = control_states[step]

        step_left = (step, x_coord - 1, y_coord)
        step_right = (step, x_coord + 1, y_coord)
        step_up = (step, x_coord, y_coord - 1)
        step_down = (step, x_coord, y_coord + 1)

        clauses.extend(init_rules(control.is_right, step_left, steppos, step_right))
        clauses.extend(init_rules(control.is_left, step_right, steppos, step_left))
        clauses.extend(init_rules(control.is_down, step_up, steppos, step_down))
        clauses.extend(init_rules(control.is_up, step_down, steppos, step_up))

    problem.add_clauses(clauses)


def add_key_rules(helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour la clé
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    stage_data = helltaker_problem.stage_data
    stage_states = helltaker_problem.stage_states
    aux_states: KeyState = helltaker_problem.key_states
    problem: SatProblem = helltaker_problem.problem

    for y_coord in range(stage_data["m"]):
        for x_coord in range(stage_data["n"]):
            if stage_data["grid"][y_coord][x_coord] != "K":
                continue
            key_x, key_y = x_coord, y_coord
            problem.add_clauses(
                [tuple([aux_states.cle[stage_data["max_steps"]].neg()])]
            )
            # Initialisation de l'état clé
            for target_step in range(stage_data["max_steps"]):
                key_cell_state: CaseState = stage_states[(target_step, key_x, key_y)]
                has_key_state: Variable = aux_states.cle[target_step]
                has_key_state_prev: Variable = aux_states.cle[target_step + 1]
                problem.add_clauses(
                    regle_ou_condition(
                        [Litteral(key_cell_state.est_hero.nom, True)],
                        [has_key_state.pos()],
                    )
                )
                problem.add_clauses(
                    regle_ou_condition(
                        [Litteral(has_key_state_prev.nom, True)],
                        [has_key_state.pos()],
                    )
                )
                problem.add_clauses(
                    regle_ou_condition(
                        [has_key_state_prev.neg(), key_cell_state.est_hero.neg()],
                        [has_key_state.neg()],
                    )
                )


def add_lock_rules(helltaker_problem: HelltakerProblem):
    """
    Génère les contraintes pour les coffres
    :param helltaker_problem: Modélisation du problème
    :return: void
    """
    stage_states = helltaker_problem.stage_states
    stage_data = helltaker_problem.stage_data
    control_states = helltaker_problem.input_states
    aux_states: KeyState = helltaker_problem.key_states
    problem: SatProblem = helltaker_problem.problem

    def gen_unlock_rule(
            ctl: Variable,
            lock_steppos: StepCoord,
            player_steppos: StepCoord,
    ):
        step_lock, _, _ = lock_steppos

        has_key = aux_states.cle[step_lock]

        if not compatible_position(player_steppos, stage_data):
            return []

        unlock_condition = regle_ou_condition(
            # Coffre supprimé si possède la clé et dévérouille le coffre
            [
                has_key.pos(),
                stage_states[player_steppos].est_hero.pos(),
                ctl.pos(),
            ],
            [stage_states[suiv_coord(lock_steppos)].est_coffre.neg()],
        )
        keep_conditions = regle_ou_condition(
            # Coffre non supprimé si action illégale
            [
                has_key.pos(),
                stage_states[player_steppos].est_hero.pos(),
                ctl.neg(),
                stage_states[lock_steppos].est_coffre.pos(),
            ],
            [stage_states[suiv_coord(lock_steppos)].est_coffre.pos()],
        ) + regle_ou_condition(
            # Coffre non supprimé si le joueur
            # n'est pas en train de rentrer dans le coffre
            [
                has_key.pos(),
                stage_states[player_steppos].est_hero.neg(),
                ctl.pos(),
                stage_states[lock_steppos].est_coffre.pos(),
            ],
            [stage_states[suiv_coord(lock_steppos)].est_coffre.pos()],
        )
        return unlock_condition + keep_conditions

    for steppos, _ in stage_states.items():
        next_steppos = suiv_coord(steppos)
        if not compatible_position(next_steppos, stage_data):
            next_steppos = steppos

        # Ajoute la variable proche du coffre si la prochaine case est un coffre
        problem.add_clauses(
            regle_ou_condition(
                [stage_states[next_steppos].est_coffre.pos()],
                [stage_states[steppos].est_proche_coffre.pos()],
            )
        )
        problem.add_clauses(
            regle_ou_condition(
                [stage_states[next_steppos].est_coffre.neg()],
                [stage_states[steppos].est_proche_coffre.neg()],
            )
        )

    for (x_coord, y_coord) in get_lock_positions(stage_data):
        for step in range(1, stage_data["max_steps"] + 1):
            steppos = (step, x_coord, y_coord)
            # Ne supprime pas le coffre si pas de clé
            problem.add_clauses(
                regle_ou_condition(
                    [aux_states.cle[step].neg()],
                    [
                        stage_states.get(steppos).est_coffre.pos(),
                        stage_states.get(suiv_coord(steppos)).est_coffre.pos(),
                    ],
                )
            )
            # Si le coffre supprimé à n, n+1 aussi supprimé
            problem.add_clauses(
                regle_ou_condition(
                    [stage_states[steppos].est_coffre.neg()],
                    [stage_states.get(suiv_coord(steppos)).est_coffre.neg()],
                )
            )
            problem.add_clauses(
                regle_ou_condition(
                    [
                        stage_states[steppos].est_hero.neg()
                        for steppos in get_close_cells(
                        step, x_coord, y_coord, stage_data
                    )
                    ]
                    + [stage_states[steppos].est_coffre.pos()],
                    [stage_states.get(suiv_coord(steppos)).est_coffre.pos()],
                )
            )

            control = control_states[step]
            steppos_left = (step, x_coord - 1, y_coord)
            steppos_right = (step, x_coord + 1, y_coord)
            steppos_up = (step, x_coord, y_coord - 1)
            steppos_down = (step, x_coord, y_coord + 1)

            problem.add_clauses(
                gen_unlock_rule(control.is_right, steppos, steppos_left)
            )
            problem.add_clauses(
                gen_unlock_rule(control.is_left, steppos, steppos_right)
            )
            problem.add_clauses(gen_unlock_rule(control.is_down, steppos, steppos_up))
            problem.add_clauses(gen_unlock_rule(control.is_up, steppos, steppos_down))


def main():
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    import time
    start_time = time.time()

    # récupération de la grille et de toutes les infos
    infos = grid_from_file(filename)

    problem = generate_problem(infos)
    problem.solve()
    res = ""
    for action in problem.get_solution():
        res += action
    print(res)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res


if __name__ == "__main__":
    main()
