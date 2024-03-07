<template>
    <div class="viewWrapper">
        <div class="mt-4">
            <el-input
                v-model="keyword"
                style="max-width: 600px"
                placeholder="请输入关键词"
                class="input-with-select"
            >
                <template #prepend>
                    <el-select v-model="selectedInputLanguage" placeholder="Select" class="languageSelector" @change="test" >
                        <el-option v-for="(v,k) in supportedInputLanguage" :label="v" :value="k" :key="k"/>
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" @click="onQueryButtonClicked"/>
                </template>
            </el-input>

            <div>
                <TranslateDisplay v-for="translate in queryResult" :translate-obj="translate" class="translate"></TranslateDisplay>
            </div>
        </div>
    </div>

</template>

<script setup>
import {onBeforeMount, ref} from 'vue';
import { Delete, Download, Plus, ZoomIn } from '@element-plus/icons-vue';
import { Search } from '@element-plus/icons-vue'
import global from "@/global/global"
import api from "@/api/keywordQuery"
import TranslateDisplay from "@/components/TranslateDisplay.vue";

const queryLanguages = [1,4]

const queryResult = ref([])


const selectedInputLanguage = ref('4')
const keyword = ref("")
const supportedInputLanguage = ref({})

onBeforeMount(async ()=>{
    global.languages = (await api.getLangCode()).json
    supportedInputLanguage.value = global.languages
})
    //(()=>{
//     let ans = []
//     for(let k in global.languages){
//         ans.push({"val": k, "name": global.languages[k]})
//     }
//     console.log(ans)
//     return ans
// })()

const onQueryButtonClicked = async () =>{
    let ans = (await api.queryByKeyword(keyword.value, selectedInputLanguage.value)).json
    // 去重，合并相同的语音条目
    let resultMap = new Map()
    for(let item of ans){
        let key = item.translates[queryLanguages[0]]
        if(!resultMap.has(key)){
            resultMap.set(key, item)
            continue
        }
        let oldItem = resultMap.get(key)
        let voicePathsToAdd = []
        for(let newVoicePath of item.voicePaths){
            let found = false
            for(let oldVoicePath of oldItem.voicePaths){
                if(oldVoicePath === newVoicePath){
                    found = false
                    break
                }
            }
            if(!found){
                voicePathsToAdd.push(newVoicePath)
            }
        }
        if(voicePathsToAdd.length > 0){
            oldItem.voicePaths.push(...voicePathsToAdd)

        }
    }
    // 重排序，把有语音的条目拉到上面
    queryResult.value.length = 0
    let noVoiceEntries = []

    resultMap.forEach((item, key, _)=>{
        if(item.voicePaths.length > 0){
            queryResult.value.push(item)
        }else{
            noVoiceEntries.push(item)
        }
    })


    queryResult.value.push(...noVoiceEntries)
}




const test = (evt) => {
    console.log(evt)
}

</script>

<style scoped>




.viewWrapper{
    position: relative;
    width: 85%;
    margin: 0 auto;
    background-color: #fff;
    box-shadow: 0 3px 3px rgba(36,37,38,.05);
    border-radius: 3px;
    padding: 20px;
}

.languageSelector{
    width: 120px;
}

.languageSelector:deep(input){
    text-align: center;
}
.translate:not(:last-child){
    border-bottom: 1px solid #ccc;
}
</style>
