import databaseHelper
import languagePackReader


# class TranslateText:
#     def __init__(self, textHash):
#         self.textHash = textHash
#
#
# class GenshinText:
#     def __init__(self, text):

def selectVoicePathFromTextHash(textHash: int):
    voicePath: str = databaseHelper.selectVoicePathFromTextHashInDialogue(textHash)
    if voicePath is not None:
        return voicePath

    voicePath = databaseHelper.selectVoicePathFromTextHashInFetter(textHash)
    if voicePath is not None:
        return voicePath


if __name__ == "__main__":
    while True:
        keyword = input("Input Keyword: ")
        if keyword == "":
            break
        contents = databaseHelper.selectTextMapFromKeyword(keyword, 4)
        langs = [1, 4]
        for content in contents:
            translates = databaseHelper.selectTextMapFromTextHash(content[0], langs)
            for translate in translates:
                print(translate)
            voicePath: str = selectVoicePathFromTextHash(content[0])
            if voicePath is not None:
                print(voicePath)
                audioBin = languagePackReader.getAudioBin(voicePath, 4)
                if audioBin is not None:
                    with open("Z:\\" + voicePath.replace("\\", "_"), 'wb') as f:
                        f.write(audioBin)
                    pass
                else:
                    print("Audio file deleted!")
            print("")
