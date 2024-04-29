# DNA-Challenge

## Code

### Build()

Randomly picks bases Afrom A, T, C, G and appends them to a list to make a sequnce until the length matches the input length. The function also takes GC Content as a parameter, biasing the random selection of bases.

### spot_homoplymer_runs()

Takes a sequnce as input and the number of consecutive bases before a run is defined (3 by default). The function uses a sliding-window approach, iterating through the bases, for each base (i) the function iterates again (j) until i != j if at any point j - i is greatwer then the run tlength then all bases are appended to a list. The functioo returns this list with the index position of all run bases.

### add_errors()

Takes a Sequence, an error_rate, a homopolymer error rate and the location of homopolymer runs as input. Defines 3 subfunctions (add_insertion, add_deletion, add_mismatch). The function loops through all N bases in the sequence giving it a random chance of being "mutated", this  liklihood increaes as the bases index increases meaning that the last index is N times more likely to be mutated. Next the function loops through the indexes containing homopolymer runs and randomly assigned bases (based on the homopolymer error rate) into either a deletion or an insertion only. The function returns this modified sequence and a list containing the mutation types and indexes.

## Graphs

