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

def initialize_posting():
    obj = open("posting.pickle","wb")
    posting = defaultdict(defaultdict)
    pickle.dump(posting,obj)
    obj.close()

def make_postings(docID,token_count,key_posting):
    for token,count in token_count.items():
        key_posting[token][docID] =  count
    return key_posting

def pickle_postings(key_posting):
    obj = open("posting.pickle","wb")
    pickle.dump(key_posting,obj)
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
    print("Number of documents:",docID) 
    pickle_postings(key_posting)
    pickle_docid_urls(docid_url_dict)   
    print_report_info(key_posting)




















if __name__ == "__main__":
    read_files()
