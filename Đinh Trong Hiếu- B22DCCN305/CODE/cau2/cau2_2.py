import pandas as pd

# Load the data from the CSV file
file_path = 'results.csv'
data = pd.read_csv(file_path, header=2)

# Lấy các cột số để xác định chỉ số cầu thủ
numeric_columns = data.select_dtypes(include='number').columns.tolist()

# Loại bỏ các cột không phải là chỉ số (nếu cần)
exclude_columns = ['Unnamed: 0', 'Team', 'Nation', 'Position']  # các cột không phải là chỉ số
metric_columns = [col for col in numeric_columns if col not in exclude_columns]

# Khởi tạo dictionary cho DataFrame
stats = {'Team': ['All']}

# Tính toán median, mean, và std cho toàn bộ dữ liệu (tên nhóm là "All")
for column in metric_columns:
    stats[f'Median of {column}'] = [data[column].median()]
    stats[f'Mean of {column}'] = [data[column].mean()]
    stats[f'Std of {column}'] = [data[column].std()]

# Nhóm dữ liệu theo 'Team' và tính toán cho từng nhóm
grouped = data.groupby('Team')

# Tính toán median, mean, và std cho mỗi nhóm Team
for team_name, group in grouped:
    # Khởi tạo một dictionary tạm thời để lưu dữ liệu của từng Team
    team_stats = {'Team': team_name}
    for column in metric_columns:
        team_stats[f'Median of {column}'] = group[column].median()
        team_stats[f'Mean of {column}'] = group[column].mean()
        team_stats[f'Std of {column}'] = group[column].std()
    # Thêm dữ liệu của team vào stats
    for key, value in team_stats.items():
        stats.setdefault(key, []).append(value)

# Chuyển dictionary thành DataFrame
stats_df = pd.DataFrame(stats)

# Ghi DataFrame vào file CSV
output_file = 'results2.csv'
stats_df.to_csv(output_file, index=False, encoding='utf-8')

# In ra thông báo sau khi ghi dữ liệu thành công
print(f"The data has been written to the file '{output_file}'.")
