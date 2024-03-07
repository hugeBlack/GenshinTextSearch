<script setup>
import {reactive, ref, watch} from "vue";
import {ElTable} from "element-plus";
import stuInfoApi from "@/api/login"

const showBox = ref(false);
let resolveFun = undefined;
let rejectFun = undefined;
let isNormalClosed = false;

const total = ref(0);
const currentPage = ref(1);

const queryForm = reactive({
    field: '',
    keyword: '',
    precise: false
})
const fields = [
    {field: "user_id", name: "用户ID"},
    {field: "stu_id", name: "学号"},
    {field: "stu_name", name: "姓名"},
]

const students = reactive({
    v:[]
})

watch(showBox, (newShowBox, oldShowBox) => {
    if(newShowBox === false && !isNormalClosed){
        onCancelClicked();
    }
})

watch(currentPage, ()=>{
    getStudents()
})

const selectStudent = () => {
    showBox.value = true;
    isNormalClosed = false;
    getStudents();
    return new Promise(function(resolve, reject){
        resolveFun = resolve;
        rejectFun = reject;
    })
}

const onSelectStudentClicked = (row) => {
    isNormalClosed = true;
    resolveFun && resolveFun(row);
    showBox.value = false;
}

const onCancelClicked = () => {
    isNormalClosed = true;
    rejectFun && rejectFun("user cancelled student selection.")
    showBox.value = false;
}

const getStudents = () =>{
    stuInfoApi.getStudentPageWithKeyword(queryForm.field, queryForm.keyword, queryForm.precise, currentPage.value).then((res)=>{
        students.v = res.json.students;
        total.value = res.json.count;
    })
}

const onClear = () => {
    queryForm.field = ''
    queryForm.keyword = ''
    queryForm.precise = false
}

defineExpose({
    selectStudent
})
</script>

<template>
<el-dialog v-model="showBox" title="选择学生">
    <el-form :inline="true" :model="queryForm" class="queryForm">
        <el-form-item label="查询字段">
            <el-select
                v-model="queryForm.field"
                clearable
                @change="()=>{queryForm.keyword=''}"
            >
                <el-option label="无" value="" />
                <el-option v-for="f in fields" :label="f.name" :value="f.field" />
            </el-select>
        </el-form-item>

        <el-form-item label="关键字" >
            <el-input v-model="queryForm.keyword" placeholder="无" clearable />
        </el-form-item>

        <el-form-item>
            <el-checkbox label="精确匹配" v-model="queryForm.precise"/>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="getStudents">筛选</el-button>
            <el-button  @click="onClear">清空</el-button>
            <span class="resultCounter">&nbsp; 共 {{total}} 个结果</span>
        </el-form-item>
    </el-form>

    <el-table
        ref="multipleTableRef"
        :data="students.v"
        style="width: 100%"
    >
        <el-table-column v-for="f in fields" :property="f.field" :label="f.name"></el-table-column>

        <el-table-column label="操作">
            <template #default="scope">
                <el-button link type="primary" size="small" @click="onSelectStudentClicked(scope.row) ">选择</el-button>
            </template>
        </el-table-column>
    </el-table>
    <div class="paginationBlock" >
        <el-pagination layout="prev, pager, next" :total="total" v-model:current-page="currentPage" :default-page-size="10"/>
    </div>
</el-dialog>
</template>

<style scoped>
.queryForm .el-input {
    --el-input-width: 220px;
}

.paginationBlock {
    display: flex;
    justify-content: center;
    margin: 10px 0;
}
</style>