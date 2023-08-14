import csv

#将一个文件差分为两个小文件

input_file = 'account_20230803_nameTagInfo_ETH (1).csv'
output_first_file = 'ETH_accounts_3.csv'
output_remaining_file = 'ETH_accounts_4.csv'

first_rows = []
remaining_rows = []

with open(input_file, 'r', newline='',encoding='gbk',errors='ignore') as csv_in:
    csv_reader = csv.reader(csv_in)
    header = next(csv_reader)  # 读取头部

    for index, row in enumerate(csv_reader):
        if index <= 60000:
            first_rows.append(row)
        else:
            remaining_rows.append(row)

# 写入前14898行到一个新文件
with open(output_first_file, 'w', newline='',encoding='gbk',errors='ignore') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(header)
    csv_writer.writerows(first_rows)

# 写入剩余行到另一个新文件
with open(output_remaining_file, 'w', newline='',encoding='gbk',errors='ignore') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(header)
    csv_writer.writerows(remaining_rows)

print("拆分完成！")
