<script setup>
import axios from "axios";
import {ref} from "vue";
import {truncate} from "../util.js";
import dayjs from "dayjs";

const dialogVisible = ref(false), dialogMode = ref('add');
const loading = ref(false), page = ref(1), page_count = ref(1), elem_per_page = ref(20), total = ref(0);
const station_id = ref(''), english_name = ref(''), chinese_name = ref(''), district = ref(''), introduction = ref('');

const data = ref([]);
const columns = [
    {
        title: 'Station ID',
        data_key: 'station_id',
    },
    {
        title: 'English Name',
        data_key: 'english_name',
    },
    {
        title: 'Chinese Name',
        data_key: 'chinese_name',
    },
    {
        title: 'District',
        data_key: 'district',
    },
    {
        title: 'Introduction',
        data_key: 'introduction',
        isSpecial: true
    }
];

function update() {
    loading.value = true;
    setTimeout(() => {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/stations',
            params: {
                page: page.value,
                elem_per_page: elem_per_page.value
            } // for GET, use params instead of data
        }).then((response) => {
            data.value = response.data.result;
            total.value = response.data.total;
            loading.value = false;
        }).catch((error) => {
            console.log(error);
            loading.value = false;
        });
    }, 500);
}

update();

function updatePage(value) {
    page.value = value;
    update();
}

function deleteStation(stationId) {
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/stations/' + stationId,
        data: {}
    });
    update();
}

function submitStationDialog() {
    dialogVisible.value = false;

    const form = new FormData();
    form.append('english_name', english_name.value);
    form.append('chinese_name', chinese_name.value);
    form.append('district', district.value);
    form.append('introduction', introduction.value);

    if (dialogMode.value === 'edit') {
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/stations/' + station_id.value,
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        });
    } else {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/stations',
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        });
    }
    update();
}

function editStation(row) {
    station_id.value = row['station_id'];
    english_name.value = row['english_name'];
    chinese_name.value = row['chinese_name'];
    district.value = row['district'];
    introduction.value = row['introduction'];

    dialogVisible.value = true;
    dialogMode.value = 'edit';
}

function addStation() {
    station_id.value = '';
    english_name.value = '';
    chinese_name.value = '';
    district.value = '';
    introduction.value = '';

    dialogVisible.value = true;
    dialogMode.value = 'add';
}
</script>

<template>
    <div class="layout-content">
        <h1 class="text-2xl absolute top-3 left-3">Stations Operations</h1>
        <el-pagination
            class="absolute top-4 left-3/4 -translate-x-full"
            background hide-on-single-page small
            :page-size="elem_per_page"
            :pager-count="6"
            layout="prev, pager, next, jumper"
            :total="total" @current-change="updatePage"
        />
        <el-button circle size="large" class="absolute top-3 right-3"
                   style="box-shadow: 0 0 2px 1px #00000014" @click="addStation()">
            <el-icon :size="20">
                <Plus/>
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
                        v-else-if="col.data_key === 'introduction'"
                    >
                        <template #reference>
                            <span class="text-xs">{{
                                    truncate(row['introduction'], 10)
                                }}</span>
                        </template>
                        <template #default>
                            <p>{{ row['introduction'] }}</p>
                        </template>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column width="160px" label="Operations">
                <template #default="{ row }">
                    <el-button type="primary" size="small" plain @click="editStation(row)">
                        Edit
                    </el-button>
                    <el-button type="danger" size="small" @click="deleteStation(row['station_id'])" plain>
                        Delete
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <el-dialog :title="(dialogMode === 'edit' ? 'Edit' : 'Add' ) + ' Station'" v-model="dialogVisible" width="500">
        <el-form>
            <el-form-item label="English Name">
                <el-input v-model="english_name" placeholder="English Name"></el-input>
            </el-form-item>
            <el-form-item label="Chinese Name">
                <el-input v-model="chinese_name" placeholder="Chinese Name"></el-input>
            </el-form-item>
            <el-form-item label="District">
                <el-dropdown>
                    <span class="el-button w-full">{{ district }}
                      <el-icon class="el-icon--right">
                        <arrow-down/>
                      </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item @click="district = '福田区'">福田区</el-dropdown-item>
                            <el-dropdown-item @click="district = '罗湖区'">罗湖区</el-dropdown-item>
                            <el-dropdown-item @click="district = '南山区'">南山区</el-dropdown-item>
                            <el-dropdown-item @click="district = '宝安区'">宝安区</el-dropdown-item>
                            <el-dropdown-item @click="district = '龙岗区'">龙岗区</el-dropdown-item>
                            <el-dropdown-item @click="district = '盐田区'">盐田区</el-dropdown-item>
                            <el-dropdown-item @click="district = '龙华区'">龙华区</el-dropdown-item>
                            <el-dropdown-item @click="district = '坪山区'">坪山区</el-dropdown-item>
                            <el-dropdown-item @click="district = '光明区'">光明区</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-form-item>
            <el-form-item label="Introduction">
                <el-input v-model="introduction" type="textarea" placeholder="Introduction"></el-input>
            </el-form-item>
        </el-form>
        <div class="text-center">
            <el-button type="primary" class="w-32" size="large" @click="submitStationDialog">
                {{ dialogMode === 'edit' ? 'Edit' : 'Add' }}
            </el-button>
        </div>
    </el-dialog>
</template>

<style scoped>

</style>