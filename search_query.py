import indexer
from functools import reduce
def get_query_user():
    user_query = input("Enter the query:")
    return user_query.lower()

def get_query_stems(user_query):    
    user_query_tokens = indexer.tokenize(user_query)
    query_stems = indexer.return_stems(user_query_tokens)
    return query_stems
    
def read_key_postings():
    obj = open("posting.pickle", "rb")
    key_postings = indexer.pickle.load(obj)
    obj.close()
    return key_postings

def get_docIDs_intersection(query_stems):
    stem_docIDs = []
    for stem in query_stems:
        stem_docIDs.append(key_postings[stem].keys())
    return list(reduce(lambda i, j: i & j, (set(x) for x in stem_docIDs))) 

def get_intersected_docIDs_freq_tuple_list(key_postings, query_stems, intersected_docIDs):
    common_docIDs_freq = []
    for stem in query_stems:
        for docID in intersected_docIDs:
            common_docIDs_freq.append((stem,docID,key_postings[stem][docID]))
    return sorted(common_docIDs_freq, key = lambda x: (x[0],-x[2],x[1]) )


        
#{token:{docIDs:frequency}}































if __name__ == "__main__":
    user_query = get_query_user()
    query_stems = get_query_stems(user_query)
    key_postings = read_key_postings()
    intersected_docIDs = get_docIDs_intersection(query_stems)
    docID_freq_list =  get_intersected_docIDs_freq_tuple_list(key_postings, 
            query_stems, intersected_docIDs)
    #print(docID_freq_list)
    print(sorted(key_postings['learn'].items(),key = lambda x: -x[1]))