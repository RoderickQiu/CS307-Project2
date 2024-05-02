<script setup>
import axios from "axios";
import {ref} from "vue";
import {truncate} from "../util.js";
import dayjs from "dayjs";

const dialogVisible = ref(false), dialogMode = ref('add');
const line_name = ref(''), start_time = ref(''), end_time = ref(''), intro = ref(''), mileage = ref(''),
    color = ref(''), first_opening = ref(''), url = ref(''), line_id = ref('')

const columns = [
    {
        title: 'Line ID',
        key: 'line_id',
        data_key: 'line_id',
        width: 50
    },
    {
        title: 'Line Name',
        key: 'line_name',
        data_key: 'line_name',
        width: 100
    },
    {
        title: 'Start Time',
        key: 'start_time',
        data_key: 'start_time',
        width: 100
    },
    {
        title: 'End Time',
        key: 'end_time',
        data_key: 'end_time',
        width: 100
    },
    {
        title: 'Intro',
        key: 'intro',
        data_key: 'intro',
        width: 200,
        isSpecial: true
    },
    {
        title: 'Mileage',
        key: 'mileage',
        data_key: 'mileage',
        width: 100
    },
    {
        title: 'Color',
        key: 'color',
        data_key: 'color',
        width: 50
    },
    {
        title: 'First Opening',
        key: 'first_opening',
        data_key: 'first_opening',
        width: 100,
        isSpecial: true
    },
    {
        title: 'URL',
        key: 'url',
        data_key: 'url',
        width: 100,
        isSpecial: true
    }];

const data = ref([]);

function update() {
    setTimeout(() => {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/lines',
            data: {}
        }).then((response) => {
            data.value = response.data;
        }).catch((error) => {
            console.log(error);
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

    if (dialogMode.value === 'edit') {
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/lines/' + line_id.value,
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        });
    } else {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/lines',
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
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
        <el-table
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