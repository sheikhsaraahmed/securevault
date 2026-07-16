def generate_fuzzy_set(bank, edit_distance=1):
    fuzzy_set = set()
    fuzzy_set.add(bank)
    
    for i in range(len(bank)):
          variant = bank[:i]+'*'+bank[i+1:]
          fuzzy_set.add(variant)
    
    for i in range(len(bank)+1):
          variant = bank [:i]+'*'+bank[i:]
          fuzzy_set.add(variant)
    
    return fuzzy_set
    
import hmac
import hashlib
def get_trapdoor(bank, secret_key):
    key_bytes = secret_key.encode()            #this will convert key string into bytes
    word_bytes = bank.encode()                 #this will convert word string into bytes
    
    h = hmac.new(key_bytes, word_bytes, hashlib.sha256) #this do the HMAC
    return h.hexdigest()                        # convert result to a readable hex string
    
print(get_trapdoor("bank", "my_secret_key"))

def hash_fuzzy_set(fuzzy_set, secret_key):
    trapdoor_set = set()
    for bank in fuzzy_set:
        trapdoor = get_trapdoor(bank, secret_key)
        trapdoor_set.add(trapdoor)
    return trapdoor_set
    
fuzzy = generate_fuzzy_set("bank")
trapdoors = hash_fuzzy_set(fuzzy, "my_secret_key")
print(trapdoors)
print(len(trapdoors))

def add_to_index(index, file_id, tag, secret_key):
    fuzzy_set = generate_fuzzy_set(tag)
    trapdoors = hash_fuzzy_set(fuzzy_set, secret_key)
    
    for trapdoor in trapdoors:
        if trapdoor not in index:
            index[trapdoor] = []         
        index[trapdoor].append(file_id) 
        
index = {}
add_to_index(index, "file_001", "bank", "my_secret_key")
add_to_index(index, "file_002", "documents", "my_secret_key")
print(len(index))

def search_index(index, query, secret_key):
    fuzzy_set = generate_fuzzy_set(query)
    trapdoors = hash_fuzzy_set(fuzzy_set, secret_key)
    
    results = set()
    for trapdoor in trapdoors:
        if trapdoor in index:
            for file_id in index[trapdoor]:
                results.add(file_id)        
    
    return results
    
index = {}
add_to_index(index, "file_001", "bank", "my_secret_key")
add_to_index(index, "file_002", "documents", "my_secret_key")

# exact match test
print(search_index(index, "bank", "my_secret_key"))

# typo test — one letter off
print(search_index(index, "bnk", "my_secret_key"))