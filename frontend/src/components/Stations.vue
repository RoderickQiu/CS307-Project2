<script setup>
import axios from "axios";
import {h, ref} from "vue";
import {firstLetterUppercase, getErrorMessage, truncate} from "../util.js";
import dayjs from "dayjs";
import {ElMessage, ElMessageBox} from "element-plus";
import {first} from "lodash-es";

const dialogVisible = ref(false), dialogMode = ref('add'), moreDialogVisible = ref(false);
const loading = ref(false), page = ref(1), page_count = ref(1), elem_per_page = ref(20), total = ref(0);
const station_id = ref(''), english_name = ref(''), chinese_name = ref(''), district = ref(''), introduction = ref(''),
    status = ref('opening');
const selectedLine = ref(''), selectedOperation = ref(''), operationVal = ref(''), operationVal2 = ref('');

const data = ref([]), dataLines = ref([]), dataStationsOnLine = ref([]);
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
    },
    {
        title: 'Status',
        data_key: 'status',
        isSpecial: true
    }
];
let columnsOnLine = columns.slice();
columnsOnLine.push({
    title: 'Line Num',
    data_key: 'line_num',
});
columnsOnLine = columnsOnLine.filter((col) => col.data_key !== 'introduction');

function updateLines() {
    setTimeout(() => {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/lines',
            data: {}
        }).then((response) => {
            dataLines.value = response.data;
        }).catch((error) => {
            ElMessage.error(getErrorMessage(error));
            console.log(error);
        });
    }, 500);
}

function addStationOnLine() {
    const form = new FormData();
    form.append('line_num', operationVal2.value);
    axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/lines/' + selectedLine.value + '/stations/' + operationVal.value,
        data: form,
    }).then(() => {
        setTimeout(() => {
            fetchStationsOnLine(selectedLine.value);
        }, 500);
    }).catch((error) => {
        ElMessage.error(getErrorMessage(error));
        console.log(error);
    });
}

function deleteStationOnLine() {
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/lines/' + selectedLine.value + '/stations/' + operationVal.value,
    }).then(() => {
        setTimeout(() => {
            fetchStationsOnLine(selectedLine.value);
        }, 500);
    }).catch((error) => {
        console.log(error);
        ElMessage.error(getErrorMessage(error));
    });
}

function getStationWithDistanceN() {
    axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/lines/' + selectedLine.value + '/stations/' + operationVal.value + '/n/' + operationVal2.value,
    }).then((response) => {
        if (response.data.hasOwnProperty('station_id')) {
            let flag = false;
            let stationID = response.data['station_id'], stationName = '';
            for (let i = 0; i < dataStationsOnLine.value.length; i++) {
                if (dataStationsOnLine.value[i]['station_id'] === stationID) {
                    stationName = dataStationsOnLine.value[i]['english_name'];
                    ElMessageBox({
                        title: 'Result',
                        message: h('div', null, [
                            h('p', null, [
                                h('span', {style: 'font-weight: bold'}, 'Station ID: '),
                                h('span', null, stationID),
                            ]),
                            h('p', null, [
                                h('span', {style: 'font-weight: bold'}, 'Station Name: '),
                                h('span', null, stationName),
                            ]),
                        ]),
                        confirmButtonText: 'OK',
                    })
                    flag = true;
                    break;
                }
            }
            if (!flag) {
                ElMessageBox.alert('No such station on this line', 'Error', {
                    confirmButtonText: 'OK',
                });
            }
        } else {
            ElMessageBox.alert('No such station', 'Error', {
                confirmButtonText: 'OK',
            })
        }
    }).catch((error) => {
        ElMessage.error(getErrorMessage(error));
        console.log(error);
    });
}

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
            ElMessage.error(getErrorMessage(error));
            loading.value = false;
        });
    }, 500);
}

update();
updateLines();

function updatePage(value) {
    page.value = value;
    update();
}

function deleteStation(stationId) {
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/stations/' + stationId,
        data: {}
    }).catch((error) => {
        console.log(error);
        ElMessage.error(getErrorMessage(error));
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
    form.append('status', status.value);

    if (dialogMode.value === 'edit') {
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/stations/' + station_id.value,
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        }).catch((error) => {
            console.log(error);
            ElMessage.error(getErrorMessage(error));
        });
    } else {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/stations',
            data: form,
            headers: {'Content-Type': `multipart/form-data; boundary=${form._boundary}`}
        }).catch((error) => {
            console.log(error);
            ElMessage.error(getErrorMessage(error));
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
    status.value = row['status'];

    dialogVisible.value = true;
    dialogMode.value = 'edit';
}

function addStation() {
    station_id.value = '';
    english_name.value = '';
    chinese_name.value = '';
    district.value = '';
    introduction.value = '';
    status.value = 'opening';

    dialogVisible.value = true;
    dialogMode.value = 'add';
}

function fetchStationsOnLine(lineId) {
    dataStationsOnLine.value = [];
    axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/lines/' + lineId + '/stations',
    }).then((response) => {
        dataStationsOnLine.value = response.data;
    }).catch((error) => {
        console.log(error);
        ElMessage.error(getErrorMessage(error));
    });
}

function getStatusText(status) {
    switch (status) {
        case 'opening':
            return 'Opening';
        case 'under':
            return 'Under construction';
        case 'closed':
            return 'Closed';
        default:
            return 'Unknown';
    }
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
        <div class="absolute top-2.5 right-3">
            <el-button circle size="large"
                       style="box-shadow: 0 0 2px 1px #00000014" @click="addStation()">
                <el-icon :size="20">
                    <Plus/>
                </el-icon>
            </el-button>
            <el-button circle size="large"
                       style="box-shadow: 0 0 2px 1px #00000014" @click="data = []; update(); updateLines()">
                <el-icon :size="20">
                    <Refresh/>
                </el-icon>
            </el-button>
            <el-button type="success" circle size="large"
                       style="box-shadow: 0 0 2px 1px #00000014"
                       @click="dataStationsOnLine = []; moreDialogVisible = true">
                <el-icon :size="20">
                    <More/>
                </el-icon>
            </el-button>
        </div>
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
                    <span v-else-if="col.data_key === 'status'">{{ getStatusText(row['status']) }}</span>
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
    <el-dialog title="More actions" v-model="moreDialogVisible" width="800">
        <el-form>
            <el-form-item label="Select Line">
                <el-select aria-label="Select Line" v-model="selectedLine" placeholder="Select a line name"
                           style="width: 100%">
                    <el-option
                        v-for="item in dataLines"
                        :key="item.line_id"
                        :label="item.line_name"
                        :value="item.line_id"
                        @click="fetchStationsOnLine(item.line_id)"
                    />
                </el-select>
            </el-form-item>
            <div v-if="dataStationsOnLine.length > 0">
                <el-table
                    element-loading-text="Loading..."
                    v-loading="loading"
                    :data="dataStationsOnLine"
                    fit max-height="200px"
                >
                    <el-table-column v-for="col in columnsOnLine" :prop="col.data_key" :label="col.title">
                        <template #default="{ row }">
                            <span v-if="col.isSpecial !== true">{{ row[col.data_key] }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <br/>
                <el-form-item label="Select Operation">
                    <el-select v-model="selectedOperation">
                        <el-option label="Add one or more stations" value="add_station"/>
                        <el-option label="Delete station on line" value="delete_station"/>
                        <el-option label="Get station with distance n" value="get_station_with_distance_n"/>
                    </el-select>
                </el-form-item>
                <el-form-item v-if="selectedOperation === 'add_station'">
                    <el-input placeholder="Station ID or IDs, e.g. [id1,id2,id3]" v-model="operationVal"
                              style="width: calc(50% - 40px)"/>
                    <el-input placeholder="Line num to insert" v-model="operationVal2"
                              style="width: calc(50% - 48px); margin-left: 8px"/>
                    <el-button @click="addStationOnLine" style="width: 72px; margin-left: 8px">Add</el-button>
                </el-form-item>
                <el-form-item v-else-if="selectedOperation === 'delete_station'">
                    <el-input placeholder="Station ID to delete" v-model="operationVal"
                              style="width: calc(100% - 80px)"/>
                    <el-button type="danger" style="width: 72px; margin-left: 8px" @click="deleteStationOnLine">Delete
                    </el-button>
                </el-form-item>
                <el-form-item v-else-if="selectedOperation === 'get_station_with_distance_n'">
                    <el-input placeholder="Station ID" v-model="operationVal"
                              style="width: calc(50% - 40px)"/>
                    <el-input placeholder="Distance (pos. for ahead, neg. for behind)" v-model="operationVal2"
                              style="width: calc(50% - 48px); margin-left: 8px"/>
                    <el-button class="operation-btn" @click="getStationWithDistanceN">Get</el-button>
                </el-form-item>
            </div>
            <el-form-item v-else>
                <span class="w-full text-center !text-gray-400">No data</span>
            </el-form-item>
        </el-form>
        <br/>
        <div class="text-center">
            <el-button type="primary" class="w-32" size="large" @click="moreDialogVisible = false">
                Close
            </el-button>
        </div>
    </el-dialog>
    <el-dialog :title="(dialogMode === 'edit' ? 'Edit' : 'Add' ) + ' Station'" v-model="dialogVisible" width="500">
        <el-form>
            <el-form-item label="English Name">
                <el-input v-model="english_name" placeholder="English Name"></el-input>
            </el-form-item>
            <el-form-item label="Chinese Name">
                <el-input v-model="chinese_name" placeholder="Chinese Name"></el-input>
            </el-form-item>
            <el-form-item label="Status">
                <el-dropdown>
                    <span class="el-button w-full">{{ getStatusText(status) }}
                      <el-icon class="el-icon--right">
                        <arrow-down/>
                      </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item @click="status = 'opening'">Opening</el-dropdown-item>
                            <el-dropdown-item @click="status = 'under'">Under construction
                            </el-dropdown-item>
                            <el-dropdown-item @click="status = 'closed'">Closed</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
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