# 导入语音包

以下教程针对已下载整理好的数据库，您可以从release页面下载该数据库`data.db`，然后放置在`dbBuild`文件夹下

以下教程假设您未对`DBConfig.py`做出改动，该文件可以定制目录等内容，如果您对其进行修改，则请自行调整下文中的目录。

1. 前往[https://gitlab.com/Dimbreath/AnimeGameData/-/tree/main/TextMap](https://gitlab.com/Dimbreath/AnimeGameData/-/tree/main/TextMap)下载您需要的语言的json文件，点击所需的文件进入预览页面，然后点击右边的下载图标即可。
    
    语音文件名与语言的对应关系如下：

    | 语言文件名           | 语言               | 编号 |
    |:----------------|:-----------------|:---|
    | TextMapCHS.json | 简体中文             | 1  |
    | TextMapCHT.json | 繁體中文             | 2  |
    | TextMapDE.json  | Deutsch          | 3  |
    | TextMapEN.json  | English          | 4  |
    | TextMapES.json  | Español          | 5  |
    | TextMapFR.json  | Français         | 6  |
    | TextMapID.json  | Bahasa Indonesia | 7  |
    | TextMapIT.json  | Italiano         | 8  |
    | TextMapJP.json  | 日本語              | 9  |
    | TextMapKR.json  | 한국어              | 10 |
    | TextMapPT.json  | Português        | 11 |
    | TextMapRU.json  | Русский язык     | 12 |
    | TextMapTH.json  | ภาษาไทย          | 13 |
    | TextMapTR.json  | Türkçe           | 14 |
    | TextMapVI.json  | Tiếng Việt       | 15 |
2. 将下载好的语言文件放置在`dbBuild/langs`目录下，不要修改文件名
3. 请使用`cd`命令或者`右键->在终端中打开`等方式进入`dbBuild`目录，使其成为当前的工作目录。
4. 运行`dbBuild`目录下的`textMapImport.py`文件：
    ```shell
   python textMapImport.py
    ```
   如果提示`tqdm`未找到，请先安装：
    ```shell
   pip install tqdm
    ```
5. 等待脚本运行结束，将`data.db`文件转移到上级（与`server.py`同级）目录中，

# 从头构建数据库

本节教程针对希望通过游戏数据数据直接从头构建数据库的用户。

1. 下载游戏资源：请克隆Dim的整个仓库[https://gitlab.com/Dimbreath/AnimeGameData](https://gitlab.com/Dimbreath/AnimeGameData/)到任意文件夹
2. 按照`DBConfig.py`的指引修改该文件中的目录，`LANG_PATH`可设置为`TextMap`文件夹
3. 运行`DBInit.py`来创建数据表、索引等内容，并导入一些初始数据。你也可以直接执行`databaseDDL.sql`文件中的SQL语句来初始化数据库
4. 运行`DBBuild.py`来导入语音、任务、角色等信息
5. 按照上一节的方法导入所需语言的文本数据
6. 将`data.db`文件转移到上级（与`server.py`同级）目录中，