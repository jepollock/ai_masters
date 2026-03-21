# Toward Integrating Feature Selection Algorithms for Classification and Clustering

@article{subsetcover,
author = {Liu, Huan and Yu, Lei},
year = {2005},
month = {04},
pages = {491-502},
title = {Yu, L.: Toward Integrating Feature Selection Algorithm for Classification and Clustering. IEEE Transaction on Knowledge and Data Engineering 17(4), 491-502},
volume = {17},
journal = {IEEE Transactions on Knowledge and Data Engineering - TKDE},
doi = {10.1109/TKDE.2005.66}
}towar

Subset Generation => Subset Evaluation => Goodness => Exit if yes. Otherwise back to next subset.

Complete Search - beam search is a complete search - no.

Simulated annealing as a subset search?

Proposes a method of deciding _which_ algorithm to use for feature selection.

Generally, start with set-cover and if it is small, search from empty.
If it is large, search backwards - 
If the resulting set is larger than the set cover, choose the set cover.



@article{article,
author = {Kohavi, Ron and John, George},
year = {1997},
month = {12},
pages = {273-324},
title = {Wrappers for Feature Subset Selection},
volume = {97},
journal = {Artificial Intelligence},
doi = {10.1016/S0004-3702(97)00043-X}
}

Wrappers for Feature Subset Selection

Says, watch out for redundancy measures because 1-hots will all show
as redundant. This is from the probability based definitions, and how
they end up conflicting. Brings in the definition of "weakly relevant",
which says X is weakly relevant if there is a subset + x that is better
at predicting Y than the subset alone.

--- This is where search comes from.

However, there's some additional warnings - model might perform better if a strong feature is removed - e.g. (x1 & x2) | x3

When looking at {x2, x3}, removing x2 will improve performance.

Woah, the converse might also be true, irrelevant features may improve performance.

Need recursive references.

Filter algorithms:

FOCUS - complete search, examining all subsets.

Relief - randomized search, uses "relevance"

DecisionTree - problem - might not find the appropriate set for the actual model. Restricted subset search - since it's binary, it's based on the height, so O(lg(m)) However, this is embedded? Not really, only if the final model is a DecisionTree.

Wrapper search algorithms - hill-climbing search: this document describes forward-search, greedy.

This also has BestFirstSearch, which is very strange and poorly described?

There is a high risk of overfitting if using k-fold cross validation in feature selection. Keep a separate holdout set for another run of k-fold cross validation in a final training run, or better yet, a test set.


Multiple Reference Points-Based Decomposition for
Multiobjective Feature Selection in Classification:
Static and Dynamic Mechanisms

@article{article,
author = {Nguyen, Bach and Xue, Bing and Andreae, Peter and Ishibuchi, Hisao and Zhang, Mengjie},
year = {2019},
month = {04},
pages = {1-1},
title = {Multiple Reference Points-Based Decomposition for Multiobjective Feature Selection in Classification: Static and Dynamic Mechanisms},
volume = {PP},
journal = {IEEE Transactions on Evolutionary Computation},
doi = {10.1109/TEVC.2019.2913831}
}


@article{article,
author = {Guyon, Isabelle and Elisseeff, André},
year = {2003},
month = {01},
pages = {1157 - 1182},
title = {An Introduction of Variable and Feature Selection},
volume = {3},
journal = {J. Machine Learning Research Special Issue on Variable and Feature Selection},
doi = {10.1162/153244303322753616}
}

An Introduction to Variable and Feature Selection

Filter method - Variable Ranking

The Correlation criteria - Pearson correlaion coefficient.

show equation here.
R(i)^2 provides a ranking. Sort descending, pick to the top.
Only detects linear dependencies - slope of a line.
To detect others, pre-apply mutations and add those features to the 
pile (lg, 1/x, x^2, sqrt(x))
f
MutualInformation as ranking criteria

Continue here.

Not much else, over my head.





@article{article,
author = {Kim, Sb and Rattakorn, Panaya},
year = {2011},
month = {05},
pages = {5704-5710},
title = {Unsupervised feature selection using weighted principal components},
volume = {38},
journal = {Expert Syst. Appl.},
doi = {10.1016/j.eswa.2010.10.063}
}

https://www.sciencedirect.com/science/article/pii/S0957417410012078

Unsupervised feature selection using weighted principal components

Other information: https://stats.stackexchange.com/questions/27300/using-principal-component-analysis-pca-for-feature-selection#:~:text=The%20basic%20idea%20when%20using,regression%20(or%20PLS%20regression).


Feature Selection for Classification


@article{7cee3d47ab9c42afa0831ca4232aa803,
title = "Feature selection for classification",
keywords = "Classification, Feature selection, Framework",
author = "M. Dash and H. Liu",
year = "1997",
doi = "10.1016/s1088-467x(97)00008-5",
language = "English (US)",
volume = "1",
pages = "131--156",
journal = "Intelligent Data Analysis",
issn = "1088-467X",
publisher = "SAGE Publications Ltd",
number = "3",
}

Subset search algorithms

These backtrack...

branch and bound, "best first search", and beam search

Evaluation Functions - 
 InformationMeasures is basically a DecisionTree - it uses InformationGain and ranks the features.
 Distance Measures - don't understand this one -linear fit?
   No, it's Relief, like KNN, but for feature selection.
   It selects for features that best indicate class boundaries -> f(x) vs f(x1) => class change.
   requires euclidean distances, so normalized data.
 Dependence Measures - variance, covariance?
 
 
 




==========

Embedded - SVM and DecisionTree, SVM creates new features, DecisionTree learns the subset.

Wrapper - has search engines - this is where SFFS and SBS appear.





CFS - Filter method with subset search algorithm.
    - uses Information Gain for categorization data.
	- uses both information gain (discrete) and Pearson's Correlation (continuous)
	- since 


KNIME work

1) train Naive Bayes on train.csv and test on test.csv - report train/test accuracy

Training accuracy: 82.86%
Testing accuracy: 80.19%

2) split using specific seed 202203 70/30 and redo
3) Discuss the results.

Training accuracy: 86.12
Testing accuracy: 85.85

This new seed performs better than the previous split. This shows the algorithm is sensitive to the seed, and we should explore this using k-cv and multiple seeds to find the variation/std deviation. The algorithm may be unstable in the inclusion of a particular row in the training data.

4) Use SFS wrapping NB with default settings on whole dataset.
   what is selected. what is wrong - NO TEST SET!

F1-5, F7, F9, F11, F13, F15, F22-28

Since there wasn't a test/train split, this will bias the model. We won't know if the model generalizes well because the feature set was generated from data we would later use to test it.




   
5) Use the selected features in (4) and transfort training + test set. Compare with 1(a), why is there a difference? Answer:There may be bias from the test data, resulting in the model overfitting the dataset.

Training Accuracy: 91.02%
Test Accuracy: 89.62%

The change on Training accuracy is because noisy features are removed, allowing the better signal to be retrieved.


6) Repeat 4+5 using the training set.

Training Accuracy: 91.43%
Test Accuracy: 89.62%

It selected many fewer features - F3,4,7,23 for no loss in test accuracy.


7) Now do a C4.5 decision tree.

Training Accuracy: 97.55%
Testing Accuracy: 91.51%

Features selected
F2-5,F7,F9,F15,F16,F22,F23


8) Now use PCA and then do a decision tree.

Decision tree ends up more balanced.


Training Accuracy: 96.33%
Testing Accuracy: 82.08%

It fits the training data well, but doesn't generalize as well. Too much information was lost by filtering down to 5 features. Even going to 20 features doesn't reach the same quality. PCA makes this worse. Why? Feature relationships are non-linear?


9) Now use CFS

Score = Merit

Merit = sum(lookup(feature, class, correlation_table)) got it.

Remember, the corelation matrix needs to be normalized!

		sqrt(len(fs_set) + (len(fs_set)-1)*sum(lookup(feature, other features, correlation_table)))
		
	    sqrt(k + (k-1)*sum(lookup(feature, other features, correlation_table)))


lookup(feature, class, correlation_table) = 
    filter(cols = features, filter(row_id = class, correlation_matrix))
	


