import sqlite3

# Dim的解包数据仓库所在的文件夹，如果只是导入语言包不用管
DATA_PATH = r'G:\AnimeGameData'

# Dim的解包数据的TextMap文件夹位置，请在其中放置需要导入的语言json，并保持其TextMapXX.json的文件名不变
LANG_PATH = r'./langs'

# 导入/生成的数据库的位置，默认为../data.db，如果要新建从头建立数据库建议选一个其他位置
conn = sqlite3.connect(r"./data.db")

# 所有数据库相关的操作请在dbBuild目录下运行脚本！
