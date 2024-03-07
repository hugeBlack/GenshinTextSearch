import {ref} from "vue";
import {ElLoading} from "element-plus";

let _showLoading_DO_NOT_USE = ref(false);
let loadingService = ref()

let loadingCount = 0;
function startLoading(){
    //已经全局设置了自动显示和取消加载界面，不要再自己调用了！
    //每有需要加载的资源就可以调用一次，loadingCount++，loadingCount类似于一个信号量，当loadingCount>0超过300ms就会显示加载图标
    //返回loadingCount
    loadingCount++;
    // _showLoading_DO_NOT_USE.value = true;
    loadingService.value = ElLoading.service({
        lock: true,
        text: '请稍后'
    })

    return loadingCount;

}

function endLoading(){
    //已经全局设置了自动显示和取消加载界面，不要再自己调用了！
    //资源完成加载或加载失败时调用一次，使得loadingCount--，当loadingCount<=0时立即清除加载图标
    //调用了startLoading就要保证一定会在未来的某个时候调用同等次数的endLoading，否则加载图标不会消失！
    //返回loadingCount
    if(loadingCount>0){
        loadingCount--;
    }
    if(loadingCount<=0){
        loadingCount = 0;
        loadingService.value.close && loadingService.value.close()
        // _showLoading_DO_NOT_USE.value = false
    }else{
        loadingCount--;
    }
    return loadingCount;
}

export default {
    startLoading,
    endLoading,
    _showLoading_DO_NOT_USE
}