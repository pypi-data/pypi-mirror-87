#-----------------------
# @author: Tony Ribeiro
# @created: 2019/11/06
# @updated: 2019/11/06
#
# @desc: simple Probabilizer implementation, for Learning from probabilistic states transitions.
#   - INPUT: a set of pairs of discrete multi-valued states
#   - OUTPUT: multiple set of minimal rules which together realize only the input transitions
#   - THEORY:
#       - NEW
#   - COMPLEXITY:
#       - Variables: exponential or polynomial
#       - Values: exponential or polynomial
#       - Observations: polynomial
#-----------------------

from ..utils import eprint
from ..objects.rule import Rule
from ..objects.logicProgram import LogicProgram
from ..algorithms.gula import GULA
from ..algorithms.pride import PRIDE
from ..algorithms.synchronizer import Synchronizer
import csv

import itertools
import math

class Probabilizer:
    """
    Define a simple complete version of the Synchronizer algorithm.
    Learn logic rules that explain sequences of state transitions
    of a dynamic system:
        - discrete
        - non-deterministic
        - semantic constraint rules
    INPUT: a set of pairs of states
    OUTPUT: a logic programs
    """

    @staticmethod
    def fit(variables, values, transitions, complete=True, synchronous_independant=True):
        """
        Preprocess transitions and learn rules for all variables/values.

        Args:
            variables: list of string
                variables of the system
            values: list of list of string
                possible value of each variable
            transitions: list of (list of int, list of int)
                state transitions of a dynamic system

        Returns:
            LogicProgram
                - each rules are minimals
                - the output set explains/reproduces the input transitions
        """
        #eprint("Start LUST learning...")

        # Nothing to learn
        #if len(transitions) == 0:
        #    return [LogicProgram(variables, values, [])]

        #eprint("Raw transitions:", input)

        encoded_input = Probabilizer.encode(transitions, synchronous_independant)
        conclusion_values = Probabilizer.conclusion_values(variables, encoded_input)

        # DBG
        eprint("total encoded transitions: ",len(encoded_input))

        #for i in encoded_input:
        #    eprint(i)
        #exit()

        #eprint("Variables:", variables)
        #eprint("Condition values:", values)
        #eprint("Conclusion values:", conclusion_values)

        # Encode transition with id of values
        for (i,j) in encoded_input:
            for var in range(0,len(j)):
                for val_id in range(0,len(conclusion_values[var])):
                    if conclusion_values[var][val_id] == j[var]:
                        j[var] = val_id
                        break

        #eprint("Conclusion value ID encoded transitions:", encoded_input)

        if synchronous_independant:
            if complete:
                model = GULA.fit(variables, values, encoded_input, conclusion_values)
            else:
                model = PRIDE.fit(variables, values, encoded_input)
        else:
            model = Synchronizer.fit(variables, values, encoded_input, conclusion_values, complete)

        output = LogicProgram(variables, values, model.get_rules(), model.get_constraints(), conclusion_values)

        #eprint("Probabilizer output raw: \n", output.to_string())
        #eprint("Probabilizer output logic form: \n", output.logic_form())

        return output, conclusion_values

    def encode(transitions, synchronous_independant=True):
        # Extract occurences of each transition
        next_states = dict()
        nb_transitions_from = dict()
        for (i,j) in transitions:
            s_i = tuple(i)
            s_j = tuple(j)
            # new init state
            if s_i not in next_states:
                next_states[s_i] = dict()
                nb_transitions_from[s_i] = 0
            # new next state
            if s_j not in next_states[s_i]:
                next_states[s_i][s_j] = (s_i,s_j,0)

            (_, _, p) = next_states[s_i][s_j]
            next_states[s_i][s_j] = (s_i,s_j,p+1)
            nb_transitions_from[s_i] += 1

        #eprint("Transitions counts:", next_states)

        # Extract probability of each transition
        #for s_i in next_states:
        #    for s_j in next_states[s_i]:
        #        (i, j, p) = next_states[s_i][s_j]
                #next_states[s_i][s_j] = (i, j, p / nb_transitions_from[s_i])
        #        next_states[s_i][s_j] = (i, j, p)

        #eprint("Transitions ratio:", next_states)

        # Encode probability locally
        encoded_input = []
        for s_i in next_states:
            if synchronous_independant:
                local_proba = dict()
                for s_j in next_states[s_i]: # For each transition
                    (_, j, p) = next_states[s_i][s_j]
                    for var in range(0,len(j)): # for each variable
                        if var not in local_proba:
                            local_proba[var] = dict()
                        if j[var] not in local_proba[var]: # for each value
                            #local_proba[var][j[var]] = 0.0
                            local_proba[var][j[var]] = 0

                        local_proba[var][j[var]] += p # accumulate probability

            # DBG
            #print("local proba:",local_proba)
            for s_j in next_states[s_i]: # For each transition
                (i, j, p) = next_states[s_i][s_j]
                # DBG
                #print(j)
                if synchronous_independant: # state proba is the product of local proba
                    encoded_j = [
                    str(j[var])+
                    ","+
                    str(int(local_proba[var][j[var]]/math.gcd(local_proba[var][j[var]],nb_transitions_from[s_i])))+
                    "/"+str(int(nb_transitions_from[s_i]/math.gcd(local_proba[var][j[var]],nb_transitions_from[s_i])))
                    for var in range(0,len(j))]
                else: # state probability is independant
                    encoded_j = [
                    str(j[var])+
                    ","+
                    str(int(p/math.gcd(p,nb_transitions_from[s_i])))+
                    "/"+str(int(nb_transitions_from[s_i]/math.gcd(p,nb_transitions_from[s_i])))
                    for var in range(0,len(j))]
                encoded_input.append([i,encoded_j])

        #eprint("String encoded transitions:", encoded_input)

        return encoded_input

    def conclusion_values(variables, transitions):
        conclusion_values = []

        # Extract each variable possible value
        for var in range(0,len(variables)):
            domain = []
            for (i,j) in transitions:
                if j[var] not in domain:
                    domain.append(j[var])
            conclusion_values.append(domain)

        return conclusion_values
