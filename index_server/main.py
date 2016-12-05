from flask import *
import config
import requests
import json
import re
import operator
from operator import itemgetter

    
main = Blueprint('main', __name__, template_folder='templates')

file_pagerank = "pagerank.out"
file_tfidf = "outfile.txt"
file_stopwords = "stopwords.txt"
prDict={}
with open(file_pagerank,'r') as f_pr:
    for line in f_pr:
        line = line.strip("\t\n")
        docid = line.split(",",1)[0]
        pagerank = line.split(",",1)[1]
        prDict[docid] = pagerank
f_pr.close()
    
stopwords = []
with open(file_stopwords,'r') as f_st:
    for line in f_st:
        line = line.strip("\t\n")
        stopwords.append(line)
f_st.close()
    
tfDict = {}
with open(file_tfidf,'r') as f_tf:
    for line in f_tf:
        dic_value = []
        term = line.split(" ",1)[0]
        rem = line.split(" ",1)[1]
        idf = rem.split(" ",1)[0]
        idf = float(idf)
        rem = rem.split(" ",1)[1]
        total = rem.split(" ",1)[0]
        total = int(total)
        rem = rem.split(" ",1)[1]
        d = []
        word = ""
        dic = {}
        rem = rem.strip("\t\n")
        for ch in rem:
            if ch != " ":
                word += ch
            else:
                d.append(word)
                word = ""
                if len(d) == 3:
                    key = d[0]
                    value = [d[1],d[2]]
                    dic[key] = value
                    d = []
        dic_value = [idf,total,dic]
        tfDict[term] = dic_value
f_tf.close()
   
@main.route('/', methods = ['GET'])
def index_server():
    qu = request.args.get('q')
    weight = request.args.get('w')
    qu = str(qu)
    qu = qu.lower()
    qu = re.sub(r'[^a-zA-Z0-9]+', '', qu)
    word = ""
    query = []
    for ch in qu:
        if ch != " ":
            word += ch
        else:
            query.append(word)
            word = ""
    query.append(word)
    que = []
    for q in query:
        if not q in stopwords:
            que.append(q)
    query = que
    weight = str(weight)
    weight = float(weight)
    count={}
    existdocs=[]
    word={}
    result={}
    querys={}
    fa=0
    score={}
    cosine=0
    resultdeno={}
    querydeno=0
    tmp=""
    
    for word in query:
        if word in querys:
            querys[word] += 1
        else:
            querys[word] = 1
            
    for query in querys:
        for key in tfDict:
            if key == query:
                for item in tfDict[query][2]:
                    if item in count:
                        count[item] += 1
                    else:
                        count[item] = 1
                        
    for key in count:
        if count[key] == len(querys):
            existdocs.append(key)

    for key in querys:
        for doc in existdocs:
            for item in tfDict[key][2]:
                if doc == item:
                    if doc in result:
                        result[doc][0][key] = float(tfDict[key][2][doc][0])*tfDict[key][0]/(float(tfDict[key][2][doc][1])**0.5)
                    else:
                        result[doc] = [{key:float(tfDict[key][2][doc][0])*tfDict[key][0]/(float(tfDict[key][2][doc][1])**0.5)}]

    for key in querys:
        if not key in tfDict:
            a = []
            rDict = {"hits": a}
            return jsonify(rDict)
        tfidf = querys[key]*tfDict[key][0]
        tmp = querys[key]
        querys[key] = [tmp,tfidf]
        fa += tfidf*tfidf

    for key in querys:
        querys[key][1] = querys[key][1]/(fa**0.5)

    for key in result:
        for item in result[key][0]:
            if key in resultdeno:
                resultdeno[key] += result[key][0][item]*result[key][0][item]
            else:
                resultdeno[key] = result[key][0][item]*result[key][0][item]
        resultdeno[key] = resultdeno[key]**0.5

    for key in querys:
        querydeno += querys[key][1]*querys[key][1]
    querydeno = querydeno**0.5

    for key in result:
        for query in querys:
            cosine += querys[query][1]*result[key][0][query]
        cosine = cosine/(resultdeno[key]*querydeno)
        score[key] = cosine
        cosine = 0
    for key in score:
        if not key in prDict:
            prDict[key] = 0
        score[key] = (1-weight)*float(score[key])+weight*float(prDict[key])
              
    jDict = {}
    value = []
    for key in score:
        tmp = {}
        docid = key
        docid = int(docid)
        sc = score[key]
        tmp = {"docid" : docid, "score" : sc}
        value.append(tmp)
    newValue = sorted(value, key=itemgetter('score','docid'), reverse=True)
    jDict = {"hits" : newValue}
    return jsonify(jDict)
