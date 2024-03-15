import os
from tqdm import tqdm
import json
from DBConfig import conn, LANG_PATH


def importTextMap(mapName: str):
    cursor = conn.cursor()
    # 检查是否已经导入

    sql2 = "select id,imported from langCode where codeName = ?"
    cursor.execute(sql2, (mapName,))
    ans2 = cursor.fetchall()
    if len(ans2) == 0:
        print("{}命名不正确或不是语言文件，已跳过".format(mapName))
        return

    langId = ans2[0][0]
    imported = ans2[0][1]
    if imported == 1:
        ans = input("{}已经似乎导入到数据库了，要重新导入吗？输入y清空该语言并重新导入，输入n取消该语言的导入")
        if ans != 'y':
            return

    sql1 = 'delete from textMap where lang=?'
    cursor.execute(sql1, (langId,))

    # 加数据
    sql3 = "insert or ignore into textMap(hash, content, lang) values (?,?,?)"
    textMap = json.load(open(LANG_PATH + "\\" + mapName, encoding='utf-8'))
    for hashVal, content in tqdm(textMap.items(), total=len(textMap)):
        cursor.execute(sql3, (hashVal, content, langId))

    # 设置为导入状态
    sql4 = 'update langCode set imported=1 where id=?'
    cursor.execute(sql4, (langId,))

    cursor.close()
    conn.commit()


def importAllTextMap():
    files = os.listdir(LANG_PATH)
    for fileName in files:
        print("Now: " + fileName)
        importTextMap(fileName)


if __name__ == "__main__":
    importAllTextMap()