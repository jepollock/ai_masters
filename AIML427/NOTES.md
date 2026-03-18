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

