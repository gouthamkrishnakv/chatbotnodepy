#! ./bin/python3
import nltk, json, sys, logging, datetime
logging.basicConfig(filename="logs/chatbotnode_" + datetime.date.today().isoformat() + ".log", level=logging.DEBUG)
logging.info('LOGGING STARTED')


# GET FILENAME
filename = 'file.json'
if(len(sys.argv) > 1):
    filename = sys.argv[1]
    logging.info('Filename found from app parameters')
# INPUT FILE

try:
    inpstr = open('question.qn').readline()
    logging.info('FILE FOUND, SUCCESSS')
except FileNotFoundError:
    logging.error('FILE NOT FOUND Error')
    inpstr = input().lower()
logging.info('string fetch successful, string is\'' + inpstr + '\'')
words = nltk.word_tokenize(inpstr)
logging.info('tokenized to an array of words')
stopwords = nltk.corpus.stopwords.words('english')
logging.info('Request stopwords')
# print(stopwords)
[word for word in words if word not in stopwords]
tagged = nltk.pos_tag(words)
# print(words)
# print(tagged)
try:
    obj = json.load(open(filename))
    logging.info('JSON Decode successful. Passing to value score')
except json.JSONDecodeError:
    logging.error('JSON  File' + filename + 'DECODE ERROR. Sanitize your JSON file.')
    exit(0)
ele_vals = [0]*len(obj)
# print(ele_vals)
isFound = False
logging.info('word score calculation in progress')
for tagwords in tagged:
    i=0
    for k,v in obj.items():
        if tagwords[0] in k:
            # print(tagwords[0] + " " + k)
            isFound = True
            if tagwords[1] == "NN" or tagwords[1] == "NNP":
                ele_vals[i]+=2
            else:
                ele_vals[i]+=1
        i+=1
# print(ele_vals)
logging.info('error value calculation finished. values are' + str(list(obj.items())))
maxv = ele_vals[0]
maxpos = 0
for i in range(len(ele_vals)):
    if(maxv < ele_vals[i]):
        maxpos = i
        maxv = ele_vals[i]
# print(maxpos)
logging.info('Maximum value calculated. The maximum value position is' + str(maxpos))
if isFound:
    # res = json.load(open('res.json','r'))
    # res.append(list(obj.items()))
    # print(type(list(obj.items())))
    json.dump(list(obj.items())[maxpos],open('res.json','w'))
    print(list(obj.items())[maxpos])
else:
    json.dump({'msg': 'Not Found'}, open('res.json','w'))
    logging.warning('Did not find the object. Need to work better on sanitation.')
