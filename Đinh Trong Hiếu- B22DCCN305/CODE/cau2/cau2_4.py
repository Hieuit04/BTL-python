import pandas as pd

# Đường dẫn đến file CSV đã tải lên
file_path = 'results2.csv'

# Đọc dữ liệu từ file CSV
data = pd.read_csv(file_path)

# Lấy các cột số để xác định chỉ số
numeric_columns = data.select_dtypes(include='number').columns.tolist()

# Loại bỏ các cột không phải là chỉ số (nếu cần)
exclude_columns = ['Unnamed: 0', 'Team', 'Nation', 'Position']  # các cột không phải là chỉ số
metric_columns = [col for col in numeric_columns if col not in exclude_columns]

# Khởi tạo dictionary để lưu thông tin đội có chỉ số cao nhất ở mỗi chỉ số
team_top_metrics = {}

# Tìm đội có chỉ số cao nhất ở mỗi chỉ số
for column in metric_columns:
    top_team_row = data[['Team', column]].sort_values(by=column, ascending=False).head(1)
    team_name = top_team_row['Team'].values[0]
    max_value = top_team_row[column].values[0]

    # Lưu kết quả vào dictionary
    team_top_metrics[column] = {
        'Team': team_name,
        'Max_Value': max_value
    }

# Đếm số lượng chỉ số cao nhất mà mỗi đội có
team_performance = {}
for metric, info in team_top_metrics.items():
    team_name = info['Team']
    team_performance[team_name] = team_performance.get(team_name, 0) + 1

# Tìm đội có phong độ tốt nhất
best_team = max(team_performance, key=team_performance.get)
best_team_metrics_count = team_performance[best_team]

# Ghi kết quả vào file txt
with open('results4.txt', 'w', encoding='utf-8') as f:
    f.write("Đội có chỉ số cao nhất ở mỗi chỉ số:\n")
    for metric, info in team_top_metrics.items():
        f.write(f"Chỉ số: {metric}, Đội: {info['Team']}, Giá trị lớn nhất: {info['Max_Value']}\n")
    
    f.write(f"\nĐội có phong độ tốt nhất: {best_team} với {best_team_metrics_count} chỉ số cao nhất.\n")

print("Kết quả đã được ghi vào file 'results4.txt'.")
