import os
import json
import sys
from bs4 import BeautifulSoup as bs
import nltk
import re
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict 
import numpy as np

def get_important_words(soup):
    imp_words = soup.find_all(['title','h1','h2','h3'])
    imp_text = [tag.get_text() for tag in imp_words]
    final_imp_word_list = []
    if imp_text!=[]:
        for text in imp_text:
            if text!='':
                final_imp_word_list.extend([w for w in tokenize(text) if w not in stopwords.words('english')])
    return return_stems(list(set(final_imp_word_list)))

def get_content_string(rawcontent):
    soup = bs(rawcontent, 'html.parser')
    imp_words = get_important_words(soup)
    text = soup.get_text()
    return imp_words,text


def tokenize(content_string):
    s = re.compile("[a-z0-9]+")
    return re.findall(s,content_string.lower())

def return_stems(tokens):
    porter = PorterStemmer()
    for i in range(0,len(tokens)):
        tokens[i] = porter.stem(tokens[i])
    return tokens

def get_token_occurances(stems):
    numWords = dict()
    for word in stems:
        if word in numWords:
            numWords[word] += 1
        else:
            numWords[word] = 1
    return numWords

def make_postings(docID,token_count,key_posting,imp_words):
    for token,count in token_count.items():
        if token in imp_words:
            key_posting[token][docID] =  (count,'y')
        else:
            key_posting[token][docID] =  (count,'n')
    return key_posting

def pickle_final_postings(key_posting):
    obj = open("final_posting.pickle","wb")
    pickle.dump(key_posting,obj)
    obj.close()

def sortandwritetodisk(key_posting,partialindexnumber):
    file_to_open =  "partial"+str(partialindexnumber)+".pickle"
    obj = open(file_to_open,"wb")
    sorted_posting = sorted(key_posting.items(), key = lambda kv: (kv[0],kv[1]))
    sorted_key_posting = defaultdict(defaultdict)
    for k,v in sorted_posting:
        sorted_key_posting[k] = v
    pickle.dump(sorted_key_posting,obj)
    obj.close()


def print_report_info(key_posting):
    print("\nNumber of unique words: ",len(key_posting))

def make_dict_urls(docid_url_dict,docID,url):
    docid_url_dict[docID] = url
    return docid_url_dict

def pickle_docid_urls(docid_url_dict):
    obj = open("doc_id_urls.pickle","wb")
    pickle.dump(docid_url_dict,obj)
    obj.close()

def make_alphabet_number_initial_postings():
    alphabet_list = alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
    for c in alphabet_list:
        file_obj = open("partials/"+c+".pickle","wb")
        pickle.dump(defaultdict(defaultdict),file_obj)
        file_obj.close()
    num_obj = open("partials/numbers.pickle","wb")
    pickle.dump(defaultdict(defaultdict),num_obj)
    num_obj.close()

def merge_and_write_alphabet_number_postings(partial_posting):
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
    alphabet_num_postings = dict()
    for c in alphabet_list: #opening all files
        file_obj = open("partials/"+c+".pickle","rb")
        alphabet_num_postings[c] = pickle.load(file_obj)
        file_obj.close()
    num_obj = open("partials/numbers.pickle","rb")
    alphabet_num_postings['num'] = pickle.load(num_obj)
    num_obj.close()
    for k,v in partial_posting.items(): #merging and sorting
        if k[0] in alphabet_list:
            if k not in alphabet_num_postings[k[0]]:
                alphabet_num_postings[k[0]][k] = v
            else:
                temp_dict = {**alphabet_num_postings[k[0]][k],**partial_posting[k]}
                value = defaultdict(defaultdict,temp_dict)
                alphabet_num_postings[k[0]][k] = value
        else:
            if k not in alphabet_num_postings['num']:
                alphabet_num_postings['num'][k] = v
            else:
                temp_dict = {**alphabet_num_postings['num'][k],**partial_posting[k]}
                value = defaultdict(defaultdict,temp_dict)
                alphabet_num_postings['num'][k] = value
    
    #sorting             
    for c,v in alphabet_num_postings.items():
        sorted_posting = sorted(v.items(), key = lambda kv: (kv[0],kv[1]))
        sorted_final_posting = defaultdict(defaultdict)
        for k,v in sorted_posting:
            sorted_final_posting[k] = v
        alphabet_num_postings[c] =  sorted_final_posting
    sorted_posting = sorted(alphabet_num_postings['num'].items(), key = lambda kv: (kv[0],kv[1]))
    sorted_final_posting = defaultdict(defaultdict)
    for k,v in sorted_posting:
        sorted_final_posting[k] = v
    alphabet_num_postings['num'] =  sorted_final_posting
    #Writing to disk
    for c in alphabet_list:
        file_obj = open("partials/"+c+".pickle","wb")
        alphabet_num_postings[c] = pickle.dump(alphabet_num_postings[c],file_obj)
        file_obj.close()
    num_obj = open("partials/numbers.pickle","wb")
    pickle.dump(alphabet_num_postings['num'],num_obj)
    num_obj.close()
def create_alphabetical_order_posting(partial_obj,partial_number):
    partial_posting = pickle.load(partial_obj)
    if partial_number == 1:
        make_alphabet_number_initial_postings()
    merge_and_write_alphabet_number_postings(partial_posting) 

def calculate_tfidf(tf,N,df):
    if tf==0 or df==0:return 0
    return (1+np.log10(tf))*(np.log10(N/df))

def write_tfidf(N):
    alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
    alphabet_num_postings = dict()
    for c in alphabet_list: #opening all files
        file_obj = open("partials/"+c+".pickle","rb")
        alphabet_num_postings[c] = pickle.load(file_obj)
        file_obj.close()
    num_obj = open("partials/numbers.pickle","rb")
    alphabet_num_postings['num'] = pickle.load(num_obj)
    num_obj.close()
    for c,v in alphabet_num_postings.items():
        for term,posting in v.items():
            for docID,tf_tuple in posting.items():
                tfidf_score = calculate_tfidf(tf_tuple[0],N,len(posting))
                if tf_tuple[1] == 'y':
                    tfidf_score += 0.25 * tfidf_score 
                alphabet_num_postings[c][term][docID] = tfidf_score
            sorted_tfidf = {docID: tfidf for docID,tfidf in sorted(alphabet_num_postings[c][term].items(),key = lambda kv:(-kv[1],kv[0]))}
            sorted_tfidf = defaultdict(float, sorted_tfidf)
            alphabet_num_postings[c][term] = sorted_tfidf
    #write
    for c in alphabet_list:
        file_obj = open("partials_tfidf/"+c+".pickle","wb")
        alphabet_num_postings[c] = pickle.dump(alphabet_num_postings[c],file_obj)
        file_obj.close()
    num_obj = open("partials_tfidf/numbers.pickle","wb")
    pickle.dump(alphabet_num_postings['num'],num_obj)
    num_obj.close()

def read_files():
    directory = "C:\\Users\\Shreya\\Documents\\CLASS NOTES\\CS 121\\Assignment3\\developer\\developer\\DEV"
    list_of_all_urls =  []
    sub_directories = os.listdir(directory)
    key_posting = defaultdict(defaultdict)
    docid_url_dict =  defaultdict(str)
    docID = 0
    for sub_directory in sub_directories:
        subdirectory_path = os.path.join(directory,sub_directory)
        for file_path in os.listdir(subdirectory_path):
            file_path = os.path.join(subdirectory_path,file_path)
            file_object = open(file_path,"r")
            json_data = json.load(file_object)
            if json_data["url"] not in list_of_all_urls:
                docID+=1
                print(docID)
                imp_words,content_string = get_content_string(json_data["content"])
                tokens = tokenize(content_string)
                stems = return_stems(tokens)
                token_count = get_token_occurances(stems)
                key_posting = make_postings(docID,token_count,key_posting,imp_words)
                list_of_all_urls.append(json_data["url"])
                docid_url_dict = make_dict_urls(docid_url_dict,docID,json_data["url"])
                file_object.close()
                if docID % 15000 == 0:
                    sortandwritetodisk(key_posting,docID//15000)
                    key_posting.clear()
    N = 55393
    sortandwritetodisk(key_posting,(docID//15000)+1)
    partial1_obj = open("partial1.pickle","rb")
    partial2_obj = open("partial2.pickle","rb")
    partial3_obj =  open("partial3.pickle","rb")
    partial4_obj = open("partial4.pickle","rb")

    create_alphabetical_order_posting(partial1_obj,1)
    create_alphabetical_order_posting(partial2_obj,2)
    create_alphabetical_order_posting(partial3_obj,3)
    create_alphabetical_order_posting(partial4_obj,4)

    partial1_obj.close()
    partial2_obj.close()
    partial3_obj.close()
    partial4_obj.close()

    write_tfidf(N)

if __name__ == "__main__":
    read_files()
