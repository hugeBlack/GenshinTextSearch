<template>

    <div class="viewWrapper">
        <h1 class="pageTitle">设置</h1>
        <div class="helpText">
            <p>所有已经导入到数据库的文本语言会在此处显示。要导入新的语言，请关闭服务器，并使用导入工具。</p>
            <p>所有游戏已下载的语言包会在此处显示。请进入游戏来管理语音包。</p>
            <p>要修改游戏资源路径，请关闭服务器并修改config.json，然后再启动服务器。</p>
        </div>
        <el-form :label-width="120" label-position="left" >
            <el-form-item label="默认搜索语言">
                <el-select v-model="selectedInputLanguage" placeholder="Select" class="languageSelector" >
                    <el-option v-for="(v,k) in supportedInputLanguage" :label="v" :value="k" :key="k"/>
                </el-select>
            </el-form-item>
            <el-form-item label="来源语言">
                <el-select v-model="selectedSourceLanguage" placeholder="Select" class="languageSelector" >
                    <el-option v-for="(v,k) in supportedInputLanguage" :label="v" :value="k" :key="k"/>
                </el-select>
            </el-form-item>
            <el-form-item label="结果语言">
                <el-transfer v-model="transferComponentValue" :data="transferComponentData" :titles="['可选语言', '已选语言']"/>
            </el-form-item>
            <el-form-item label="游戏资源路径">
                {{ global.config.assetDir }}
            </el-form-item>
            <el-form-item label="已安装语音包">
                <el-tag v-for="v in voicePacks" effect="plain" class="langPackTag">
                    {{ v }}
                </el-tag>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="save">
                    保存
                </el-button>
            </el-form-item>
        </el-form>
    </div>

</template>
<script setup>
import global from "@/global/global"
import api from "@/api/basicInfo";

import {onBeforeMount, ref} from "vue";
import {ElMessage} from "element-plus";

const selectedInputLanguage = ref(global.config.defaultSearchLanguage + '')
const selectedSourceLanguage = ref(global.config.sourceLanguage + '')
const supportedInputLanguage = ref({})

const transferComponentData = ref([])
const transferComponentValue = ref([])

const voicePacks = ref({})

onBeforeMount(async ()=>{
    supportedInputLanguage.value = global.languages

    voicePacks.value = global.voiceLanguages

    for(const [languageCode, languageName] of Object.entries(global.languages)){
        transferComponentData.value.push({
            'key': languageCode,
            'label': languageName,
            disabled: false,
        })
    }

    for(let langCode of global.config.resultLanguages){
        transferComponentValue.value.push(langCode + '')
    }


})

const save = async () => {
    let newConfig = (await api.saveConfig(transferComponentValue.value, selectedInputLanguage.value, selectedSourceLanguage.value)).json

    global.config.resultLanguages = newConfig.resultLanguages
    global.config.defaultSearchLanguage = newConfig.defaultSearchLanguage
    global.config.sourceLanguage = newConfig.sourceLanguage

    ElMessage({type: "success" ,message:"设置已保存"})
}
</script>

<style>
.viewWrapper{
    position: relative;
    width: 85%;
    margin: 0 auto;
    background-color: #fff;
    box-shadow: 0 3px 3px rgba(36,37,38,.05);
    border-radius: 3px;
    padding: 20px;
}

.pageTitle {
    border-bottom: 1px #ccc solid;
    padding-bottom: 10px;
}

.helpText {
    margin: 20px 0 20px 0;
    color: #999;
}

.langPackTag {
    margin-right: 10px;
}
</style>