correct_secreted = [0.975,0.966,0.972,0.998,1,1] #from false_positives.py
correct_nonsecreted = [0.837,0.845,0.842,0.808,0.802,0.771] #from false_negatives.py

# Normalize each list by its sum
normalized_secreted = [x / sum(correct_secreted) for x in correct_secreted]
normalized_nonsecreted = [x / sum(correct_nonsecreted) for x in correct_nonsecreted]

# Assuming you want to combine these normalized values somehow
# For example, averaging the normalized values of corresponding positions
weights = [(ns + nns) / 2 for ns, nns in zip(normalized_secreted, normalized_nonsecreted)]


print(weights)