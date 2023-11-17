from finiteAutomaton import FiniteAutomaton
def print_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(str(content))

def print_menu():
    print("1. Print states.")
    print("2. Print alphabet.")
    print("3. Print final states.")
    print("4. Print transitions.")
    print("5. Print initial state.")
    print("6. Print is deterministic.")
    print("7. Check if sequence is accepted by DFA.")
    print("8. Exit")

def options_for_dfa():
    finite_automaton = FiniteAutomaton("fa.in")

    print("FA read from file.")
    print_menu()
    print("Your option: ")

    option = int(input())

    while option != 0:
        if option == 1:
            print("Final states: ")
            print(finite_automaton.get_states())
            print()
        elif option == 2:
            print("Alphabet: ")
            print(finite_automaton.get_alphabet())
            print()
        elif option == 3:
            print("Final states: ")
            print(finite_automaton.get_final_states())
            print()
        elif option == 4:
            print(finite_automaton.write_transitions())
        elif option == 5:
            print("Initial state: ")
            print(finite_automaton.get_initial_state())
            print()
        elif option == 6:
            print("Is deterministic?")
            print(finite_automaton.check_if_deterministic())
        elif option == 7:
            print("Sequence: ")
            sequence = input()
            if finite_automaton.check_sequence(sequence):
                print("Sequence is valid")
            else:
                print("Invalid sequence")
        elif option == 8:
            return
        else:
            print("Invalid command!")

        print()
        print_menu()
        print("Your option: ")
        option = int(input())

if __name__ == "__main__":
    options_for_dfa()
