import pandas as pd
import os

# Hàm mới: Đọc dữ liệu từ file CSV có sẵn trong source code
def load_metadata_from_csv():
    # Đường dẫn tới file datasets.csv nằm cùng thư mục services
    csv_path = os.path.join(os.path.dirname(__file__), "datasets.csv")
    
    if os.path.exists(csv_path):
        # Đọc file CSV
        df = pd.read_csv(csv_path)
        # Đảm bảo có cột ID (nếu CSV thiếu) để model hoạt động
        if 'id' not in df.columns:
            df['id'] = df.index + 1
        return df
        
    # Trả về DataFrame rỗng nếu không thấy file
    return pd.DataFrame(columns=["id", "title", "description", "tags", "text_sample"])