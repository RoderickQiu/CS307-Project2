import dayjs from "dayjs";

export const truncate = (str, n = 20) => {
    if (!str) return "";
    return str.length > n ? str.substr(0, n - 1) + '...' : str;
}

export const becomeStyledTimeStr = (timeStr) => {
    let parsedTime = dayjs(timeStr);
    return parsedTime.format('YYYY-MM-DDTHH:mm:ss');
}

export const firstLetterUppercase = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

export const getErrorMessage = (error) => {
    return error.response && error.response.data.error ? error.response.data.error : error.message;
}