"""
    DSA Integration: Linear Search vs Dictionary Lookup
    
    Comparing two approaches to finding a transaction by ID:
    1. Linear Search - scan through the list one by one
    2. Dictionary Lookup - use a dictionary with id as key for instant access
"""

import time
import json


# Load the transactions from the json file we generated
with open('data/processed/transactions.json', 'r') as f:
    transactions_list = json.load(f)

print(f"Total transactions loaded: {len(transactions_list)}")



# METHOD 1: LINEAR SEARCH

def linear_search(transactions, target_id):
    """scans through the list of transactions one by one until it finds the target id"""
    for transaction in transactions:
        if transaction["transaction_id"] == target_id:
            return transaction
    return None


# METHOD 2: DICTIONARY LOOKUP


transactions_dict = {}
for transaction in transactions_list:
    transactions_dict[transaction["transaction_id"]] = transaction


def dictionary_lookup(transactions_dict, target_id):
    """looks up a transaction directly by its key in the dictionary"""
    return transactions_dict.get(target_id, None)


# PERFORMANCE COMPARISON

# generate 20 target IDs to search for
# mix of early, middle, late, and non-existent IDs
target_ids = [1, 5, 10, 25, 50, 100, 200, 300, 400, 500,
              600, 800, 1000, 1200, 1400, 1500, 1600, 1650, 1661, 9999]

print(f"\nSearching for {len(target_ids)} transaction IDs...\n")
print(f"{'ID':<8}{'Linear Search':<25}{'Dictionary Lookup':<25}{'Speed Difference'}")
print("=" * 80)

total_linear_time = 0
total_dict_time = 0

for target_id in target_ids:

    # measure linear search: run it 10000 times to get a measurable duration
    start = time.perf_counter()
    for _ in range(10000):
        linear_result = linear_search(transactions_list, target_id)
    linear_time = time.perf_counter() - start

    # measure dictionary lookup: run it 10000 times to get a measurable duration
    start = time.perf_counter()
    for _ in range(10000):
        dict_result = dictionary_lookup(transactions_dict, target_id)
    dict_time = time.perf_counter() - start

    total_linear_time += linear_time
    total_dict_time += dict_time

    # calculate how many times faster dictionary lookup is
    if dict_time > 0:
        speedup = linear_time / dict_time
    else:
        speedup = float('inf')

    # check if the transaction was found
    found = "Found" if linear_result is not None else "Not Found"

    print(f"{target_id:<8}{linear_time:.6f}s ({found}){'':<6}{dict_time:.6f}s{'':<13}{speedup:.1f}x faster")


print("=" * 80)
print(f"\n{'Total Linear Search Time:':<30}{total_linear_time:.6f}s")
print(f"{'Total Dictionary Lookup Time:':<30}{total_dict_time:.6f}s")
print(f"{'Overall Speedup:':<30}{total_linear_time / total_dict_time:.1f}x faster")


# DISPLAY SAMPLE RESULTS

print("\n\n========================================")
print("Sample Search Results")
print("========================================")

sample_ids = [1, 500, 1661, 9999]

for target_id in sample_ids:
    result = dictionary_lookup(transactions_dict, target_id)
    if result:
        print(f"\nTransaction ID {target_id}:")
        print(f"  Category: {result['category']}")
        print(f"  Amount:   {result['amount']} RWF")
        print(f"  Date:     {result['transaction_date']}")
        print(f"  Status:   {result['status']}")
        print(f"  Sender:   {result['sender']}")
        print(f"  Receiver: {result['receiver']}")
    else:
        print(f"\nTransaction ID {target_id}: Not Found")


# REFLECTION

"""
Linear Search has a time complexity of O(n). It starts at the beginning 
of the list and checks each transaction one by one until it finds the 
target. In the worst case, if the target is at the end or doesn't exist, 
it checks every single transaction. With 1,661 transactions, searching 
for ID 1661 means checking all 1,661 items.

Dictionary Lookup has a time complexity of O(1) on average. Python 
dictionaries are implemented as hash tables. When you look up a key, 
Python runs it through a hash function that calculates the exact memory 
location where the value is stored. It jumps directly to that location 
instead of scanning through everything. Whether you have 100 or 1 million 
transactions, the lookup time stays essentially the same.

The tradeoff is that the dictionary requires extra memory to store the 
hash table structure and it takes O(n) time upfront to build the 
dictionary from the list. But once built, every subsequent lookup is O(1).

Another data structure that could improve search efficiency is a Binary 
Search Tree (BST) or a balanced variant like a Red-Black Tree. If the 
transactions were stored in a BST sorted by transaction_id, each search 
would take O(log n) time, which for 1,661 records means checking at most 
about 11 items instead of all 1,661. This sits between linear search 
O(n) and dictionary lookup O(1), but unlike a dictionary, a BST also 
maintains sorted order, which is useful for range queries like finding 
all transactions between ID 500 and ID 800.
"""