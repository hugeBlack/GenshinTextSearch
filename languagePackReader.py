import os

from AudioReader.FilePackager import Package, fnv_hash_64

# AUDIO_PATH = r'E:\gs\Genshin Impact Game\YuanShen_Data\StreamingAssets\AudioAssets\Japanese'
AUDIO_PATH = r'E:\gs\Genshin Impact Game\YuanShen_Data\Persistent\AudioAssets\English(US)'

jpPack = Package()
files = os.listdir(AUDIO_PATH)

for fileName in files:
    fobj = open(AUDIO_PATH + "\\" + fileName, "rb")
    jpPack.addfile(fobj)

langCodes = {
    1: "Chinese",
    4: "English(US)",
    9: "Japanese",
    10: "Korean"
}


def getAudioBin(path: str, langCode: int):
    if langCode not in langCodes:
        raise "No voice-over for this language!"
    langStr = langCodes[langCode]
    hashVal = fnv_hash_64((langStr + "\\" + path).lower())
    # TODO 多语言支持，要检测是否安装了这个语言
    try:
        wemFiles = jpPack.get_file_data_by_hash(hashVal, langid=0, mode=2)
        wenBin, pckPath = wemFiles[0]
        return wenBin
    except FileNotFoundError:
        return None  # 文件被米删了
