# Search-Engine

Description of .py files we used
# indexer.py
This is our index creation file.
Indexer loads all the JSON files in the target directories and extracts the data from each file. It only saves unique documents with the content tokenized. Each token is indexed with a docID that represents each unique document.

Indexer first generates 4 partial indexes. All 4 partial indexes are merged and pickle-dumped into alphabetically ordered pickle files like partials/a...z and partials/num according to the starting letter of the alphabet or if it's a number. It also stores the precomputed tfidf files in pickle files under the directory partials_tfidf/a .... partials_tfidf/z and partials/num according to the starting letter of the alphabet or if it's a number.

Indexer also generates a pickle file named "doc_id_urls.pickle" that contains a dictionary with all document IDs as keys and their matching URLs as values.

It checks for duplicates and near duplicates as well.

# search_query.py
This our search component file.
Search_query.py allows a user to input a query. It returns the top 5 URLs matching a query based on the TF-IDF scores of documents where the query appears once or more. It implements a boolean AND search but with a ranked retrieval. It uses an aggregate tfidf score to compute the relevance of the best matching documents. It's optimized to maximize the speed + performance using the concept of contendenders and champion lists during post processing.

How to use our system
--------------------------------------

----------
Steps
----------

1) Download the zip file in the submission(unzip) which already has all the pre - computed indexes and run the indexer.py file and give the input directory as your ROOT folder of your dev files.
Eg input in my case: C:\\Users\\Shreya\\Documents\\CLASS NOTES\\CS 121\\Assignment3\\developer
2) Then to run the search component run search_query.py file

(OR)
1) Download the just the indexer.py files and search_query.py files
2) Then add 2 folders called partials and partials_tfidf (please follow the exact names).
3) Run indexer.py to create the indexes.
4) Run search_query.py to run the search component




