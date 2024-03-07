import os

import databaseHelper
import languagePackReader
from AudioReader.FilePackager import Package, fnv_hash_64


def audioExtractText():
    AUDIO_PATH = r'E:\gs\Genshin Impact Game\YuanShen_Data\StreamingAssets\AudioAssets\Japanese'

    jpPack = Package()
    files = os.listdir(AUDIO_PATH)

    for fileName in files:
        fobj = open(AUDIO_PATH + "\\" + fileName, "rb")
        jpPack.addfile(fobj)

    hashVal = fnv_hash_64("JAPANESE\\VO_LQ\\VO_yaeMiko\\vo_SGLQ103_5_yaeMiko_24.wem".lower())

    wemFiles = jpPack.get_file_data_by_hash(hashVal, langid=0, mode=2)

    wenBin, pckPath = wemFiles[0]

    with open("{}.wem".format(hashVal), "wb") as f:
        f.write(wenBin)

    print(pckPath)


def searchTest():
    keyword = "jumble"
    contents = databaseHelper.selectTextMapFromKeyword(keyword, 4)
    hashVal, content = contents[0]
    print(hashVal, content)
    texts = databaseHelper.selectTextMapFromTextHash(hashVal)
    print(texts)
    for content in contents:
        print(content[1])
        voicePath: str = databaseHelper.selectVoicePathFromTextHashInDialogue(content[0])
        if voicePath is not None:
            audioBin = languagePackReader.getAudioBin(voicePath, 9)
            print(voicePath)
            if audioBin is not None:
                with open("Z:\\" + voicePath.replace("\\", "_"), 'wb') as f:
                    f.write(audioBin)
                pass
            else:
                print("Audio file deleted!")
