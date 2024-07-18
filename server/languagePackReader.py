import os

from AudioReader.FilePackager import Package, fnv_hash_64
import config

GENSHIN_PATH = config.getAssetDir()

langCodes = {
    1: "Chinese",
    4: "English(US)",
    9: "Japanese",
    10: "Korean"
}

langPackages: 'dict[int, Package]' = {}


def loadLangPackages():
    paths = [
        os.path.join(GENSHIN_PATH, "Persistent", "AudioAssets"),
        os.path.join(GENSHIN_PATH, "StreamingAssets", "AudioAssets")
    ]

    langToCode = {
        "Chinese": 1,
        "English(US)": 4,
        "Japanese": 9,
        "Korean": 10
    }
    for pathDir in paths:
        if not os.path.exists(pathDir):
            continue

        for langName, code in langToCode.items():
            if code in langPackages:
                continue
            langPackPath = os.path.join(pathDir, langName)
            if not os.path.exists(langPackPath):
                continue
            files = os.listdir(langPackPath)
            if len(files) < 10:
                continue

            voicePack = Package()
            for fileName in files:
                fobj = open(os.path.join(langPackPath, fileName), "rb")
                voicePack.addfile(fobj)
            langPackages[code] = voicePack

            print("loaded voice pack: " + langName)


def getAudioBin(path: str, langCode: int):
    if langCode not in langCodes:
        raise "No voice-over for this language!"
    langStr = langCodes[langCode]
    hashVal = fnv_hash_64((langStr + "\\" + path).lower())
    # TODO 多语言支持，要检测是否安装了这个语言
    try:
        voicePack = langPackages[langCode]

        wemFiles = voicePack.get_file_data_by_hash(hashVal, langid=0, mode=2)
        wenBin, pckPath = wemFiles[0]
        return wenBin
    except FileNotFoundError | KeyError:
        return None  # 文件被米删了


def checkAudioBin(path: str, langCode: int):
    if langCode not in langPackages:
        raise "No voice-over for this language!"
    langStr = langCodes[langCode]
    hashVal = fnv_hash_64((langStr + "\\" + path).lower())
    voicePack = langPackages[langCode]

    return voicePack.check_file_by_hash(hashVal, langid=0, mode=2)


loadLangPackages()
