class FiniteAutomaton:

    def __init__(self, file_path):
        self.elem_separator = ";"
        self.is_deterministic = False
        self.initial_state = ""
        self.states = []
        self.alphabet = []
        self.final_states = []
        self.transitions = {}
        self.read_from_file(file_path)

    def read_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.states = file.readline().strip().split(self.elem_separator)
            self.initial_state = file.readline().strip()
            self.alphabet = file.readline().strip().split(self.elem_separator)
            self.final_states = file.readline().strip().split(self.elem_separator)

            for line in file:
                transition_components = line.strip().split(" ")

                if (transition_components[0] in self.states and
                        transition_components[2] in self.states and
                        transition_components[1] in self.alphabet):
                    transition_states = (transition_components[0], transition_components[1])

                    if transition_states not in self.transitions:
                        self.transitions[transition_states] = {transition_components[2]}
                    else:
                        self.transitions[transition_states].add(transition_components[2])

        self.is_deterministic = self.check_if_deterministic()

    def check_if_deterministic(self):
        return all(len(states) <= 1 for states in self.transitions.values())

    def get_states(self):
        return self.states

    def get_initial_state(self):
        return self.initial_state

    def get_alphabet(self):
        return self.alphabet

    def get_final_states(self):
        return self.final_states

    def get_transitions(self):
        return self.transitions

    def write_transitions(self):
        result = "Transitions: \n"
        for (state, symbol), next_states in self.transitions.items():
            result += f"<{state},{symbol}> -> {next_states}\n"
        return result

    def check_sequence(self, sequence):
        if not sequence:
            return self.initial_state in self.final_states

        state = self.initial_state
        for symbol in sequence:
            transition_key = (state, symbol)
            if transition_key in self.transitions:
                state = next(iter(self.transitions[transition_key]))
            else:
                return False

        return state in self.final_states

