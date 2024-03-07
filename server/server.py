from flask import Flask, jsonify, request, send_file, make_response
import controllers
from flask_cors import CORS
app = Flask(__name__)
CORS(app)



def buildResponse(data=None, code=200, msg="ok"):
    return jsonify({
        "data": data,
        "code": code,
        "msg": msg
    })


@app.route("/api/getLangCode")
def hello():
    return buildResponse({
        1: "Chinese",
        4: "English(US)",
        9: "Japanese",
        10: "Korean"
    })


@app.route("/api/keywordQuery", methods=['POST'])
def keywordQuery():
    langCode = request.json['langCode']
    keyword = request.json['keyword']

    return buildResponse(controllers.getTranslateObj(keyword, langCode))


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


# Run the server if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
