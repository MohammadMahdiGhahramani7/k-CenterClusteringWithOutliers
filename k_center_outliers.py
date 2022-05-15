import os
import sys
import time
import math


def readVectorsSeq(filename):
    with open(filename) as f:
        result = [tuple(map(float, i.split(','))) for i in f]
    return result
    
    
def euclidean(point1,point2):
    res = 0
    for i in range(len(point1)):
        diff = (point1[i]-point2[i])
        res +=  diff*diff
    return math.sqrt(res)
    
    
def distanceCalculator(points):
  '''
  This function compute the pairwise distances between points and save them
  in a 2-d matrix. This matrix is similar to adjacency matrix for graphs. The 
  output matrix has the following features:
  a) M[i][i] = 0 for all i in P
  b) M[i][j] = M[j][i]
  c) M[i][j] + M[j][k] >= M[i][k] => since we use euclidean distance
  '''
  
  dis_matrix = [[float('inf') for _ in range(len(points))] for _ in range(len(points))]
  for i in range(len(points)):
    for j in range(i+1, len(points)):
      dis_matrix[i][j] = euclidean(points[i], points[j])
      dis_matrix[j][i] = dis_matrix[i][j]
  return dis_matrix


def ball(Z, idx_x, r, W, W_status=True):
  '''
  This function receives an arguman W_status determining whether we
  wish to compute the coressponding total weight or not. It is useful
  since it avoids extra computations when calculating ball-weight variable.
  '''

  if W_status:
    result = [Z[idx_x]] #Each center covers itself first.
    weight = 1
    for idx_point in range(len(Z)):
      if dist_matrix[idx_x][idx_point] <= r and Z[idx_point] != 0:
        result.append(Z[idx_point])
        if W_status: weight += W[idx_point] 
    return (result, weight)
    
  else:
    result = [Z[idx_x]] #Each center covers itself first.
    for idx_point in range(len(Z)):
      if dist_matrix[idx_x][idx_point] <= r and Z[idx_point] != 0:
        result.append(Z[idx_point])
    return result
  

def SeqWeightedOutliers(P,W,k,z,alpha):

  kPluszPlus1 = k + z + 1
  r = min(list(map(lambda x: min(x[:kPluszPlus1]), dist_matrix[:kPluszPlus1])))/2
  number_of_guesses = 0
  print(f"Initial guess = {r}")
  while True:
    number_of_guesses += 1
    Z, S, Wz = P.copy(), [], sum(W)
    S_idx = [] #This extra variable contains the indexes associated to the points in S.
    # Considering this variable is useful because it avoids extra computations relating to
    # distance calculation. Instead of computing the distance(whenever it is required), we
    # can simply use dist_matrix variable on a particular set of indexes. This indexes are
    # taken from this variable.
    Z_copy = Z.copy() # It is needed because when we change r -> 2*r, the value of Z should
    # reset. Apart from that, since the value of Z changes after each iteration(Z.remove(sth)),
    # the indexes in Z are not unchanged. However, if we want to take advantage of dist_matrix to
    # avoids extra computations, we need fixed indexes. That is why when we use Z.remove(y)
    # we set Z_copy[location_y] = 0 to avoid index problem and make it easier to use 
    # dist_matrix in the body of ball function.
    while len(S) < k and Wz > 0:
      maximum = 0
      for idx_x in range(len(P)):
        _, ball_weight = ball(Z_copy, idx_x, (1 + 2*alpha)*r, W)
        if ball_weight > maximum and P[idx_x] in Z: # The second condition is useful when
        # the initial r is so small that each point can only find itself in its circle.
        # If we do not consider this condition, the code will always select the first point 
        # and do not switch to other points.
          maximum = ball_weight
          newcenter = P[idx_x]
          newcenter_idx = idx_x # As mentioned before, to take advantage of dist_matrix we need
          # indexes and not points.
      S.append(newcenter)
      S_idx.append(newcenter_idx)
      larger_ball = ball(Z_copy, newcenter_idx, (3 + 4*alpha)*r, W, False)
      for y in larger_ball:
        location_y = Z_copy.index(y)
        Z.remove(y)
        Z_copy[location_y] = 0 # We set the value of the corresponding index of y to 0 and
        # we take care of it in the body of the ball function when we check 
        # "... and Z[idx_point] != 0" in if statement.
        Wz -= W[location_y]
    if Wz <= z:
      print(f"Final guess = {r}")
      print(f"Number of guesses = {number_of_guesses}")
      return (S, S_idx) # S_idx will be useful when computing the objective function
    else:
      r *= 2


def ComputeObjective(P,S,z): #To be more efficient, instead of S=solution we call the function
  # with S=idx_solution (taking advantage of dist_matrix).
  DISTANCES = []
  for idx_point in range(len(P)):
    if idx_point not in S: #We do not consider centers since their distance from
    # their closest center is 0.
      minimum = float('inf')
      for idx in S:
        distance = dist_matrix[idx][idx_point]
        if distance < minimum:
          minimum = distance
      DISTANCES.append(minimum)
  return sorted(DISTANCES)[-z-1] #exclude the z largest distances and return the largest
  # among the remaining ones.


def main():
  assert len(sys.argv[1:]) == 3, "Usage: python3 G103HW2.py <file_path> <k> <z>"	
  global k, z
  path, k, z = sys.argv[1:]
  assert os.path.isfile(path), "File or folder not found"
  assert k.isdigit() and z.isdigit(), "k and z must be both integers"
  k, z = int(k), int(z)
  inputPoints = readVectorsSeq(path)
  print(f"Input size n = {len(inputPoints)}")
  print(f"Number of centers k = {k}")
  print(f"Number of outliers z = {z}")
  weights = [1 for _ in range(len(inputPoints))]
  global dist_matrix #We define it global to be also used in other functions
  # whenever it is needed.
  dist_matrix = distanceCalculator(inputPoints)
  start = time.time()
  solution, idx_solution = SeqWeightedOutliers(inputPoints,weights,k,z,0)
  end = time.time()
  duration = end - start
  objective = ComputeObjective(inputPoints,idx_solution,z)#To be more efficient, instead of S=solution we call the function
  # with S=idx_solution (taking advantage of dist_matrix).
  print(f"Objective function = {objective}")
  print(f"Time of SeqWeightedOutliers = {1e3 * duration}")
  
  
if __name__ == "__main__":
  main()
# LAST COMMENT: This code focuses more on indexes, instead of values.
# For example, we do not use "solution" variable to compute objective
# function. It instead uses idx_solution with the aim of exploiting
# dist_matrix to avoid extra computations. This consideration helps
# the code to get executed even faster than sample answers for artificial9000.txt
# dataset, reported on Moodle.
# Code Execution Time               Execution Time Reported on Moodle(Python)
# ----------------------------------------------------------------------------
#  426886.6319656372                   544602.6632785797 (9200, 9, 300)
#  335746.69647216797                  382610.8775138855 (9200, 9, 200)
#  167138.81397247314                  169261.5430355072 (9200, 9, 0)
