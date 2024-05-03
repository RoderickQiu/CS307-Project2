<script setup>
import axios from "axios";
import {ref} from "vue";
import {truncate} from "../util.js";
import dayjs from "dayjs";
import {ElMessage} from "element-plus";

const dialogVisible = ref(false), dialogMode = ref('add'), loading = ref(false);
const line_name = ref(''), start_time = ref(''), end_time = ref(''), intro = ref(''), mileage = ref(''),
    color = ref(''), first_opening = ref(''), url = ref(''), line_id = ref(''), business_carriage = ref(false);

const columns = [
    {
        title: 'Line ID',
        data_key: 'line_id',
    },
    {
        title: 'Line Name',
        data_key: 'line_name',
    },
    {
        title: 'Start Time',
        data_key: 'start_time',
    },
    {
        title: 'End Time',
        data_key: 'end_time',
    },
    {
        title: 'Business',
        data_key: 'business_carriage',
        isSpecial: true
    },
    {
        title: 'Intro',
        data_key: 'intro',
        isSpecial: true
    },
    {
        title: 'Mileage',
        data_key: 'mileage',
    },
    {
        title: 'Color',
        data_key: 'color',

    },
    {
        title: 'First Opening',
        data_key: 'first_opening',
        isSpecial: true
    },
    {
        title: 'URL',
        data_key: 'url',
        isSpecial: true
    }
];

const data = ref([]);

function update() {
    loading.value = true;
    setTimeout(() => {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/lines',
            data: {}
        }).then((response) => {
            loading.value = false;
            data.value = response.data;
        }).catch((error) => {
            loading.value = false;
            console.log(error);
            ElMessage.error(error);
        });
    }, 500);
}

update();

function deleteLine(lineId) {
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/lines/' + lineId,
        data: {}
    });
    update();
}

function submitLineDialog() {
    dialogVisible.value = false;

    const form = new FormData();
    form.append('line_name', line_name.value);
    form.append('start_time', start_time.value);
    form.append('end_time', end_time.value);
    form.append('intro', intro.value);
    form.append('mileage', mileage.value);
    form.append('color', color.value);
    form.append('first_opening', dayjs(first_opening.value).format('YYYY-MM-DD'));
    form.append('url', url.value);
    form.append('business_carriage', business_carriage.value ? 1 : 0);

    if (dialogMode.value === 'edit') {
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/lines/' + line_id.value,
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        }).catch((error) => {
            console.log(error);
            ElMessage.error(error);
        });
    } else {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/lines',
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        }).catch((error) => {
            console.log(error);
            ElMessage.error(error);
        });
    }
    update();
}

function editLine(row) {
    line_id.value = row['line_id'];
    line_name.value = row['line_name'];
    start_time.value = row['start_time'];
    end_time.value = row['end_time'];
    intro.value = row['intro'];
    mileage.value = row['mileage'];
    color.value = row['color'];
    first_opening.value = dayjs(row['first_opening']).format('YYYY-MM-DD');
    url.value = row['url'];
    business_carriage.value = row['business_carriage'] === 1;

    dialogVisible.value = true;
    dialogMode.value = 'edit';
}

function addLine() {
    line_name.value = '';
    start_time.value = '';
    end_time.value = '';
    intro.value = '';
    mileage.value = '';
    color.value = '';
    first_opening.value = '';
    url.value = '';
    business_carriage.value = false;

    dialogVisible.value = true;
    dialogMode.value = 'add';
}
</script>

<template>
    <el-dialog :title="(dialogMode === 'edit' ? 'Edit' : 'Add' ) + ' Line'" v-model="dialogVisible" width="500">
        <el-form>
            <el-form-item label="Line Name">
                <el-input v-model="line_name"/>
            </el-form-item>
            <el-form-item label="Start Time">
                <el-input v-model="start_time"/>
            </el-form-item>
            <el-form-item label="End Time">
                <el-input v-model="end_time"/>
            </el-form-item>
            <el-form-item label="Intro">
                <el-input v-model="intro"/>
            </el-form-item>
            <el-form-item label="Business Carriage">
                <el-switch v-model="business_carriage"/>
            </el-form-item>
            <el-form-item label="Mileage">
                <el-input-number v-model="mileage"/>
            </el-form-item>
            <el-form-item label="Color">
                <el-input v-model="color"/>
            </el-form-item>
            <el-form-item label="First Opening">
                <el-date-picker
                    v-model="first_opening"
                    type="date"
                    placeholder="Pick a day"
                    format="YYYY-MM-DD"
                    class="w-full"
                />
            </el-form-item>
            <el-form-item label="URL">
                <el-input v-model="url"/>
            </el-form-item>
        </el-form>
        <div class="text-center">
            <el-button type="primary" class="w-32" size="large" @click="submitLineDialog">
                {{ dialogMode === 'edit' ? 'Edit' : 'Add' }}
            </el-button>
        </div>
    </el-dialog>
    <div class="layout-content">
        <h1 class="text-2xl absolute top-3 left-3">Lines Operations</h1>
        <el-button circle size="large" class="absolute top-3 right-3"
                   style="box-shadow: 0 0 2px 1px #00000014" @click="addLine()">
            <el-icon :size="20">
                <Plus/>
            </el-icon>
        </el-button>
        <el-button circle size="large" class="absolute top-3 right-16"
                   style="box-shadow: 0 0 2px 1px #00000014" @click="data = []; update()">
            <el-icon :size="20">
                <Refresh/>
            </el-icon>
        </el-button>
        <el-table
            element-loading-text="Loading..."
            v-loading="loading"
            :data="data"
            width="100%" height="calc(100vh - 5.5rem)" class="top-12"
            fit
        >
            <el-table-column v-for="col in columns" :prop="col.data_key" :label="col.title">
                <template #default="{ row }">
                    <span v-if="col.isSpecial !== true">{{ row[col.data_key] }}</span>
                    <el-popover
                        placement="right"
                        title="Introduction"
                        :width="400"
                        trigger="hover"
                        v-else-if="col.data_key === 'intro'"
                    >
                        <template #reference>
                            <span class="text-xs">{{
                                    truncate(row['intro'], 10)
                                }}</span>
                        </template>
                        <template #default>
                            <p>{{ row['intro'] }}</p>
                        </template>
                    </el-popover>
                    <a v-else-if="col.data_key === 'url'" :href="row['url']">Link</a>
                    <span v-else-if="col.data_key === 'first_opening'">{{
                            dayjs(row['first_opening']).format('YYYY-MM-DD')
                        }}</span>
                    <span v-else-if="col.data_key === 'business_carriage'">{{
                            row['business_carriage'] === 1 ? 'Yes' : 'No'
                        }}</span>
                    <span v-else>{{ row[col.data_key] }}</span>
                </template>
            </el-table-column>
            <el-table-column width="160px" label="Operations">
                <template #default="{ row }">
                    <el-button type="primary" size="small" plain @click="editLine(row)">
                        Edit
                    </el-button>
                    <el-button type="danger" size="small" @click="deleteLine(row['line_id'])" plain>
                        Delete
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<style scoped>

</style>