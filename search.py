import json
from scipy import spatial
import glob
import ntpath

files = glob.glob('./shapes/*.json')

initial = []
initial_id = -1
winning_distance = 100000000000
winning_shape = []
winning_id = -1

euclid_distance = 100000000000
euc_win_shape = []
euc_win_id = -1

# pick a search reference document
starter = "./shapes/10.json"
with open(starter) as shape_file:
    shape = json.load(shape_file)
    product_id = ntpath.basename(starter).split('.')[0]
    initial_id = product_id
    initial = shape

print("starting")

# Get distances (euclidean and cosine)
for f in files:
    with open(f) as shape_file:
        shape = json.load(shape_file)
        product_id = ntpath.basename(f).split('.')[0]

        # if no starter was selected, pick one now
        if len(initial) == 0 and product_id != initial_id:
            initial_id = product_id
            initial = shape
        
        # if the product ids don't match, calculate distances
        elif product_id != initial_id:
            curr_dist = spatial.distance.cosine(initial, shape)
            if curr_dist < winning_distance:
                winning_distance = curr_dist
                winning_id = product_id
                winning_shape = shape
                print(winning_id, "takes the lead with", winning_distance)
            
            euc_dist = spatial.distance.euclidean(initial, shape)
            if euc_dist < euclid_distance:
                euclid_distance = euc_dist
                euc_win_id = product_id
                euc_win_shape = shape

print("")
print("Winners (Cosine)")
print("")
print("initial_id =", initial_id)
print("initial =", initial)
print("winning_id =", winning_id)
print("winning_shape =",winning_shape)
print("winning_distance =", winning_distance)


print("")
print("Winners (Euclidean)")
print("")
print("initial_id =",initial_id)
print("initial =", initial)
print("euc_win_id =", euc_win_id)
print("euc_win_shape =", euc_win_shape)
print("euclid_distance =", euclid_distance)
