import simNameService
import word2vec
import json
from flask import Flask,request
from flask import jsonify
app = Flask(__name__)

@app.route('/getSimInstitutionByName')
def getSimInstitutionByName():
    name = request.args.get('name')
    nameList = simNameService.getSimNameByCity(simNameService.getLocationByName(name))
    return jsonify(nameList)
    # responseStr = ""
    # for name in nameList:
    #     responseStr = responseStr + name + '</br>'
    # return responseStr

@app.route('/getWordRepresentation')
def getWordRepresentation():
    algorithm = request.args.get('algorithm')
    word = request.args.get('word')
    if algorithm == 'word2vec':
        vec = word2vec.getWordVecFromModel(word)
        vecStr = json.dumps(vec,ensure_ascii=False)
        response = vecStr
    elif algorithm == 'tfidf':
        response = 'tfidf'
    elif algorithm == 'lda':
        response = 'lda'
    return response

if __name__ == '__main__':
    app.run()