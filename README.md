# k-CenterClusteringWithOutliers
K-Center Clustering With Outliers
k-center with z outliers problem, that is, the robust version of the k-center problem which is useful in the analysis of noisy data (a quite common scenario in big data computing). Given a set P of points and two integers k and z, the problem requires to determine a set S ⊂ P of k centers which minimize the maximum distance of a point of P-Z from S, where Z are the z farthest points of P from S. In other words, with respect to the standard k-center problem, in the k-center with z outliers problem, we are allowed to disregard the z farthest points from S in the objective function. Unfortunately, the solution of this problem turns out much harder than the one of the standard k-center problem. The 3-approximation sequential algorithm by Charikar et al. for k-center with z outliers, which we call kcenterOUT, is simple to implement but has superlinear complexity (more than quadratic, unless sophisticated data structures are used)

How to run the code:

#### "python k_center_outliers.py filepath k z" 
##### k: number of clusters 
##### z: number of outliers allowed to be disregarded.
  
