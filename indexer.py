import os
import json
import sys
from bs4 import BeautifulSoup as bs
import nltk
import re
import pickle
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict 

def get_content_string(rawcontent):
    soup = bs(rawcontent, 'html.parser')
    text = soup.find_all(text=True)
    content = ''
    blacklist = ['style', 'script', 'head',  'meta', '[document]']
    for t in text:
        if t.parent.name not in blacklist:
            content += '{} '.format(t)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', content)

def tokenize(content_string):
    s = re.compile("[a-z0-9']+")
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

def make_postings(docID,token_count,key_posting):
    for token,count in token_count.items():
        key_posting[token][docID] =  count
    return key_posting

def pickle_final_postings(key_posting):
    obj = open("final_posting.pickle","wb")
    pickle.dump(key_posting,obj)
    obj.close()

def sortandwritetodisk(key_posting,partialindexnumber):
    print(partialindexnumber)
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

def mergepartials(file_obj1,file_obj2):
    posting1 = pickle.load(file_obj1)
    posting2 = pickle.load(file_obj2)
    merged = defaultdict(defaultdict)
    for k,v in posting1.items():
        if k not in posting2:
            merged[k] =  v
        else:
            temp_dict = {**v,**posting2[k]}
            value = defaultdict(defaultdict,temp_dict)
            merged[k] = value
    for k,v in posting2.items():
        if k not in posting1:
            merged[k] = v
    return merged

def mergeandsort(merged1,merged2):
    merged = defaultdict(defaultdict)
    for k,v in merged1.items():
        if k not in merged2:
            merged[k] =  v
        else:
            temp_dict = {**v,**merged2[k]}
            value = defaultdict(defaultdict,temp_dict)
            merged[k] = value
    for k,v in merged2.items():
        if k not in merged1:
            merged[k] = v
    sorted_posting = sorted(merged.items(), key = lambda kv: (kv[0],kv[1]))
    sorted_final_posting = defaultdict(defaultdict)
    for k,v in sorted_posting:
        sorted_final_posting[k] = v
    return sorted_final_posting
    
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
                content_string = get_content_string(json_data["content"])
                tokens = tokenize(content_string)
                stems = return_stems(tokens)
                token_count = get_token_occurances(stems)
                key_posting = make_postings(docID,token_count,key_posting)
                list_of_all_urls.append(json_data["url"])
                docid_url_dict = make_dict_urls(docid_url_dict,docID,json_data["url"])
                file_object.close()
                if docID % 15000 == 0:
                    print(docID)
                    sortandwritetodisk(key_posting,docID//15000)
                    key_posting.clear()
    sortandwritetodisk(key_posting,(docID//15000)+1)
    partial1_obj = open("partial1.pickle","rb")
    partial2_obj = open("partial2.pickle","rb")
    partial3_obj =  open("partial3.pickle","rb")
    partial4_obj = open("partial4.pickle","rb")

    merged1 = mergepartials(partial1_obj,partial2_obj)
    merged2 = mergepartials(partial3_obj,partial4_obj)

    partial1_obj.close()
    partial2_obj.close()
    partial3_obj.close()
    partial4_obj.close()

    final_posting = mergeandsort(merged1,merged2)
    pickle_final_postings(final_posting)
    print(len(final_posting))





















if __name__ == "__main__":
    read_files()
