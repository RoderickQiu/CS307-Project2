import csv

# 读取CSV文件
with open('Price.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    lines = list(reader)

# 提取数据
data = []
for line in lines[3:]:
    non_empty_columns = list(filter(None, line))
    for column in range(3, len(non_empty_columns)):
        line_data = [line[0], line[1], line[2], lines[2][column], line[column]] 
        data.append(line_data)

# 导出数据到data.txt文件
with open('data.txt', 'w', encoding='utf-8') as file:
    for line_data in data:
        file.write(','.join(line_data) + '\n')

print("数据已成功提取并导出为data.txt文件。")