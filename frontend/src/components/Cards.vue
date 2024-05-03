<script setup>
import {ref} from 'vue';
import axios from "axios";
import {ElMessage} from "element-plus";
import dayjs from "dayjs";
import {becomeStyledTimeStr} from "@/util.js";

const mode = ref('Cards'), data = ref([]), loading = ref(false),
    page = ref(1), elem_per_page = ref(10), total = ref(0),
    moreDialogVisible = ref(false), dialogVisible = ref(false), currentRow = ref({}),
    currentRides = ref([]), onlineRides = ref([]), fromStation = ref(''), startTime = ref(''),
    toStation = ref(''), endTime = ref(''), price = ref(0), isBusiness = ref(false),
    currentBoarding = ref([]);

const columnsCards = [
    {
        title: 'Card Number',
        data_key: 'card_number',
    },
    {
        title: 'Money',
        data_key: 'money',
    },
    {
        title: 'Create Time',
        data_key: 'create_time',
        isSpecial: true,
    }
];
const columnsUsers = [
    {
        title: 'User ID Number',
        data_key: 'user_id_number',
    },
    {
        title: 'Name',
        data_key: 'name',
    },
    {
        title: 'Phone',
        data_key: 'phone',
    },
];
const columnsCardRide = [
    {
        title: 'Ride ID',
        data_key: 'ride_id',
    },
    {
        title: 'On the Ride',
        data_key: 'on_the_ride',
        isSpecial: true,
    },
    {
        title: 'Business',
        data_key: 'business_carriage',
        isSpecial: true,
    },
    {
        title: 'From',
        data_key: 'from_station',
    },
    {
        title: 'Start Time',
        data_key: 'start_time',
        isSpecial: true,
    },
];
const columnsUserRide = [
    {
        title: 'Ride ID',
        data_key: 'ride_id',
    },
    {
        title: 'On the Ride',
        data_key: 'on_the_ride',
        isSpecial: true,
    },
    {
        title: 'Business',
        data_key: 'business_carriage',
        isSpecial: true,
    },
    {
        title: 'From',
        data_key: 'from_station',
    },
    {
        title: 'Start Time',
        data_key: 'start_time',
        isSpecial: true,
    },
];

function getColumns() {
    if (mode.value === 'Cards') {
        return columnsCards;
    } else {
        return columnsUsers;
    }
}

function getRideColumns() {
    if (mode.value === 'Cards') {
        return columnsCardRide;
    } else {
        return columnsUserRide;
    }
}

function update() {
    loading.value = true;
    setTimeout(() => {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/' + mode.value.toLowerCase(),
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
            ElMessage.error(error);
            loading.value = false;
        });
    }, 500);
}

update();

function updatePage(value) {
    page.value = value;
    update();
}

function openDialog(row) {
    dialogVisible.value = true;
    currentRow.value = row;
    price.value = -1;
    fetchAllRides();
}

function fetchAllRides() {
    let url = mode.value === 'Cards'
        ? ('http://127.0.0.1:5000/card_rides/card/' + currentRow.value.card_number) :
        ('http://127.0.0.1:5000/user_rides/user/' + currentRow.value.user_id_number);
    setTimeout(() => {
        axios({
            method: 'get',
            url: url,
        }).then((response) => {
            currentRides.value = response.data;
            onlineRides.value = currentRides.value.filter(ride => ride.on_the_ride === 0);
        }).catch((error) => {
            console.log(error);
            ElMessage.error(error);
        });
    }, 500);
    getAllBoardingRides();
}

function getOnTheRide() {
    const form = new FormData();
    if (mode.value === 'Cards') {
        form.append('card_id', currentRow.value.card_number);
    } else {
        form.append('user_id', currentRow.value.user_id_number);
    }
    form.append('from_station', fromStation.value);
    form.append('business_carriage', isBusiness.value ? 1 : 0);
    form.append('start_time', becomeStyledTimeStr(startTime.value));
    axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/' + (mode.value === 'Cards' ? 'card' : 'user') + '_rides',
        data: form
    }).then((_response) => {
        fetchAllRides();
    }).catch((error) => {
        console.log(error);
        ElMessage.error(error);
    });
}

function getOffTheRide() {
    const form = new FormData();
    let id = onlineRides.value[0].ride_id;
    form.append('to_station', toStation.value);
    form.append('end_time', becomeStyledTimeStr(endTime.value));
    axios({
        method: 'put',
        url: 'http://127.0.0.1:5000/' + (mode.value === 'Cards' ? 'card' : 'user') + '_rides/' + id,
        data: form
    }).then((response) => {
        price.value = response.data.price;
        onlineRides.value = [];
    }).catch((error) => {
        console.log(error);
        ElMessage.error(error);
    });
}

function getAllBoardingRides() {
    axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/online'
    }).then((response) => {
        currentBoarding.value = response.data;
        console.log(currentBoarding.value)
    }).catch((error) => {
        console.log(error);
        ElMessage.error(error);
    });
}
</script>

<template>
    <div class="layout-content">
        <h1 class="text-2xl absolute top-3 left-3">
            Mode:&nbsp;
            <el-select v-model="mode" class="w-32" size="large">
                <el-option label="Cards" value="Cards" @click="update()"/>
                <el-option label="Users" value="Users" @click="update()"/>
            </el-select>
        </h1>
        <el-pagination
            class="absolute top-5 left-2/3 -translate-x-2/3"
            background hide-on-single-page small
            :page-size="elem_per_page"
            :pager-count="6"
            layout="prev, pager, next, jumper"
            :total="total" @current-change="updatePage"
        />
        <el-button circle size="large" class="absolute top-3 right-16"
                   style="box-shadow: 0 0 2px 1px #00000014" @click="update()">
            <el-icon :size="20">
                <Refresh/>
            </el-icon>
        </el-button>
        <el-button type="success" circle size="large"
                   style="box-shadow: 0 0 2px 1px #00000014" class="absolute top-3 right-4"
                   @click="getAllBoardingRides(); moreDialogVisible = true">
            <el-icon :size="20">
                <More/>
            </el-icon>
        </el-button>
        <el-table v-loading="loading" :data="data"
                  style="width: 100%; height: calc(100% - 4rem)" class="top-16">
            <el-table-column v-for="column in getColumns()" :key="column.data_key"
                             :label="column.title" :prop="column.data_key">
                <template #default="{row}">
                    <span v-if="column.isSpecial !== true">{{ row[column.data_key] }}</span>
                    <span v-else-if="column.data_key === 'create_time'">
                        {{ dayjs(row['create_time']).format('YYYY-MM-DD') }}
                    </span>
                </template>
            </el-table-column>
            <el-table-column label="Operation" width="180">
                <template #default="{row}">
                    <el-button type="primary" size="small" plain @click="openDialog(row)">
                        Take operation
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <el-dialog :title="mode + ' Operations'" v-model="dialogVisible" width="600">
        <el-form>
            <el-form-item v-if="mode === 'Cards'" label="Card Number">
                <el-input v-model="currentRow.card_number" readonly disabled/>
            </el-form-item>
            <el-form-item v-else label="User ID Number">
                <el-input v-model="currentRow.user_id_number" readonly disabled/>
            </el-form-item>
            <el-form-item label="Current Ride" v-if="onlineRides.length > 0">
                <el-table :data="onlineRides" style="width: 100%">
                    <el-table-column v-for="column in getRideColumns()" :key="column.data_key"
                                     :label="column.title" :prop="column.data_key">
                        <template #default="{row}">
                            <span v-if="column.isSpecial !== true">{{ row[column.data_key] }}</span>
                            <span v-else-if="column.data_key === 'on_the_ride'
                                || column.data_key === 'business_carriage'">
                            {{ row['on_the_ride'] ? 'No' : 'Yes' }}
                        </span>
                            <span v-else>
                            {{ dayjs(row[column.data_key]).format('MM-DD HH:mm:ss') }}
                        </span>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
            <el-form-item label="Get on the ride" v-if="onlineRides.length === 0">
                <el-input class="mb-2" placeholder="From station ID" v-model="fromStation"/>
                <el-date-picker type="datetime" class="mb-2" v-model="startTime" placeholder="Start time"/>
                <el-switch v-model="isBusiness" class="mr-2" active-text="Business ride if possible"/>
                <el-button type="primary" plain @click="getOnTheRide">Get on the ride</el-button>
            </el-form-item>
            <el-form-item label="Get off the ride" v-if="onlineRides.length > 0">
                <el-input class="mb-2" placeholder="To station ID" v-model="toStation"/>
                <el-date-picker type="datetime" class="mb-2" v-model="endTime" placeholder="End time"/>
                <el-button type="primary" plain @click="getOffTheRide">Get off the ride</el-button>
            </el-form-item>
            <el-form-item label="Price of the ride" v-if="price !== -1">
                <b>¥ {{ price }}</b>
            </el-form-item>
        </el-form>
        <br/>
        <div class="text-center">
            <el-button type="primary" class="w-32" size="large" @click="dialogVisible = false">
                Close
            </el-button>
        </div>
    </el-dialog>
    <el-dialog title="More actions" v-model="moreDialogVisible" width="800">
        <p class="text-xl mb-2">All rides that is going on</p>
        <el-table :data="currentBoarding" style="width: 100%">
            <el-table-column v-for="column in getRideColumns()" :key="column.data_key"
                             :label="column.title" :prop="column.data_key">
                <template #default="{row}">
                    <span v-if="column.isSpecial !== true">{{ row[column.data_key] }}</span>
                    <span v-else-if="column.data_key === 'on_the_ride'
                                || column.data_key === 'business_carriage'">
                            {{ row['on_the_ride'] ? 'No' : 'Yes' }}
                        </span>
                    <span v-else>
                            {{ dayjs(row[column.data_key]).format('MM-DD HH:mm:ss') }}
                        </span>
                </template>
            </el-table-column>
        </el-table>
        <br/>
        <div class="text-center">
            <el-button type="primary" class="w-32" size="large" @click="moreDialogVisible = false">
                Close
            </el-button>
        </div>
    </el-dialog>
</template>

<style scoped>

</style>