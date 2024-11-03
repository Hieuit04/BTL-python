import pandas as pd

# Load the data from the CSV file
file_path = 'results.csv'
data = pd.read_csv(file_path, header=2)

# Lấy các cột số để xác định chỉ số cầu thủ
numeric_columns = data.select_dtypes(include='number').columns.tolist()

# Loại bỏ các cột không phải là chỉ số (nếu cần)
exclude_columns = ['Unnamed: 0', 'Team', 'Nation', 'Position']  # các cột không phải là chỉ số
metric_columns = [col for col in numeric_columns if col not in exclude_columns]

# Khởi tạo dictionary để lưu kết quả
top_bottom_players = {}

# Tìm top 3 và bottom 3 cầu thủ ở mỗi chỉ số
for column in metric_columns:
    # Sắp xếp giảm dần để lấy top 3, tăng dần để lấy bottom 3
    top_3 = data[['Player', column]].sort_values(by=column, ascending=False).head(3)
    bottom_3 = data[['Player', column]].sort_values(by=column, ascending=True).head(3)
    
    # Lưu kết quả
    top_bottom_players[column] = {
        'top_3': top_3,
        'bottom_3': bottom_3
    }

# Ghi kết quả vào tệp văn bản
with open('results1.txt', 'w', encoding='utf-8') as f:
    for metric, results in top_bottom_players.items():
        f.write(f"\nChỉ số: {metric}\n")
        f.write("Top 3:\n")
        f.write(results['top_3'].to_string(index=False))
        f.write("\nBottom 3:\n")
        f.write(results['bottom_3'].to_string(index=False))
        f.write("\n" + "="*40 + "\n")

# In ra thông báo sau khi ghi dữ liệu thành công
print("Dữ liệu đã được ghi vào file 'results1.txt'.")
