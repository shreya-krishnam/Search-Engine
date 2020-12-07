# Search-Engine

# indexer.py
Indexer loads all the JSON files in the target directories and extracts the data from each file. It only saves unique documents with the content tokenized. Each token is indexed with a docID that represents each unique document.

Indexer first generates 4 partial indexes that each of them contains a maximum of 15,000 documents. All 4 partial indexes are merged and pickle-dumped into one file and saved to the disk as "posting.pickle".

Indexer also generates a pickle file named "doc_id_urls.pickle" that contains a dictionary with all document IDs as keys and their matching URLs as values.

# search_query.py
search_query allows a user to input a query. It returns the top 5 URLs matching a query based on the TF-IDF scores of documents where the query appears once or more. If a query has multiple terms, search_query uses "AND" to get the intersections of documents that contain each term in the query.


