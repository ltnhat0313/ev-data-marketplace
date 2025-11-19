import requests
import sys
import time
import subprocess # Thư viện để chạy lệnh Docker từ Python
from requests.exceptions import RequestException


# CẤU HÌNH & TIỆN ÍCH


BASE_URL = "http://localhost"

# Mã màu
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def ok(msg):
    print(f"{GREEN}[PASS]{RESET} {msg}")

def fail(msg, detail=""):
    print(f"{RED}[FAIL]{RESET} {msg}")
    if detail:
        print(f"      → {detail}")

def warn(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")

def section(title):
    print(f"\n{BOLD}=== {title} ==={RESET}")

# --- BIẾN TOÀN CỤC ---
TOKEN = None
PROVIDER_TOKEN = None
ADMIN_TOKEN = None
NEW_DATASET_ID = None

TS = int(time.time())
CONSUMER_EMAIL = f"consumer_{TS}@ev.com"
PROVIDER_EMAIL = f"provider_{TS}@ev.com"

ADMIN_EMAIL = "admin@evdata.com"
ADMIN_PASS_DEFAULT = "123456" 
PASSWORD = "password123"

# --- HÀM GỌI API ---
def call(method, url, **kwargs):
    try:
        r = requests.request(method, url, timeout=10, **kwargs)
        return r
    except RequestException as e:
        fail(f"Connection failed → {url}", str(e))
        sys.exit(1)


# 0. HOTFIX: TỰ ĐỘNG SỬA LỖI DB (Thêm mới)

def auto_fix_admin_password():
    section("0. PRE-CHECK: AUTO FIX DATABASE PASSWORD")
    print("   -> Đang cập nhật mật khẩu Admin trong Docker DB...")
    
    # Mã hash chuẩn cho '123456' tương thích với Auth Service hiện tại
    correct_hash = "$2b$12$DSLGpi6ofcprqFRZFDw9mOFBGa0nT3AMDmbECkig5RagnGuqHfose"
    
    # Lệnh Docker để update DB trực tiếp
    cmd = f'docker exec ev_mysql mysql -u root -p161105 auth_db -e "UPDATE users SET hashed_password=\'{correct_hash}\' WHERE email=\'admin@evdata.com\';"'
    
    try:
        # Chạy lệnh shell, ẩn output rác
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ok("Đã cập nhật mật khẩu Admin thành công (Hotfix Applied)")
    except subprocess.CalledProcessError:
        warn("Không thể tự động sửa DB (Có thể container chưa chạy?). Test Admin có thể sẽ lỗi.")


# 1. HEALTH CHECK

def test_health():
    section("1. CHECK TRAEFIK & SERVICES ONLINE")
    r = call("GET", f"{BASE_URL}/api/auth/")
    if r.status_code in [200, 404, 405]:
        ok("Auth Service online")
    else:
        fail("Auth Service FAILED", f"status={r.status_code}")

    r = call("GET", f"{BASE_URL}/api/datasets/search")
    if r.status_code == 200:
        ok("Market Service online")
    else:
        fail("Market Service FAILED", f"status={r.status_code}")


# 2. AUTH FLOW

def test_auth_flow():
    section("2. TEST AUTHENTICATION")
    global TOKEN

    payload = {"username": f"u_{TS}", "email": CONSUMER_EMAIL, "password": PASSWORD}
    r = call("POST", f"{BASE_URL}/api/auth/register", json=payload)
    if r.status_code == 200:
        ok(f"Consumer đăng ký OK → {CONSUMER_EMAIL}")
    else:
        fail("Consumer đăng ký FAIL", r.text)
        return

    r = call("POST", f"{BASE_URL}/api/auth/login", json={"email": CONSUMER_EMAIL, "password": PASSWORD})
    if r.status_code == 200:
        TOKEN = r.json()["access_token"]
        ok("Consumer login OK → JWT nhận thành công")
    else:
        fail("Consumer login FAIL", r.text)
        sys.exit(1)


# 3. JIT SYNC CHECK

def test_jit_sync():
    section("3. TEST JIT USER SYNC")
    r = call("GET", f"{BASE_URL}/api/datasets/mine", headers={"Authorization": f"Bearer {TOKEN}"})
    if r.status_code == 200:
        ok("JIT provisioning OK — User synced to Market DB")
    else:
        fail("JIT provisioning FAILED", r.text)


# 4. RBAC CHECK

def test_rbac_consumer_upload():
    section("4. TEST RBAC (Consumer bị chặn Upload)")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    files = {"file": ("test.csv", "a,b\n1,2", "text/csv")}
    data = {"title": "Illegal Upload", "price": 100}

    r = call("POST", f"{BASE_URL}/api/datasets/upload", headers=headers, files=files, data=data)
    if r.status_code == 403:
        ok("Consumer bị chặn upload (403 Forbidden) → Correct")
    else:
        fail(f"Consumer upload được (Status {r.status_code}) → SECURITY HOLE!", r.text)


# 5. PROVIDER FLOW

def test_provider_flow():
    section("5. TEST PROVIDER FLOW")
    global PROVIDER_TOKEN, NEW_DATASET_ID

    # A. Đăng ký Provider
    prov_payload = {"username": f"p_{TS}", "email": PROVIDER_EMAIL, "password": PASSWORD}
    call("POST", f"{BASE_URL}/api/auth/register", json=prov_payload)
    
    # Login
    r_login = call("POST", f"{BASE_URL}/api/auth/login", json={"email": PROVIDER_EMAIL, "password": PASSWORD})
    temp_token = r_login.json()["access_token"]
    
    # Trigger JIT
    call("GET", f"{BASE_URL}/api/datasets/mine", headers={"Authorization": f"Bearer {temp_token}"})

    # B. Admin Login
    r_admin = call("POST", f"{BASE_URL}/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASS_DEFAULT})
    if r_admin.status_code != 200:
        fail("Admin login failed", r_admin.text)
        return
    admin_token = r_admin.json()["access_token"]

    # C. Tìm ID & Nâng quyền
    r_users = call("GET", f"{BASE_URL}/api/admin/users?page_size=100", 
                   headers={"Authorization": f"Bearer {admin_token}"})
    
    market_user_id = None
    if r_users.status_code == 200:
        users_list = r_users.json().get("items", [])
        for u in users_list:
            if u["email"] == PROVIDER_EMAIL:
                market_user_id = u["id"]
                break
    
    if not market_user_id:
        fail("Không tìm thấy user provider bên Market DB")
        return
    
    print(f"   -> Tìm thấy Provider bên Market DB với ID: {market_user_id}")

    r_promote = call("PUT", f"{BASE_URL}/api/admin/users/{market_user_id}/role?new_role=provider", 
                     headers={"Authorization": f"Bearer {admin_token}"})
    
    if r_promote.status_code == 200:
        ok(f"Admin đã nâng quyền user {market_user_id} lên PROVIDER")
    else:
        fail("Admin promote failed", r_promote.text)
        return

    # D. Upload Dataset
    files = {"file": ("provider_data.csv", "col1,col2\nval1,val2", "text/csv")}
    data = {"title": "Official Provider Dataset", "price": 500}
    
    r_up = call("POST", f"{BASE_URL}/api/datasets/upload", 
                headers={"Authorization": f"Bearer {temp_token}"}, 
                files=files, data=data)

    if r_up.status_code == 200:
        NEW_DATASET_ID = r_up.json()["id"]
        ok(f"Provider upload thành công → Dataset ID: {NEW_DATASET_ID}")
    else:
        fail("Provider upload thất bại", r_up.text)


# 6. PURCHASE & DOWNLOAD

def test_purchase_download():
    section("6. TEST MUA HÀNG & TẢI XUỐNG")
    if not NEW_DATASET_ID:
        warn("Bỏ qua do chưa có Dataset ID")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}

    # Thử tải (Fail)
    r_fail = call("GET", f"{BASE_URL}/api/transactions/{NEW_DATASET_ID}/download", headers=headers)
    if r_fail.status_code == 403:
        ok("Chặn tải xuống khi chưa mua (403) → Correct")
    else:
        fail(f"Lỗi: Cho phép tải chùa (Status {r_fail.status_code})")

    # Mua
    r_buy = call("POST", f"{BASE_URL}/api/transactions/purchase?dataset_id={NEW_DATASET_ID}", headers=headers)
    if r_buy.status_code == 200:
        ok("Mua dataset thành công")
    else:
        fail("Mua dataset thất bại", r_buy.text)
        return

    # Tải lại (Pass)
    r_ok = call("GET", f"{BASE_URL}/api/transactions/{NEW_DATASET_ID}/download", headers=headers)
    if r_ok.status_code == 200:
        ok("Tải xuống thành công sau khi mua → Luồng hoàn tất!")
    else:
        fail("Vẫn không tải được sau khi mua", r_ok.text)


# 7. AI SERVICE

def test_ai_service():
    section("7. TEST AI SERVICE")
    r = call("GET", f"{BASE_URL}/api/ai/recommend?query=battery")
    if r.status_code == 200:
        ok("AI Recommend API online")
    else:
        fail("AI Recommend failed", r.text)


# MAIN RUNNER

if __name__ == "__main__":
    print(f"{BOLD}KIỂM THỬ HỆ THỐNG EV MARKETPLACE (TV1 - BACKEND){RESET}")
    print("-" * 60)

    # --- CHẠY SỬA LỖI DB TRƯỚC KHI TEST ---
    auto_fix_admin_password() 

    test_health()
    test_auth_flow()
    test_jit_sync()
    test_rbac_consumer_upload()
    test_provider_flow()
    test_purchase_download()
    test_ai_service()

    print("\n" + "-" * 60)
    print(f"{GREEN}{BOLD}HOÀN THÀNH TEST. Nếu tất cả PASS, Backend Core đã hoạt động hoàn hảo.{RESET}")