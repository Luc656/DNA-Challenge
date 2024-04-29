import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import random


def build(length, bases, gc_content):
    # build the sequence of random bases

    sequence = []
    gc_content = gc_content
    at_content = 1 - gc_content
    weights = [at_content / 2, at_content / 2, gc_content / 2, gc_content / 2]

    for i in range(length):
        base = random.choices(bases, weights)[0]
        sequence.append(base)

    return sequence


def add_errors(sequence, error_rate, homopolymer_error_rate, runs):

    # track all errors and sequences created
    errors_tracker = []
    sequences_tracker = []

    bases = ['A', 'T', 'G', 'C']

    def add_insertion(index, seq):

        insertion = random.choices(bases)[0]
        seq.insert(index, insertion)

    def add_deletion(index, seq):

        del seq[index]

    def add_mismatch(index, seq):

        start_base = seq[index]
        mismatches = [base for base in bases if base != start_base]
        mismatch = random.choice(mismatches)[0]
        seq[index] = mismatch

    for _ in range(len(sequence)):
        # loop through all 100 sequences

        # create a deep copy of the template to modify
        copy = sequence.copy()

        for idx in range(len(sequence)):
            if idx in range(len(copy)) and random.random() <= error_rate * (idx / len(copy)):
                #increase the chance off errors later in the sequence

                # randomly pick a mutation
                mutations = {'Deletion': add_deletion, 'Mismatch': add_mismatch, 'Insertion': add_insertion}
                selected_mutation = random.choice(list(mutations.keys()))
                mutation_func = mutations[selected_mutation]

                # call randomly picked mutation function
                mutation_func(idx, copy)
                errors_tracker.append({'position': idx, 'error_type': selected_mutation, 'error_rate': error_rate})

        for idx in runs:
            if idx in range(len(copy)) and random.random() < homopolymer_error_rate:
                # loop through all known run locations to randomly assign errors

                mutations = {'Homopolymer Deletion': add_deletion, 'Homopolymer Insertion': add_insertion}
                selected_mutation = random.choice(list(mutations.keys()))
                mutation_func = mutations[selected_mutation]

                mutation_func(idx, copy)
                errors_tracker.append({'position': idx, 'error_type': selected_mutation, 'error_rate': error_rate})

        sequences_tracker.append(copy)

    return sequences_tracker, errors_tracker


def spot_homopolymer_runs(sequence, min_run_length=3):

    i = 0
    runs = []
    length = len(sequence)

    while i < length:
        j = i
        while j < length and sequence[i] == sequence[j]:
            j += 1
        if j - i >= min_run_length:
            for idx in range(i, j):
                runs.append(idx)
        i = j

    return runs


def plot_sequence_length_per_error_rate(error_rates, all_sequences):
    fig, ax = plt.subplots()
    for i, error_rate in enumerate(error_rates):
        # for each error rate we generate a list of all the lengths of all the sequences
        sequence_lengths = [len(seq) for seq in all_sequences[i]]
        sns.histplot(sequence_lengths, alpha=0.5, label=f'Error Rate: {error_rate}', element='poly',  multiple='stack', discrete=True, ax=ax)
    ax.set_title('Sequence Length Distribution')
    ax.set_xlabel('Sequence Length')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.show()


def plot_gc_content_per_error_rate(error_rates, all_sequences):
    fig, ax = plt.subplots()
    for i, error_rate in enumerate(error_rates):
        # only count GC bases in the sequence
        gc_content = [sum(base in 'GC' for base in seq) / len(seq) for seq in all_sequences[i]]
        sns.histplot(gc_content, alpha=0.5, label=f'Error Rate: {error_rate}', element='poly')
    ax.set_title('Sequence Length Distribution')
    ax.set_xlabel('Sequence Length')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.show()


def plot_run_length_ratio_per_nucleotide_per_error_rate(error_rates, all_sequences):
    fig, axs = plt.subplots(4, 1, figsize=(8, 10))
    bases = ['A', 'T', 'G', 'C']
    for i, error_rate in enumerate(error_rates):
        for j, base in enumerate(bases):
            # find all homo polymer run bases and filter out any not equal to the current base
            # divide this by the sequence length to gain a ratio
            homopolymer_ratios = [(len([pos for pos in spot_homopolymer_runs(seq, 3) if seq[pos] == base]) / len(seq)) for seq
                                   in all_sequences[i]]
            sns.histplot(homopolymer_ratios, bins=20, alpha=0.5, label=f'Error Rate: {error_rate}', ax=axs[j], element='step')
            axs[j].set_title(f'Homopolymer Ratio for {base}')
            axs[j].set_xlabel('Homopolymer Ratio')
            axs[j].set_ylabel('Frequency')
            axs[j].legend()
    plt.tight_layout()
    plt.show()


def plot_homopolymer_positions_per_error_rate_per_nucleotide(error_rates, all_sequences):
    fig, axs = plt.subplots(4, 1, figsize=(8, 12))
    bases = ['A', 'T', 'G', 'C']
    for i, error_rate in enumerate(error_rates):
        for j, base in enumerate(bases):
            homopolymer_positions = []
            for seq in all_sequences[i]:
                # find the positions of all homopolymer runs if equal to the current base
                positions = [pos for pos in spot_homopolymer_runs(seq, 3) if seq[pos] == base]
                homopolymer_positions.extend(positions)
            sns.histplot(homopolymer_positions, bins=20, alpha=0.5, label=f'Error Rate: {error_rate}', ax=axs[j])
            axs[j].set_title(f'Homopolymer Positions for {base}')
            axs[j].set_xlabel('Position')
            axs[j].set_ylabel('Frequency')
            axs[j].legend(bbox_to_anchor=(1, 0.75))
    plt.tight_layout()
    plt.show()


def grid_plot_hist(data, grids, x):
    grid = sns.FacetGrid(data, col=grids, col_wrap=1, height=2, aspect=3)
    unique_values = data[x].unique()
    order = np.sort(unique_values)
    grid.map(sns.countplot, x, order=order)
    grid.set_titles('{col_name}')
    axes = grid.axes.flatten()

    # simplify axes
    for ax in axes:
        ax.set_xlim(0, 100)
        ax.set_xticks(range(0, 101, 10))
        ax.set_xticklabels([str(x) for x in range(0, 101, 10)])

    plt.tight_layout()
    plt.show()


def main():

    all_sequences = []
    all_errors = []
    error_rates = [0.02, 0.05, 0.1]
    bases = ['A', 'T', 'G', 'C']

    template = build(length=100, bases=bases, gc_content=0.6)
    runs = spot_homopolymer_runs(template, 3)
    for i in error_rates:
        # build 100 copy sequences for every error rate

        copies, errors = add_errors(template, i, 0.05, runs)
        all_sequences.append(copies)
        all_errors.extend(errors)

    df = pd.DataFrame(all_errors)

    plot_sequence_length_per_error_rate(error_rates,all_sequences)
    plt.show()
    plot_gc_content_per_error_rate(error_rates, all_sequences)
    plt.show()
    grid_plot_hist(data=df,  grids='error_type', x='position')
    plt.show()
    plot_run_length_ratio_per_nucleotide_per_error_rate(error_rates, all_sequences)
    plt.show()
    plot_homopolymer_positions_per_error_rate_per_nucleotide(error_rates, all_sequences)
    plt.show()


if __name__ == '__main__':
    main()
