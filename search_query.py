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

def get_relevance_score(intersected_docIDs,key_postings,query_stems):
    relevance_score_dict = indexer.defaultdict(int)
    for docID in intersected_docIDs:
        score = 0
        for i in range(0,len(query_stems)):
            score += key_postings[query_stems[i]][docID]
        relevance_score_dict[docID] = score
    return sorted(relevance_score_dict.items(), key = lambda x:-x[1])

def get_docid_url():
    obj = open("doc_id_urls.pickle","rb+")
    docid_url_dict = indexer.pickle.load(obj)
    obj.close()
    return docid_url_dict 
    

def print_top_five_urls(sorted_relevance_score):
    if len(sorted_relevance_score)==0:
        print("No URL matches found")
    else:
        docid_url_dict =  get_docid_url()
        if 1<=len(sorted_relevance_score)<=4:
            print("Top",len(sorted_relevance_score),"URL matches found are:")
            for i in range(0,len(sorted_relevance_score)):
                print(docid_url_dict[sorted_relevance_score[i][0]])
        else:
            print("Top 5 URL matches found are:")
            for i in range(0,5):
                print(docid_url_dict[sorted_relevance_score[i][0]])


if __name__ == "__main__":
    user_query = get_query_user()
    query_stems = get_query_stems(user_query)
    key_postings = read_key_postings()
    intersected_docIDs = get_docIDs_intersection(query_stems)
    sorted_relevance_score = get_relevance_score(intersected_docIDs,key_postings,query_stems)
    print_top_five_urls(sorted_relevance_score)