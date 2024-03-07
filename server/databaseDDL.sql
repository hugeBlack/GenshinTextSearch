create table main.avatar
(
    id              integer
        constraint avatar_pk
            primary key autoincrement,
    avatarId        integer,
    nameTextMapHash integer
);

create index main.avatar_avatarId_index
    on main.avatar (avatarId);

create table main.dialogue
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

create index main.dialogue_dialogueId_index
    on main.dialogue (dialogueId);

create index main.dialogue_textHash_index
    on main.dialogue (textHash);

create table main.fetters
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

create index main.fetters_voiceFileTextTextMapHash_index
    on main.fetters (voiceFileTextTextMapHash);

create index main.fetters_voiceFile_index
    on main.fetters (voiceFile);

create table main.langCode
(
    id       integer
        constraint langCode_pk
            primary key autoincrement,
    codeName TEXT
        constraint langCode_pk_2
            unique
);

create table main.textMap
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

create index main.textMap_hash_index
    on main.textMap (hash);

create index main.textMap_lang_index
    on main.textMap (lang);

create table main.voice
(
    id          integer
        constraint voice_pk
            primary key autoincrement,
    dialogueId  integer,
    voicePath   TEXT,
    gameTrigger TEXT,
    avatarId    integer
);

create index main.voice_dialogueId_index
    on main.voice (dialogueId);

