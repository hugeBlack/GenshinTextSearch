create table avatar
(
    id              integer
        constraint avatar_pk
            primary key autoincrement,
    avatarId        integer,
    nameTextMapHash integer
);

create index avatar_avatarId_index
    on avatar (avatarId);

create table chapter
(
    id                      integer
        constraint chapter_pk
            primary key autoincrement,
    chapterId               integer,
    chapterTitleTextMapHash integer,
    chapterNumTextMapHash   integer
);

create index chapter_chapterId_index
    on chapter (chapterId);

create table dialogue
(
    id         integer
        constraint dialogue_pk
            primary key autoincrement,
    talkerType TEXT,
    talkerId   integer,
    talkId     integer,
    textHash   integer,
    dialogueId integer
        constraint dialogue_pk_2
            unique
);

create index dialogue_dialogueId_index
    on dialogue (dialogueId);

create index dialogue_textHash_index
    on dialogue (textHash);

create table fetters
(
    id                       integer
        constraint fetters_pk
            primary key autoincrement,
    fetterId                 integer,
    avatarId                 integer,
    voiceTitleTextMapHash    integer,
    voiceFileTextTextMapHash integer,
    voiceFile                integer
);

create index fetters_voiceFileTextTextMapHash_index
    on fetters (voiceFileTextTextMapHash);

create index fetters_voiceFile_index
    on fetters (voiceFile);

create table langCode
(
    id          integer
        constraint langCode_pk
            primary key autoincrement,
    codeName    TEXT
        constraint langCode_pk_2
            unique,
    displayName TEXT,
    imported    INT
);

create table quest
(
    id               integer
        constraint quest_pk
            primary key autoincrement,
    questId          integer,
    titleTextMapHash integer,
    chapterId        integer
);

create index quest_questId_index
    on quest (questId);

create table questTalk
(
    id      integer
        constraint questTalk_pk
            primary key autoincrement,
    questId integer,
    talkId  integer
);

create index questTalk_talkId_index
    on questTalk (talkId);

create table textMap
(
    id      integer
        constraint textMap_pk
            primary key autoincrement,
    hash    integer,
    content TEXT,
    lang    integer,
    constraint textMap_pk_2
        unique (lang, hash)
);

create index textMap_hash_index
    on textMap (hash);

create index textMap_lang_index
    on textMap (lang);

create table voice
(
    id          integer
        constraint voice_pk
            primary key autoincrement,
    dialogueId  integer,
    voicePath   TEXT,
    gameTrigger TEXT,
    avatarId    integer
);

create index voice_dialogueId_index
    on voice (dialogueId);


create table main.npc
(
    id       integer
        constraint npc_pk
            primary key autoincrement,
    npcId    integer
        constraint npc_pk_2
            unique,
    textHash integer
);

create index main.npc_npcId_index
    on main.npc (npcId);


create table main.manualTextMap
(
    id        integer
        constraint manualTextMap_pk
            primary key,
    textMapId text,
    textHash  integer
);

create unique index main.manualTextMap_textMapId_uindex
    on main.manualTextMap (textMapId);




INSERT INTO langCode (id, codeName, displayName, imported) VALUES (1, 'TextMapCHS.json', '简体中文', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (2, 'TextMapCHT.json', '繁體中文', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (3, 'TextMapDE.json', 'Deutsch', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (4, 'TextMapEN.json', 'English', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (5, 'TextMapES.json', 'Español', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (6, 'TextMapFR.json', 'Français', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (7, 'TextMapID.json', 'Bahasa Indonesia', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (8, 'TextMapIT.json', 'Italiano', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (9, 'TextMapJP.json', '日本語', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (10, 'TextMapKR.json', '한국어', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (11, 'TextMapPT.json', 'Português', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (12, 'TextMapRU.json', 'Русский язык', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (13, 'TextMapTH.json', 'ภาษาไทย', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (14, 'TextMapTR.json', 'Türkçe', 0);
INSERT INTO langCode (id, codeName, displayName, imported) VALUES (15, 'TextMapVI.json', 'Tiếng Việt', 0);

