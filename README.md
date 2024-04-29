# DNA-Challenge

## Code

### Build()

Input: length, bases, gc_content

Randomly picks bases appends them to a list to make a sequence until the length matches the input length. The function also takes GC Content as a parameter, biasing the random selection of bases.

Output: list of bases

### spot_homoplymer_runs()

Input: sequence, number of consecutive bases before a run is defined (3 by default)

The function uses a sliding-window approach, iterating through the bases, for each base (i) the function iterates again (j) until i != j if at any point j - i is greater then the run length then all bases are appended to a list.

Output: returns a list with the index position of all run bases.

### add_errors()

Input: sequence, error rate, homo polymer error rate, homo polymer run locations

Defines 3 subfunctions (add_insertion, add_deletion, add_mismatch). The function loops through all N bases in the sequence giving it a random chance of being "mutated", this likelihood increases as the bases index increases meaning that the last index is N times more likely to be mutated. Next the function loops through the indexes containing homopolymer runs and randomly assigned bases (based on the homopolymer error rate) into either a deletion or an insertion only. 

Output: modified sequence and a list containing the mutation types and indexes.

## Graphs

### plot_sequence_length_per_error_rate



<img width="1509" alt="Screenshot 2024-04-29 at 14 57 29" src="https://github.com/Luc656/DNA-Challenge/assets/94873030/883e2562-f276-4f64-83f4-7a63fb44cbbf">


This graph plots the distribution of sequence lengths of the 100 sets in each different error rate category. Given that all sequences are based of the template of length 100, and the errors are randomly assigned to insertions (length increases by 1), deletions (length decreases by 1) and mismatch (no length change) we can expect the sample lengths to be normally distributed around a mean of 100. This graph supports this hypothesis and also shows that as the error rate increases the variance of the sequence lengths increases also, due to having an increased number of errors in the sequence.


### plot_gc_content_per_error_rate

![gc](https://github.com/Luc656/DNA-Challenge/assets/94873030/4b21e368-a199-4976-b20a-258ddbbea538)


This graph shows how the GC content is distributed among the 100 sets of sequences for each error rate. Given that the template sequence starts at 60% we could expect the GC contents of the copied sequences to be distributed around this mark. However, because each insertion and mismatch is randomly assigned to new based all with equal likelihood and because G and C bases make up more of the template sequence and hence are more likely to be removed we can expect this GC content to trend back towards 50%, with the trend becoming stronger at higher error rates.


### plot_error_position_per_error_type

![graph3](https://github.com/Luc656/DNA-Challenge/assets/94873030/fa56c1da-dc6f-4461-a8aa-a904ea23359e)


This graph plots the error position distribution for all error rates per error type. Due to the fact that in our template sequence errors become increasingly more likely as we iterate through the sequence we can expect most non homopolymer related errors to be distributed at the end of the sequence, this graph support this hypothesis. In addition, homo polymer runs only occur at certain positions in the template sequence, we can see where these are in the sequence by looking at their error distribution, these were also randomly sampled for error insertion hence a more even distribution than the other error types.


### plot_run_length_ratio_per_nucleotide_per_error_rate

![Screenshot 2024-04-29 at 16 46 44](https://github.com/Luc656/DNA-Challenge/assets/94873030/02c1456e-69ac-4c6b-b3d1-3e9e33a735fb)


This graph plots the distributions of total sequence length that is made up by homopolymer runs per base per error rate for all sequence copies. For bases G and C we see larger proportions of the sequences are made up of their respective homopolymers. This is likely because the template strand has 60% GC content increasing the likelihood of these bases appearing together in the sequence.

### plot_homopolymer_positions_per_error_rate_per_nucleotide

<img width="801" alt="Screenshot 2024-04-29 at 16 20 45" src="https://github.com/Luc656/DNA-Challenge/assets/94873030/140719ac-0d34-4575-b664-8b9e45fe435a">

Here we can see for each nucleotide the distribution of their homopolymer runs split by error rate. Because each copy is based off the same template they all start off with runs in the same locations, this means that for all samples the distribution tends to be similar. Note also the differences in the scale of the Y axes, we can assume this occurs because in the template sequence only runs of T and G were found. Here we could possibly expect that as the error rate increases the run frequency decreases as more errors might allow for certain runs to be transformed into non-run sequences (TTT) -> (TTG). Where no runs existed in the template (A and C) we can expect to see an increase in run frequency as the error rate increases, the plausable explanation for this is that with more errors occuring the chance of a run being created (AAG) -> (AAA) increases.
