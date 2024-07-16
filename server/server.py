import os.path
import time

from flask import Flask, jsonify, request, send_file, make_response
import controllers
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
CORS(app)


def buildResponse(data=None, code=200, msg="ok"):
    return jsonify({
        "data": data,
        "code": code,
        "msg": msg
    })


@app.route("/api/getImportedTextLanguages")
def getImportedTextLanguages():
    return buildResponse(controllers.getImportedTextMapLangs())


@app.route("/api/getImportedVoiceLanguages")
def getImportedVoiceLanguages():
    return buildResponse(controllers.getLoadedVoicePacks())


@app.route("/api/keywordQuery", methods=['POST'])
def keywordQuery():
    langCode = request.json['langCode']
    keyword: str = request.json['keyword']

    if keyword.strip() == "":
        return buildResponse([])

    start = time.time()
    contents = controllers.getTranslateObj(keyword, langCode)
    end = time.time()

    return buildResponse({
        'contents': contents,
        'time': (end - start)*1000
    })


@app.route("/api/getVoiceOver", methods=['POST'])
def getVoiceOver():
    langCode = request.json['langCode']
    voicePath = request.json['voicePath']

    wemStream = controllers.getVoiceBinStream(voicePath, langCode)
    if wemStream is None:
        resp = make_response("Audio File Not Found")
        resp.headers['Access-Control-Expose-Headers'] = 'Error'
        resp.headers['Error'] = 'True'
        return resp

    return send_file(
        wemStream,
        download_name='voicePath',
        mimetype='image/png'
    )


@app.route("/api/getTalkFromHash", methods=['POST'])
def getTalkFromHash():
    langCode = request.json['langCode']
    textHash: int = request.json['textHash']

    start = time.time()
    contents = controllers.getTalkFromHash(textHash, langCode)
    end = time.time()

    return buildResponse({
        'contents': contents,
        'time': (end - start)*1000
    })


@app.route("/api/saveSettings", methods=['POST'])
def saveSettings():
    newConfig = request.json['config']
    if 'defaultSearchLanguage' in newConfig:
        controllers.setDefaultSearchLanguage(newConfig['defaultSearchLanguage'])

    if 'resultLanguages' in newConfig:
        controllers.setResultLanguages(newConfig['resultLanguages'])

    if 'sourceLanguage' in newConfig:
        controllers.setSourceLanguage(newConfig['sourceLanguage'])

    if 'isMale' in newConfig:
        controllers.setIsMale(newConfig['isMale'])

    controllers.saveConfig()

    return buildResponse(controllers.getConfig())


@app.route("/api/getSettings")
def getConfig():
    return buildResponse(controllers.getConfig())


staticDir = r"../webui/dist/"


@app.route('/')
def serveRoot():
    return send_from_directory(staticDir, 'index.html')


@app.route("/<path:path>")
def serveStatic(path):
    filePath = staticDir + path
    if os.path.exists(filePath):
        return send_from_directory(staticDir, path)
    else:
        return send_from_directory(staticDir, 'index.html')


# Run the server if this script is executed directly
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
