import random

# -------------------------------
# INPUT MATRIX
# Rows = Shingles
# Columns = Documents C1, C2, C3, C4
# -------------------------------

matrix = [
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0]
]

num_rows = len(matrix)
num_docs = len(matrix[0])

# Number of hash functions
num_hashes = 3


# --------------------------------
# Generate hash functions: ax + b
# --------------------------------

random.seed(10)

hash_functions = []

for i in range(num_hashes):
    a = random.randint(1, num_rows - 1)
    b = random.randint(0, num_rows - 1)

    hash_functions.append((a, b))


# --------------------------------
# Create Signature Matrix
# --------------------------------

signature = [
    [float('inf')] * num_docs
    for _ in range(num_hashes)
]

for h in range(num_hashes):

    a, b = hash_functions[h]

    # Calculate hash value for every row
    hash_values = []

    for x in range(num_rows):
        hash_value = (a * x + b) % num_rows
        hash_values.append(hash_value)

    # Find minimum hash value for each document
    for doc in range(num_docs):

        for row in range(num_rows):

            if matrix[row][doc] == 1:

                signature[h][doc] = min(
                    signature[h][doc],
                    hash_values[row]
                )


# --------------------------------
# DISPLAY RESULTS
# --------------------------------

print("Input Matrix:")
print("Shingle\tC1 C2 C3 C4")

for i, row in enumerate(matrix):
    print(f"{i}\t", row)


print("\nHash Functions:")

for i, (a, b) in enumerate(hash_functions):
    print(f"h{i + 1}(x) = ({a}x + {b}) % {num_rows}")


print("\nSignature Matrix:")

print("\tC1 C2 C3 C4")

for i in range(num_hashes):
    print(f"h{i + 1}\t", end="")

    for j in range(num_docs):
        print(signature[i][j], end=" ")

    print()


# --------------------------------
# Jaccard Similarity
# --------------------------------

def jaccard_similarity(doc1, doc2):

    intersection = 0
    union = 0

    for row in range(num_rows):

        if matrix[row][doc1] == 1 and matrix[row][doc2] == 1:
            intersection += 1

        if matrix[row][doc1] == 1 or matrix[row][doc2] == 1:
            union += 1

    return intersection / union


# --------------------------------
# Estimated Similarity using MinHash
# --------------------------------

def minhash_similarity(doc1, doc2):

    same = 0

    for h in range(num_hashes):

        if signature[h][doc1] == signature[h][doc2]:
            same += 1

    return same / num_hashes


print("\nDocument Similarities:")

for i in range(num_docs):
    for j in range(i + 1, num_docs):

        actual = jaccard_similarity(i, j)
        estimated = minhash_similarity(i, j)

        print(
            f"C{i + 1} vs C{j + 1}: "
            f"Jaccard = {actual:.2f}, "
            f"MinHash = {estimated:.2f}"
        )