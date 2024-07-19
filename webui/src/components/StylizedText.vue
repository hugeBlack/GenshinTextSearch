<script setup>
import * as textStyleParser from '@/assets/textStyleParse'
import {onBeforeMount, onMounted, ref, watch} from "vue";

const props = defineProps(['text', 'keyword'])

/**
 *
 * @type {Ref<HTMLDivElement>}
 */
const textWrapper = ref(null)

const loweredKeyword = ref("")

const getLines = (translate) => {
    return translate.split("\\n")
}

/**
 * @param str{String}
 * @param kw{String}
 */
const getAllOccurrences = (str, kw) => {
    let ans = []
    if(!str) return ans

    let i = 0;
    while(i !== -1){
        i = str.indexOf(kw, i);
        if(i !== -1){
            ans.push(i)
            i += kw.length
        }
    }
    return ans;
}

/**
 * 根据传入的myDomElement构造一个一层的container Dom元素
 * @param myDomElement{textStyleParser.MyDomElement} 正在处理的myDomElement
 * @return HTMLSpanElement
 */
const createElementByMyElement = (myDomElement) => {
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
    return container
}

/**
 * 返回一个span dom
 * @param myDomElement{textStyleParser.MyDomElement} 正在处理的myDomElement
 * @param lineHtmlElements {HTMLParagraphElement[]} 所有的p元素，一开始得有一个在里面
 * @param containerStack {HTMLElement[]} container dom元素的栈，一开始是初始的p元素，会把最后一个元素作为容器元素
 * @param currentLabelStack {textStyleParser.MyDomElement[]} 当前样式栈
 */

const myDomElementIterate = (myDomElement, lineHtmlElements, containerStack, currentLabelStack) => {
    let container = containerStack[containerStack.length - 1]
    if(myDomElement.tagName !== 'root')
        currentLabelStack.push(myDomElement)

    for(let child of myDomElement.children){
        if(typeof child === 'string'){
            let lines = getLines(child)

            for(let i = 0; i < lines.length; ++i) {
                let line = lines[i];
                // 遇到换行，要复制一颗格式树，即要修改containerStack的所有内容
                if(i > 0) {
                    let newP = document.createElement('p')
                    lineHtmlElements.push(newP)
                    containerStack[0] = newP

                    /**
                     * @type {HTMLSpanElement}
                     */
                    let newContainer = undefined
                    let i = 1
                    for(let curDomElement of currentLabelStack){
                        if(newContainer) {
                            let nowContainer = createElementByMyElement(curDomElement)
                            newContainer.append(nowContainer)
                            newContainer = nowContainer
                            container = nowContainer
                        } else {
                            newContainer = createElementByMyElement(curDomElement)
                            container = newContainer
                            newP.append(newContainer)
                        }
                        containerStack[i] = newContainer
                        ++i;
                    }

                }

                // 高亮搜索关键字
                if(props.keyword){
                    let indices = getAllOccurrences(line.toLowerCase(), loweredKeyword.value);
                    if (indices.length === 0){
                        container.append(line)
                    }else{
                        let i = 0
                        for(let sub of indices){
                            if(i >= line.length)
                                break
                            container.append(line.substring(i, sub))
                            let keywordContainer = document.createElement('span')
                            keywordContainer.append(line.substring(sub, sub + props.keyword.length))
                            keywordContainer.classList.add("keywordSpan")
                            container.append(keywordContainer)
                            i = sub + props.keyword.length
                        }
                        if(i < line.length){
                            container.append(line.substring(i))
                        }
                    }
                } else {
                    container.append(line)
                }
            }


        }else{
            let childContainer = createElementByMyElement(child)
            containerStack.push(childContainer)
            container.append(childContainer)
            myDomElementIterate(child, lineHtmlElements, containerStack, currentLabelStack)
        }
    }
    currentLabelStack.pop()
    containerStack.pop()

}

const regenerateWrapperDom = (text) => {
    loweredKeyword.value = props.keyword.toLowerCase()
    while(textWrapper.value.lastChild){
        textWrapper.value.removeChild(textWrapper.value.lastChild)
    }

    let result = new textStyleParser.MyDomElement();
    result.children = textStyleParser.parse(text)
    result.tagName = 'root'
    let p = document.createElement('p')
    let lineElements = [p]
    let containerElements = [p]
    let currentLabelStack = []
    myDomElementIterate(result, lineElements, containerElements, currentLabelStack)
    for(let element of lineElements)
        textWrapper.value.append(element)


}

watch(props, (newProp)=> {
    regenerateWrapperDom(props.text)
})
onMounted(()=>{
    regenerateWrapperDom(props.text)
})


</script>

<template>
<div ref="textWrapper" class="textWrapper">

</div>
</template>

<style scoped>
.textWrapper {
    word-break: normal;
}
</style>