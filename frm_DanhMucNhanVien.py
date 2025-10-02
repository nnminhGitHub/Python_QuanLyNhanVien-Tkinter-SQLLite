# Python version 3.12
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# ===== Hàm canh giữa cửa sổ =====
def center_window(win, w=630, h=480):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ===== CỬA SỔ CHÍNH =====
root = tk.Tk()
root.title("Quản lý nhân viên")
center_window(root, 720, 480)
root.resizable(False, False)

# ===== TIÊU ĐỀ =====
lbl_title = tk.Label(root, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)

# ===== FRAME THÔNG TIN =====
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")

# Mã số
tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=10)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Chức vụ
tk.Label(frame_info, text="Chức vụ").grid(row=0, column=2, padx=5, pady=5, sticky="w")
cbb_chucvu = ttk.Combobox(frame_info, values=[
    "Trưởng phòng", "Nhân viên chuyên trách", "Phó trưởng phòng", "Kế toán", "Lái xe cơ quan"
], width=20)
cbb_chucvu.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Họ tên
tk.Label(frame_info, text="Họ tên").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_hoten = tk.Entry(frame_info, width=25)
entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Tên
tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_ten = tk.Entry(frame_info, width=15)
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")

# Giới tính
tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")

# Ngày sinh
tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, sticky="w")
date_entry = DateEntry(frame_info, width=12, background='darkblue', foreground='white', date_pattern='mm/dd/yy')
date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

# ===== DANH SÁCH NHÂN VIÊN =====
lbl_ds = tk.Label(root, text="Danh sách nhân viên", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

# Cấu hình tiêu đề cột
tree.heading("maso", text="Mã số")
tree.heading("holot", text="Họ và lót")
tree.heading("ten", text="Tên")
tree.heading("phai", text="Phái")
tree.heading("ngaysinh", text="Ngày sinh")
tree.heading("chucvu", text="Chức vụ")

# Cấu hình độ rộng cột
tree.column("maso", width=60, anchor="center")
tree.column("holot", width=150)
tree.column("ten", width=80)
tree.column("phai", width=60, anchor="center")
tree.column("ngaysinh", width=100, anchor="center")
tree.column("chucvu", width=150)

tree.pack(padx=10, pady=5, fill="both")

# ======= HÀM CHỨC NĂNG CRUD =======
def clear_input():
    """Xóa sạch dữ liệu nhập"""
    entry_maso.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.set_date("01/01/2000")
    cbb_chucvu.set("")

def them_nv():
    """Thêm nhân viên mới vào bảng"""
    maso = entry_maso.get()
    holot = entry_hoten.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    chucvu = cbb_chucvu.get()

    if maso == "" or holot == "" or ten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return

    tree.insert("", tk.END, values=(maso, holot, ten, phai, ngaysinh, chucvu))
    clear_input()

def xoa_nv():
    """Xóa nhân viên được chọn trong bảng"""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Hãy chọn một nhân viên để xóa!")
        return
    tree.delete(selected_item)

def sua_nv():
    """Tải dữ liệu từ bảng vào form để sửa"""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Hãy chọn một nhân viên để sửa!")
        return
    
    values = tree.item(selected_item)["values"]

    # Gán giá trị từ bảng vào form nhập
    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, values[0])

    entry_hoten.delete(0, tk.END)
    entry_hoten.insert(0, values[1])

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[2])

    gender_var.set(values[3])
    date_entry.set_date(values[4])
    cbb_chucvu.set(values[5])

def luu_nv():
    """Lưu thay đổi sau khi sửa"""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Hãy chọn một nhân viên để lưu!")
        return

    maso = entry_maso.get()
    holot = entry_hoten.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    chucvu = cbb_chucvu.get()

    tree.item(selected_item, values=(maso, holot, ten, phai, ngaysinh, chucvu))
    clear_input()

# ===== FRAME BUTTON =====
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

btn_them = tk.Button(frame_btn, text="Thêm", width=8, command=them_nv)
btn_them.grid(row=0, column=0, padx=5)

btn_luu = tk.Button(frame_btn, text="Lưu", width=8, command=luu_nv)
btn_luu.grid(row=0, column=1, padx=5)

btn_sua = tk.Button(frame_btn, text="Sửa", width=8, command=sua_nv)
btn_sua.grid(row=0, column=2, padx=5)

btn_huy = tk.Button(frame_btn, text="Hủy", width=8, command=clear_input)
btn_huy.grid(row=0, column=3, padx=5)

btn_xoa = tk.Button(frame_btn, text="Xóa", width=8, command=xoa_nv)
btn_xoa.grid(row=0, column=4, padx=5)

btn_thoat = tk.Button(frame_btn, text="Thoát", width=8, command=root.quit)
btn_thoat.grid(row=0, column=5, padx=5)

# ===== Thêm dữ liệu mẫu ban đầu =====
'''
sample_data = [
    ("NV001", "Nguyễn Phước Minh", "Tân", "Nam", "04/19/75", "Trưởng phòng"),
    ("NV004", "Lý Văn", "Sang", "Nam", "12/21/70", "Nhân viên chuyên trách"),
    ("NV005", "Nguyễn Thị Thu", "An", "Nữ", "08/22/81", "Phó trưởng phòng"),
    ("NV006", "Nguyễn Thanh", "Tùng", "Nam", "07/07/77", "Lái xe cơ quan"),
    ("NV007", "Trần Văn", "An", "Nam", "04/08/79", "Nhân viên chuyên trách"),
    ("NV008", "Cao Thị Ngọc", "Nhung", "Nữ", "06/18/80", "Kế toán"),
    ("NV009", "Lê Thành", "Tuyên", "Nam", "08/25/84", "Nhân viên chuyên trách"),
    ("NV010", "Phan Thị Thúy", "Tiên", "Nữ", "10/25/87", "Kế toán"),
]
for row in sample_data:
    tree.insert("", tk.END, values=row)
'''

# ===== MAIN LOOP =====
root.mainloop()

'''
them_nv():       Lấy dữ liệu từ form nhập → chèn vào Treeview.
sua_nv():        Lấy dòng đang chọn trong bảng → đưa dữ liệu ngược lên form để sửa.
luu_nv():        Sau khi sửa dữ liệu trên form → ghi đè vào dòng đã chọn trong bảng.
xoa_nv():        Xóa dòng được chọn trong bảng.
clear_input():   Dọn sạch form nhập để sẵn sàng nhập mới.
'''