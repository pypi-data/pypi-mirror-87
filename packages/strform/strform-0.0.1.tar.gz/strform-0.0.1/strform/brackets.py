"""
[ Project STRform ]
STR sequence compression and formatting

This file contains prototype concept code developed and used in MSc and PhD projects of Yao-Yuan Liu (yliu575@aucklanduni.ac.nz)

There are two main functions in this prototype:

    Condense: Turns STR sequence into the bracketed repeat format by condensing repeat stretches
    Expand: Turns STR sequences in bracketed format to original, full strings

Alexander YY Liu | yliu575@aucklanduni.ac.nz | alex.liu@esr.cri.nz

"""

# Use find_rus and condense function from CK allele caller
def find_repeat_stretches(seq, k_range=range(3, 7)):
    """
    Version v2m2
    Given a string and motif size range, return a list of repeat stretches found in the sequence.
    Run along sequence and if a motif stretch is repeated, count the number of times the motif is repeated until run is broken.
    
    Example:
    At motif size of 4, use 2 sliding windows
    [ATAG][ATAG] - Repeat detected, start counting
    [TAGA][TAGG] - Repeat ended, stop counting
    """

    found_repeats = []
    in_run_ru = 0
    run_counter = 0
    run_start_index = 0
    for i in range(len(seq)):
        if in_run_ru > 0:
            if seq[i:i + in_run_ru] == seq[i + in_run_ru:i + in_run_ru * 2]: # Current window contents matches next window
                # If already in run, add 1 to total steps/length
                run_counter += 1
            else:
                # Current window does not match next disjunct window
                # Run broken/ended, reset counters and record motif results
                found_repeats += [(seq[run_start_index:run_start_index + in_run_ru], run_start_index, i+(in_run_ru*2)-1, ((i+(in_run_ru*2)-1) - run_start_index) / in_run_ru)]
                in_run_ru = 0
                run_counter = 0
                run_start_index = 0
        else:
            # Search for new run
            for k in k_range:
                if seq[i:i + k] == seq[i+k:i+(k*2)]: # Test if current sliding window of k contain same motif as next disjunct window 
                    # A new repeat stretch is found
                    in_run_ru = k
                    run_counter += 1
                    run_start_index = i

    # At end of sequence, end current repeat stretch if still in repeat stretch
    if in_run_ru == 1:
        # Run broken/ended, reset counters and record motif results
        found_repeats += [(seq[i:i + in_run_ru], run_start_index, len(seq), (i + run_start_index) / in_run_ru)]

    return found_repeats
    
    
def condense_repeats(seq):
    """
    Condense repeat stretches into bracketed repeat format
    :param seq: input sequence
    :return: sequence in condensed bracket format
    """
    repeat_stretches = find_repeat_stretches(seq)
    if len(repeat_stretches) == 0:
        return seq
    
    for i in range(len(repeat_stretches)):
        seq = seq.replace(repeat_stretches[i][0]*int(repeat_stretches[i][3]), '['+repeat_stretches[i][0]+']'+str(int(repeat_stretches[i][3])))

    return seq
    
    
def expand_repeats(condensed_line):
    """Expand repeat stretches in bracket representations"""
    def expand_brackets(line):
        bracket_info = line.split(']')
        return bracket_info[0]*int(bracket_info[1])

    components = condensed_line.split('[')
    return ''.join([expand_brackets(x) if ']' in x else x for x in components])
    

