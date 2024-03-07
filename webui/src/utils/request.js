import axios from 'axios';
import loadingScreen from "@/global/loading";
import {ElMessage, ElMessageBox} from "element-plus";
import router from "@/router";

const service = axios.create({
    headers: {},
    timeout:5000,

})

if(import.meta.env.VITE_AXIOS_BASE_URL) service.defaults.baseURL = import.meta.env.VITE_AXIOS_BASE_URL

//发送请求时自动显示加载界面
service.interceptors.request.use((config) => {
    if(!config.doNotShowLoadingScreen)
        loadingScreen.startLoading()
    return config;
},);
//请求错误或者返回时自动清除加载界面
service.interceptors.response.use(function (response) {
    loadingScreen.endLoading()
    if(response.data.code!==200){
        return Promise.reject({
            network: false,
            response: response,
            errorCode: response.data.code,
            defaultHandler: (prefix) =>{
                if(response.data.msg){
                    ElMessage.error((prefix ? prefix : "错误") + ": " + response.data.msg)
                    return;
                }
                console.log(response.data.code)
                switch (response.data.code){
                    case 400:
                        ElMessage.error("参数错误")
                        return;
                    case 403:
                        if(response.data.msg)
                            ElMessage.error(response.data.msg)
                        else
                            ElMessage.error("拒绝访问")
                        return;
                    case 404:
                        router.replace("/error")
                        return;
                    case 500:
                        ElMessage.error("服务器错误");
                        console.error(response.data)
                        return;
                    case 550:
                        ElMessage.error("接口未实现");
                        return;
                }
                ElMessage.error((prefix ? prefix : "错误代码") + "：" + response.data.code)
            }
        });
    }else{
        response.json = response.data.data
        return response
    }
}, function (error) {
    loadingScreen.endLoading()
    if(error.code === "ERR_NETWORK"){
        error.network = true;
        ElMessage.error("网络错误，请检查网络连接")
        error.defaultHandler = () => {}
        return Promise.reject(error);
    }
    if(error.network === false){
        return Promise.reject(error);
    }
    loadingScreen.endLoading();
    switch(error.response.status){
        case 415:
            ElMessage.error("接口未实现或请求方法设置错误")
            break;
        case 413:
            ElMessage.error("上传的文件过大")
            break;
        default:
            ElMessage.error('网络错误：'+error.message)
    }

    return Promise.reject({
        network: true,
        error: error
    });
});

export default service
