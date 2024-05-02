export const truncate = (str, n = 20) => {
    return str.length > n ? str.substr(0, n - 1) + '...' : str;
}