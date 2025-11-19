import pandas as pd
import os

# Hàm này sẽ đọc dữ liệu mẫu từ file CSV có sẵn
def load_metadata_from_csv():
    """
    Tải metadata từ datasets.csv để train model AI.
    """
    # Đường dẫn file datasets.csv nằm cùng thư mục này
    csv_path = os.path.join(os.path.dirname(__file__), "datasets.csv")
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Thêm cột ID nếu thiếu (để model recommend hoạt động)
            if 'id' not in df.columns:
                df['id'] = df.index + 1
            return df
        except Exception as e:
            print(f"Lỗi đọc file datasets.csv: {e}")
            
    # Trả về DataFrame rỗng nếu có lỗi hoặc không tìm thấy file
    return pd.DataFrame(columns=["id", "title", "description", "tags", "text_sample"])

# Hàm cũ dùng để đọc từ DB (giữ lại để tránh lỗi import ở các file khác)
def load_metadata_from_db(db):
    print("WARNING: Using dummy DB function. AI should load from CSV.")
    return load_metadata_from_csv()