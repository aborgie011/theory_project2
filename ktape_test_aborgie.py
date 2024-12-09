from ktape_aborgie import KTapeTuringMachine

def read_test_cases(filename):
    """Read test cases from file with #accept and #reject sections"""
    accept = []
    reject = []
    current_list = None
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '#accept':
                current_list = accept
            elif line == '#reject':
                current_list = reject
            elif line:  #skip empty lines
                current_list.append(line)
    return accept, reject

def parse_tm_definition(filename):
    """Parse TM definition file"""
    transitions = {}
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        
        #first line contains machine name and number of tapes
        header = eval(lines[0])

        #extract name and number of tapes
        name, num_tapes = header[0], header[1]  

        if num_tapes == 2:  # 2-tape machine
            #parse transition rules for 2-tape machine
            for line in lines[1:]:
                rule = eval(line)
                if len(rule) == 8:  #2-tape machine has 8 parts
                    current_state, curr_sym1, curr_sym2, next_state, write_sym1, write_sym2, dir1, dir2 = rule
                    transitions[(current_state, (curr_sym1, curr_sym2))] = (
                        next_state, 
                        (write_sym1, write_sym2), 
                        (dir1, dir2)
                    )
                else:
                    raise ValueError(f"Unexpected number of elements in rule: {len(rule)} (Expected 8 for 2-tape machine)")
        else:  # 1-tape machine
            #parse transition rules for 1-tape machine
            for line in lines[1:]:
                rule = eval(line)
                if len(rule) == 5:  #1-tape machine has 5 parts
                    current_state, current_symbol, next_state, write_symbol, direction = rule
                    transitions[(current_state, current_symbol)] = (next_state, write_symbol, direction)
                else:
                    raise ValueError(f"Unexpected number of elements in rule: {len(rule)} (Expected 5 for 1-tape machine)")

    return name, num_tapes, transitions




def create_tm_from_file(filename):
    """Create TM instance from definition file"""
    name, num_tapes, transitions = parse_tm_definition(filename)
    
    #Fixed states list - ensure all required states are included
    states = {'q0', 'q1', 'q2', 'q3', 'qaccept', 'qreject'}
    
    #build alphabets from transitions
    input_alphabet = set()
    tape_symbols = set(['_'])  #start with blank symbol
    
    for (state, symbols), (next_state, write_symbols, _) in transitions.items():
        if num_tapes == 1:
            if symbols != '_':
                input_alphabet.add(symbols)
            tape_symbols.add(symbols)
            tape_symbols.add(write_symbols)
        else:
            if isinstance(symbols, tuple):
                for symbol in symbols:
                    if symbol not in ['_', '*']:
                        input_alphabet.add(symbol)
                tape_symbols.update(s for s in symbols if s != '*')
            tape_symbols.update(s for s in write_symbols if s != '*')
    
    #add special symbols for single tape machine
    if num_tapes == 1:
        tape_symbols.update(['X', 'Y'])
    else:
        tape_symbols.add('*')
    
    return KTapeTuringMachine(
        num_tapes=num_tapes,
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_symbols,
        transition_function=transitions,
        start_state='q0',
        accept_state='qaccept',
        reject_state='qreject'
    )

#testing
def test_tm_on_inputs(tm, accept_cases, reject_cases):
    print("\nTesting accept cases:")
    for test_input in accept_cases:
        print("=" * 50)
        print(f"Running on input: {test_input}")
        print("-" * 40)
        result = tm.simulate(test_input, verbose=True)
        if not result:
            print(f"ERROR: '{test_input}' was rejected but should accept")
    
    print("\nTesting reject cases:")
    for test_input in reject_cases:
        print("=" * 50)
        print(f"Running on input: {test_input}")
        print("-" * 40)
        result = tm.simulate(test_input, verbose=True)
        if result:
            print(f"ERROR: '{test_input}' was accepted but should reject")
            
#main
def main():
    #create single-tape TM for 0s and 1s
    single_tape_tm = create_tm_from_file('input1_aborgie.txt')
    
    #check test cases
    accept_cases, reject_cases = read_test_cases('equal_01.txt')
    
    #run
    print("\nTesting Equal 0s and 1s Single Tape Turing Machine:")
    test_tm_on_inputs(single_tape_tm, accept_cases, reject_cases)

if __name__ == '__main__':
    main()