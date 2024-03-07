<script setup>
import { reactive, ref } from "vue";
import router from "@/router";
import axios from "axios";

const showingMessages = reactive({ data: [] })

const messages = reactive({ data: [] })
const isLoading = ref(false);

const showMsg = ref(true)

const isExpended = ref(false)

const toggleExpended = () => {
    isExpended.value = !isExpended.value
    showMsg.value = false
    copyShowingMsg()
    setTimeout(() => {
        showMsg.value = true
    }, 0)
}

// 将要展示的msg复制到showingMessages
const copyShowingMsg = () => {
    showingMessages.data = []
    for (let msg of messages.data) {
        // console.log(msg)
        if (isExpended.value || !msg.is_read) {
            showingMessages.data.push(msg)
        }
    }
}

const getNotification = () => {
    isLoading.value = true
    isExpended.value = false
    axios.get("/api/notice/getPersonalNotice", { doNotShowLoadingScreen: true }).then((res) => {
        isLoading.value = false;
        showMsg.value = false;
        // console.log(res)
        messages.data = res.data.data.noticeList;
        copyShowingMsg()
        // console.log(messages.data)
        // console.log(showingMessages.data)
        setTimeout(() => {
            showMsg.value = true
        }, 0)
    }).catch(error => {
        if (error.network) return;
        error.defaultHandler("消息加载失败");
    })
}

defineExpose({ getNotification })
const goUrl = (url) => {
    if (url) router.push("/" + url);
}

const clearMessages = () => {
    messages.data = [];
    showingMessages.data = [];
    axios.get("/api/notice/clearPersonalNotice", { doNotShowLoadingScreen: true })
}
</script>

<template>
    <p class="title">
        消息通知
    </p>
    <div class="messageWrapper">
        <p class="messagePlaceHolder" v-if="showingMessages.data.length === 0">
            {{
                (() => {
                    if (isLoading) return "加载中"
                    if (messages.data.length === 0) return "没有消息"
                    if (showingMessages.data.length === 0) return "没有新消息"
                })()

            }}
        </p>
        <div class="messageEntry" v-if="showMsg" v-for="item of showingMessages.data" :class="{ clickable: item.related_link }"
            @click="goUrl(item.related_link)">
            <div class="content">
                <span class="dotWrapper" v-if="!item.is_read">
                    <span class="unreadDot"></span>
                </span>
                <span>{{ item.content }}</span>
                <!-- <span>{{ item.send_time }}</span> -->
            </div>
            <div class="goButton" v-if="item.related_link">
                <i class="fi fi-rr-angle-small-right centerIcon"></i>
            </div>
        </div>
    </div>
    <p class="messageControls" v-if="messages.data.length > 0">
        <el-button class="clearButton" @click="toggleExpended" link>
            <i class="fi centerIcon"
                :class="{ 'fi-rr-angle-down': !isExpended, ' fi-rr-angle-up': isExpended }"></i><span>{{ isExpended ? "收起" :
                    "展开全部" }}</span>
        </el-button>
        <el-button class="clearButton" @click="clearMessages" link>
            <i class="fi fi-rr-trash centerIcon"></i><span>全部已读</span>
        </el-button>
    </p>
</template>

<style scoped>
.title {
    padding: 15px;
    text-align: center;
    border-bottom: 1px solid #ccc;
}

.messageWrapper {
    max-height: 300px;
    overflow: hidden auto;
}

.messageWrapper::-webkit-scrollbar {
    width: 5px;
    height: 100%
}

.messageWrapper::-webkit-scrollbar-thumb {
    background: #bbb;
    border-radius: 5px;
}

.messageEntry {
    min-width: 50px;
    padding: 15px;
    transition: 0.2s ease-in-out;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    line-height: 1.5em;
    position: relative;
}

.messageWrapper>*:not(:last-child):after {
    border-bottom: 1px solid #ccc;
    bottom: 0;
    height: 1px;
    left: 0;
    margin: 0 16px;
    position: absolute;
    right: 0;
    background-clip: content-box;
    content: "";
}

.messageEntry:hover {
    background-color: rgb(246, 246, 246);
}

.messageEntry.clickable {
    cursor: pointer;
}

.messagePlaceHolder {
    padding: 40px 15px;
    text-align: center;
    color: #ccc;
}

.goButton {
    display: flex;
    align-items: center;
    margin-left: 3px;
}

.goButton i {
    margin: 0;
    transition: 0.3s ease-in-out;
}

.messageEntry:hover i {
    transform: translateX(3px);
}

.dotWrapper {
    height: 1.4em;
    margin-right: 10px;
    display: inline-flex;
    align-items: center;
    vertical-align: text-top;
}

.unreadDot {
    height: 6px;
    width: 6px;
    display: block;
    background-color: var(--el-color-error);
    border-radius: 50%;
}

.messageControls {
    text-align: center;
    padding: 10px;
    border-top: 1px solid #ccc;
}

.messageControls>button {
    font-weight: 400;
    color: #999;
}
</style>