class KTapeTuringMachine:
    #class attributes
    def __init__(self, num_tapes, states, input_alphabet, tape_alphabet, 
                 transition_function, start_state, accept_state, reject_state):
        self.num_tapes = num_tapes
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        
    #set up tapes
    def initialize_tapes(self, input_string):
        blank_symbol = '_'
        #store tapes
        tapes = []
        for i in range(self.num_tapes):
            if i == 0:
                tape = ['_'] + list(input_string) + [blank_symbol]  #leading blank
            else:
                tape = [blank_symbol] * (len(input_string) + 2)
            tapes.append(tape)
        return tapes
    
    #run tape machine
    def simulate(self, input_string, verbose=False):
        tapes = self.initialize_tapes(input_string)
        head_positions = [1] * self.num_tapes  
        current_state = self.start_state
        step = 0
        
        #print initial tape configurations and state
        if verbose:
            print(f"Step {step}:")
            for i in range(self.num_tapes):
                #Remove leading blank in output
                tape_str = ''.join(tapes[i][1:head_positions[i]] + 
                                 [f"[{tapes[i][head_positions[i]]}]"] + 
                                 tapes[i][head_positions[i]+1:])
                print(f"Tape {i+1}: {tape_str}")
            print(f"Current state: {current_state}")
            print()
            
        #continue simulating until the machine halts in an accepting or rejecting state
        while current_state not in [self.accept_state, self.reject_state]:
            if self.num_tapes == 1:
                current_symbols = tapes[0][head_positions[0]]
                transition_key = (current_state, current_symbols)
            else:
                current_symbols = tuple(tapes[i][head_positions[i]] for i in range(self.num_tapes))
                transition_key = (current_state, current_symbols)

            #check if there is a valid transition for the current state and symbols
            if transition_key not in self.transition_function:
                current_state = self.reject_state
                break
                
            next_state, write_symbols, move_directions = self.transition_function[transition_key]
            
            #update the tapes based on the transition rules
            if self.num_tapes == 1:
                tapes[0][head_positions[0]] = write_symbols
                if move_directions == 'R':
                    head_positions[0] += 1
                    if head_positions[0] >= len(tapes[0]):
                        tapes[0].append('_')
                elif move_directions == 'L':
                    head_positions[0] = max(0, head_positions[0] - 1)
            else:
                for i in range(self.num_tapes):
                    tapes[i][head_positions[i]] = write_symbols[i]
                    if move_directions[i] == 'R':
                        head_positions[i] += 1
                        if head_positions[i] >= len(tapes[i]):
                            tapes[i].append('_')
                    elif move_directions[i] == 'L':
                        head_positions[i] = max(0, head_positions[i] - 1)
            
            #update the current state after the transition
            current_state = next_state
            step += 1

            #print the tape configurations and state at each step
            if verbose:
                print(f"Step {step}:")
                for i in range(self.num_tapes):
                    # Don't show leading blank in output
                    tape_str = ''.join(tapes[i][1:head_positions[i]] + 
                                     [f"[{tapes[i][head_positions[i]]}]"] + 
                                     tapes[i][head_positions[i]+1:])
                    print(f"Tape {i+1}: {tape_str}")
                print(f"Current state: {current_state}")
                print()
                
        #print the result based on the final state and whether it is accepting or rejecting
        if verbose:
            if current_state == self.accept_state:
                #accept
                print("ACCEPT: Halted in accepting state qaccept")
            else:
                #reject
                print("REJECT: Halted in rejecting state qreject")
        
        return current_state == self.accept_state