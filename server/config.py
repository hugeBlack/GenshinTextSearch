import json
import os.path

config = {
    "resultLanguages": [
        1, 4
    ],

    "defaultSearchLanguage": 4,
    "assetDir": "",
    "sourceLanguage": 1
}


def loadConfig():
    if not os.path.isfile("config.json"):
        return
    fp = open("config.json", encoding='utf-8')
    fileJson = json.load(fp)
    fp.close()

    if "assetDir" in fileJson:
        config["assetDir"] = fileJson['assetDir']

    if "resultLanguages" in fileJson and fileJson["resultLanguages"] is list[int]:
        config["resultLanguages"] = fileJson["resultLanguages"]

    if "defaultSearchLanguage" in fileJson and fileJson["defaultSearchLanguage"] is int:
        config["defaultSearchLanguage"] = fileJson["defaultSearchLanguage"]

    if "sourceLanguage" in fileJson and fileJson['sourceLanguage'] is int:
        config['sourceLanguage'] = fileJson['sourceLanguage']


def saveConfig():
    fp = open("config.json", encoding='utf-8', mode="w")
    json.dump(config, fp)
    fp.close()


def setDefaultSearchLanguage(newLanguage: int):
    config['defaultSearchLanguage'] = newLanguage


def setResultLanguages(newLanguages: list[int]):
    config["resultLanguages"] = newLanguages


def setSourceLanguage(newSourceLanguage: int):
    config['sourceLanguage'] = newSourceLanguage


def getDefaultSearchLanguage():
    return config['defaultSearchLanguage']


def getResultLanguages():
    return config["resultLanguages"]


def getSourceLanguage():
    return config['sourceLanguage']


def getAssetDir():
    return config['assetDir']


loadConfig()
