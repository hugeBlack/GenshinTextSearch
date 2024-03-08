<template>
<el-upload
 
  limit="1"
  :on-change="changeFile"
  :auto-upload="false" 
  :data="uploadForm.data">
   <template #trigger>
      <el-button size="small" type="primary">选取附件</el-button>
   </template>
   <el-button style="margin-left: 10px;" size="small" type="success" 
    @click="submitUpload">上传到服务器</el-button>
</el-upload>


</template>
<script lang="ts" setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { UploadFile } from 'element-plus'; // 导入 UploadFile


const file = ref();
 
 const changeFile = (uploadFile: UploadFile) => {
     file.value = uploadFile;
 };
 const uploadForm = reactive({
    data: {
        fileId: '',
        name: '',
        type: ''
    }
});
const submitUpload = () => {
    const jsonStr = JSON.stringify(uploadForm.data);
    const blob = new Blob([jsonStr], {
        type: 'application/json'
    });
    let formData = new FormData();
    formData.append("obj", blob);
    // 这里很重要 file.value.raw才是真实的file文件，file.value只是一个Proxy代理对象
    formData.append("file", file.value.raw);
    let url = '你的后端url'
    let method = 'post'
    let headers =
    {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    axios({
        method,
        url,
        data: formData,
        headers
    }).then(res => {
        console.log(res);
        console.log(res.data);
    });
};  
</script>