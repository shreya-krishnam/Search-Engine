import indexer
from functools import reduce


def get_query_user():
    user_query = input("Enter the query:")
    return user_query.lower()

def get_query_stems(user_query):    
    user_query_tokens = indexer.tokenize(user_query)
    query_stems = indexer.return_stems(user_query_tokens)
    return query_stems
    
def return_key_postings():
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
    alphabet_num_postings = dict()
    for c in alphabet_list: #opening all files
        file_obj = open("partials_tfidf/"+c+".pickle","rb")
        alphabet_num_postings[c] = indexer.pickle.load(file_obj)
        file_obj.close()
    num_obj = open("partials_tfidf/numbers.pickle","rb")
    alphabet_num_postings['num'] = indexer.pickle.load(num_obj)
    num_obj.close()
    return alphabet_num_postings

def get_docIDs_intersection(query_stems,alphabet_num_key_postings):
    stem_docIDs = []
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
    for stem in query_stems:
        if stem[0] in alphabet_list: #checks if it's an alphabet
            s = alphabet_num_key_postings[stem[0]][stem].keys()
        else:
            s = alphabet_num_key_postings['num'][stem].keys()
        stem_docIDs.append(s)
    return list(reduce(lambda i, j: i & j, (set(x) for x in stem_docIDs))) 

def calculate_raw_cosine_score(alphabet_num_key_postings, stem,tf_query,docID):
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    tf_query_stem = tf_query[stem]
    N = 55393
    if stem[0] in alphabet_list: 
        df = len(alphabet_num_key_postings[stem[0]][stem])
        tfidf_doc = alpha_num_key_postings[stem[0]][stem][docID]
    else: 
        df = len(alphabet_num_key_postings['num'][stem])
        tfidf_doc = alpha_num_key_postings['num'][stem][docID]
    tfidf_query_stem = indexer.calculate_tfidf(tf_query_stem,N,df)
    return (tfidf_query_stem *  tfidf_doc, tfidf_query_stem , tfidf_doc)
    





def get_similarity_score(intersected_docIDs,alphabet_num_key_postings,query_stems):
    tf_query = indexer.get_token_occurances(query_stems)
    cosine_scores = indexer.defaultdict(float) #{docID: cosine_score}
    for docID in intersected_docIDs:
        tfidf_raw_scores = []
        tfidf_query_stems = []
        tfidf_docs = []
        for stem in query_stems:
            tfidf_raw_score,tfidf_query_stem,tfidf_doc = calculate_raw_cosine_score(alphabet_num_key_postings,stem,tf_query,docID)
            tfidf_raw_scores.append(tfidf_raw_score)
            tfidf_query_stems.append(tfidf_query_stem**2)
            tfidf_docs.append(tfidf_doc**2)
        normalized_tfidf_score = sum( tfidf_raw_scores)
        normalized_query_score = indexer.np.sqrt(sum(tfidf_query_stems))
        normalized_doc_score = indexer.np.sqrt(sum(tfidf_docs))
        cos_score = normalized_tfidf_score / ( normalized_query_score * normalized_doc_score )
        cosine_scores[docID] =  cos_score


    return sorted(cosine_scores.items(),key = lambda kv:-kv[1])


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
    alpha_num_key_postings = return_key_postings()
    user_query = get_query_user()
    query_stems = get_query_stems(user_query)
    intersected_docIDs = get_docIDs_intersection(query_stems,alpha_num_key_postings)
    sorted_scores = get_similarity_score(intersected_docIDs,alpha_num_key_postings,query_stems)
    print_top_five_urls(sorted_scores)