DIRECTEUR

<Introduction> 

In this study, we present a novel computational method, DIRECTEUR (direct reprogramming by chemical with transcriptome utilization for regenerative medicine), to predict new combinations of small molecules by integrating heterogeneous transcriptome data for direct reprogramming (DR). We attempt to predict small molecules that replace DR-inducing transcription factors (TFs) by combinatorial optimization of DR-characteristic gene expression patterns of small molecules based on large-scale small molecule-induced transcriptome profiles and TF-induced transcriptome profiles acquired from TF-based DR experiments.

# You can run the proposed method with the following procedures:

# Combinatorial optimization of small molecules in terms of DR-characteristic gene expression patterns

Run : src/main.py

Output : results/{result}

python main.py -i {} -t {} -n {} -e {} -optD {} -tarD {} -out {} 

# You can change any parameters filling after each arguments.

-i : default = 10 # Maximum number of iterations
-t : default = 60 # Maximum execution time (sec)
-n : default = 5  # Number of elements to include in the combination.
-e : default = 3  # Number of sub objective functions
-optD : # Transcriptome data to optimize
-tarD : # Transcriptome data during Direct Reprogramming
-out : # Output file name


# Data
Transcriptome data can be changed to your own data.
Transcriptome data: Data on expression ratios in each gene before and after Direct Reprogramming

