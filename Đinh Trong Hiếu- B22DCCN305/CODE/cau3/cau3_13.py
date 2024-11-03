import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Bước 1: Đọc dữ liệu từ file CSV
file_path = 'results.csv'
data = pd.read_csv(file_path, header=2)  # Đọc dữ liệu từ dòng thứ 3 (nếu cần)

# Loại bỏ các cột không phải số
data_numeric = data.select_dtypes(include=['float64', 'int64'])

# In ra kiểu dữ liệu và số lượng NaN trong các cột số
print("Kiểu dữ liệu của các cột số:")
print(data_numeric.dtypes)
print("Số lượng giá trị NaN trong các cột số:")
print(data_numeric.isnull().sum())

# Kiểm tra và xử lý NaN
if data_numeric.isnull().sum().sum() > 0:
    print("Dữ liệu chứa giá trị NaN. Đang xử lý...")
    data_numeric.fillna(data_numeric.mean(), inplace=True)  # Điền NaN bằng giá trị trung bình

# Bước 2: Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data_numeric)

# Bước 3: Áp dụng K-means với số cụm đã chọn là k=4
k = 4  # Chọn số cụm
kmeans = KMeans(n_clusters=k, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Đặt tên cho các cụm theo thứ tự: Tiền đạo, Tiền vệ, Hậu vệ, Thủ môn
cluster_names = {0: 'Tiền đạo', 1: 'Tiền vệ', 2: 'Hậu vệ', 3: 'Thủ môn'}
data['Cluster_Name'] = data['Cluster'].map(cluster_names)

# Xuất kết quả với tên cụm vào file .txt
result_txt = data[['Player', 'Cluster', 'Cluster_Name']].to_string(index=False)
with open('kmeans_results.txt', 'w', encoding='utf-8') as file:
    file.write("Kết quả phân cụm với tên:\n")
    file.write(result_txt)

# Bước 4: Giảm số chiều bằng PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Tạo DataFrame mới để lưu trữ kết quả PCA và nhãn cụm
pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
pca_df['Cluster'] = data['Cluster']
pca_df['Cluster_Name'] = pca_df['Cluster'].map(cluster_names)

# Bước 5: Trực quan hóa các cụm trên mặt phẳng 2D
plt.figure(figsize=(12, 8))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Cluster_Name', palette='viridis', s=100, alpha=0.8)
plt.title("Phân cụm K-means trên mặt phẳng 2D sau khi giảm số chiều bằng PCA")
plt.xlabel("Tấn công (PC1)")
plt.ylabel("Phòng thủ (PC2)")
plt.legend(title='Cụm')

# Lưu biểu đồ PCA vào một file ảnh
plt.savefig('pca_kmeans_clusters.png', format='png', dpi=300)
plt.show()
