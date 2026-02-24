import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEET_NAME

# Kết nối Google Sheet
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

users_sheet = client.open(SHEET_NAME).worksheet("users")
crops_sheet = client.open(SHEET_NAME).worksheet("crops")


# ================= USER =================

def get_user(user_id):
    data = users_sheet.get_all_records()
    for i, row in enumerate(data):
        if str(row["user_id"]) == str(user_id):
            return row, i + 2
    return None, None


def add_user(user_id, ref_id=None):
    users_sheet.append_row([
        user_id,
        10000,         # vnd
        10,            # energy
        1,             # land
        1,             # level
        0,             # exp
        "Nông dân",    # rank
        ref_id if ref_id else "",
        0              # ref_count
    ])


def add_ref_bonus(ref_id):
    ref_user, row_index = get_user(ref_id)
    if ref_user:
        new_money = int(ref_user["vnd"]) + 3000
        new_ref_count = int(ref_user["ref_count"]) + 1
        users_sheet.update(f"B{row_index}", new_money)
        users_sheet.update(f"I{row_index}", new_ref_count)


# ================= LEVEL & RANK =================

def calculate_level(exp):
    return exp // 5 + 1


def calculate_rank(level):
    if level >= 20:
        return "Tỷ phú nông nghiệp"
    elif level >= 12:
        return "Trang trại vàng"
    elif level >= 8:
        return "Đại điền chủ"
    elif level >= 5:
        return "Chủ trại"
    elif level >= 3:
        return "Thợ trồng"
    else:
        return "Nông dân"


def format_vnd(amount):
    return f"{int(amount):,} VNĐ"