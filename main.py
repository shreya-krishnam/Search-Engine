import os
import json
from bs4 import BeautifulSoup as bs
import nltk,re
from nltk.stem import PorterStemmer
from sklearn.

def get_content_string(rawcontent):
    soup = bs(rawcontent, 'html.parser')
    text = soup.find_all(text=True)
    content = ''
    blacklist = [
        '[document]',
        'noscript',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        '!–',
        'marquee',
        'img',
        'source',
    ]
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

def get_tfidf_score(tokens):




def read_files():
    directory = "C:\\Users\\Shreya\\Documents\\CLASS NOTES\\CS 121\\Assignment3\\developer\\developer\\DEV"
    sub_directories = os.listdir(directory)
    count = 0
    for sub_directory in sub_directories:
        subdirectory_path = os.path.join(directory,sub_directory)
        for file_path in os.listdir(subdirectory_path):
            file_path = os.path.join(subdirectory_path,file_path)
            file_object = open(file_path,"r")
            json_data = json.load(file_object)
            content_string = get_content_string(json_data["content"])
            print(tokenize(content_string))
            count+=1
            if count>=1:
                break
            file_object.close()












if __name__ == "__main__":
    read_files()
