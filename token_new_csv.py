import pandas as pd

# # 读取CSV文件
# csv_file_path = 'ETH_tokens_1.csv'  # 替换为你的CSV文件路径
# df = pd.read_csv(csv_file_path,encoding='gbk')
#
# # 根据指定的列进行去重
# columns_to_check = ['label_name', 'token_address', 'token_nametag']
# #columns_to_check = ['label_name', 'account_address', 'account_nametag']
# df_deduplicated = df.drop_duplicates(subset=columns_to_check)
#
# # 将去重后的数据写入新的CSV文件
# output_file_path = 'eth_token_deduplicated_file_2.csv'  # 替换为输出文件路径
# #output_file_path = 'eth_token_deduplicated_file.csv'  # 替换为输出文件路径
# df_deduplicated.to_csv(output_file_path, index=False)
#
# print("去重后的数据已保存到:", output_file_path)


# # 读取CSV文件
# csv_file_path = 'ETH_accounts_3.csv'  # 替换为你的CSV文件路径
# df = pd.read_csv(csv_file_path,encoding='gbk')
#
# # 根据指定的列进行去重
# columns_to_check = ['label_name', 'account_address', 'account_nametag']
# df_deduplicated = df.drop_duplicates(subset=columns_to_check)
#
# # 将去重后的数据写入新的CSV文件
# output_file_path = 'eth_account_deduplicated_file_3.csv'  # 替换为输出文件路径
# #output_file_path = 'eth_token_deduplicated_file.csv'  # 替换为输出文件路径
# df_deduplicated.to_csv(output_file_path, index=False)
#
# print("去重后的数据已保存到:", output_file_path)

#对爬取得到的csv文件进行去重

# 读取CSV文件
csv_file_path = 'transaction_20230727_nameTagInfo_ETH (2).csv'  # 替换为你的CSV文件路径
df = pd.read_csv(csv_file_path,encoding='gbk')

# 根据指定的列进行去重
columns_to_check = ['transaction_hash']
df_deduplicated = df.drop_duplicates(subset=columns_to_check)

# 将去重后的数据写入新的CSV文件
output_file_path = 'eth_transaction_deduplicated_file_2.csv'  # 替换为输出文件路径
#output_file_path = 'eth_token_deduplicated_file.csv'  # 替换为输出文件路径
df_deduplicated.to_csv(output_file_path, index=False)

print("去重后的数据已保存到:", output_file_path)