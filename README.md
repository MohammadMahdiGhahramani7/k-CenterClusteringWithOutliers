# k-CenterClusteringWithOutliers, Big Data
K-Center Clustering With Outliers
k-center with z outliers problem, that is, the robust version of the k-center problem which is useful in the analysis of noisy data (a quite common scenario in big data computing). Given a set P of points and two integers k and z, the problem requires to determine a set S ⊂ P of k centers which minimize the maximum distance of a point of P-Z from S, where Z are the z farthest points of P from S. In other words, with respect to the standard k-center problem, in the k-center with z outliers problem, we are allowed to disregard the z farthest points from S in the objective function. Unfortunately, the solution of this problem turns out much harder than the one of the standard k-center problem. The 3-approximation sequential algorithm by Charikar et al. for k-center with z outliers, which we call kcenterOUT, is simple to implement but has superlinear complexity (more than quadratic, unless sophisticated data structures are used)

How to run the code:

#### "python k_center_outliers.py filepath k z" 
##### k: number of clusters.
##### z: number of outliers allowed to be disregarded.
\
\
Example answers:

#### python k_center_outliers.py testdataHW2.txt 3 3

###### Input size n = 15
###### Number of centers k = 3
###### Number of outliers z = 3
###### Initial guess = 0.04999999999999999
###### Final guess = 0.04999999999999999
###### Number of guesses = 1
###### Objective function = 0.14142135623730964
###### Time of SeqWeightedOutliers = 0.14209747314453125

#### python k_center_outliers.py testdataHW2.txt 3 1

###### Input size n = 15
###### Number of centers k = 3
###### Number of outliers z = 1
###### Initial guess = 0.04999999999999999
###### Final guess = 0.7999999999999998
###### Number of guesses = 5
###### Objective function = 1.562049935181331
###### Time of SeqWeightedOutliers = 0.5886554718017578

#### python k_center_outliers.py testdataHW2.txt 3 0

###### Input size n = 15
###### Number of centers k = 3
###### Number of outliers z = 0
###### Initial guess = 0.04999999999999999
###### Final guess = 1.5999999999999996
###### Number of guesses = 6
###### Objective function = 4.242640687119285
###### Time of SeqWeightedOutliers = 0.6442070007324219

#### python k_center_outliers.py uber-small.csv 10 100

###### Input size n = 959
###### Number of centers k = 10
###### Number of outliers z = 100
###### Initial guess = 0.00011180339887711215
###### Final guess = 0.007155417528135178
###### Number of guesses = 7
###### Objective function = 0.02143944961980124
###### Time of SeqWeightedOutliers = 3989.88676071167
