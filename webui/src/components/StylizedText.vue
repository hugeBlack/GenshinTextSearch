<script setup>
import * as textStyleParser from '@/assets/textStyleParse'
import {onBeforeMount, onMounted, ref, watch} from "vue";

const props = defineProps(['text'])

/**
 *
 * @type {Ref<HTMLDivElement>}
 */
const textWrapper = ref(null)

const getLines = (translate) => {
    return translate.split("\\n")
}

/**
 * 返回一个span dom
 * @param myDomElement{textStyleParser.MyDomElement}
 * @return HTMLSpanElement
 */

const myDomElementIterate = (myDomElement) => {
    let container = document.createElement('span')
    if (myDomElement.tagName === ''){

    } else if(myDomElement.tagName === 'color'){
        // 避免白色看不见
        if(!myDomElement.tagValue.toLowerCase().startsWith('#ffffff'))
            container.style.color = myDomElement.tagValue
    }else if(myDomElement.tagName === 'i'){
        container.style.fontStyle = 'italic'
    }else{
        console.log(`unknown tag name ${myDomElement.tagName}`)
    }

    for(let child of myDomElement.children){
        if(typeof child === 'string'){
            container.append(child)
        }else{
            container.append(myDomElementIterate(child))
        }
    }
    return container
}

const regenerateWrapperDom = (text) => {
    while(textWrapper.value.lastChild){
        textWrapper.value.removeChild(textWrapper.value.lastChild)
    }
    let lines = getLines(text)
    for(let line of lines){
        /**
         * @type {textStyleParser.MyDomElement[]}
         */
        let result = textStyleParser.parse(line)
        let p = document.createElement('p')
        for(let element of result){
            p.append(myDomElementIterate(element))
        }
        textWrapper.value.append(p)
    }

}

watch(props, (newProp)=> {
    regenerateWrapperDom(props.text)
})
onMounted(()=>{
    regenerateWrapperDom(props.text)
})


</script>

<template>
<div ref="textWrapper">

</div>
</template>

<style scoped>

</style>