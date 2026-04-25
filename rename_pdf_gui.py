import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import re

selected_folder = None
pdf_files = []

def natural_sort_key(path):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', path.name)
    ]

def choose_folder():
    global selected_folder, pdf_files

    folder = filedialog.askdirectory(title="PDF 폴더 선택")
    if not folder:
        return

    selected_folder = Path(folder)
    pdf_files = sorted(selected_folder.glob("*.pdf"), key=natural_sort_key)

    list_original.delete(0, tk.END)
    list_new.delete(0, tk.END)

    if not pdf_files:
        messagebox.showwarning("알림", "선택한 폴더에 PDF 파일이 없습니다.")
        return

    for file in pdf_files:
        list_original.insert(tk.END, file.name)

    make_preview()

def make_preview():
    list_new.delete(0, tk.END)

    if not pdf_files:
        return

    pattern = entry_pattern.get().strip()
    start_text = entry_start.get().strip()

    if not pattern:
        messagebox.showerror("오류", "변경할 이름 형식을 입력하세요.")
        return

    if not start_text.isdigit():
        messagebox.showerror("오류", "시작 번호는 숫자로 입력하세요.")
        return

    start_num = int(start_text)

    for index, file in enumerate(pdf_files, start=start_num):
        new_name = pattern.replace("{번호}", f"{index:03d}")

        if not new_name.lower().endswith(".pdf"):
            new_name += ".pdf"

        list_new.insert(tk.END, new_name)

def rename_files():
    if not selected_folder or not pdf_files:
        messagebox.showerror("오류", "먼저 PDF 폴더를 선택하세요.")
        return

    if list_new.size() == 0:
        messagebox.showerror("오류", "먼저 미리보기를 생성하세요.")
        return

    if not messagebox.askyesno("확인", "정말 파일 이름을 변경하시겠습니까?"):
        return

    try:
        for i, file in enumerate(pdf_files):
            new_name = list_new.get(i)
            new_path = selected_folder / new_name

            if new_path.exists():
                messagebox.showerror("오류", f"이미 존재하는 파일명입니다:\n{new_name}")
                return

            file.rename(new_path)

        messagebox.showinfo("완료", "PDF 파일 이름 변경이 완료되었습니다.")
        choose_folder()

    except Exception as e:
        messagebox.showerror("오류", str(e))


root = tk.Tk()
root.title("PDF 이름 일괄 변경 프로그램")
root.geometry("900x600")

top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=15, pady=10)

tk.Label(top_frame, text="변경 이름 형식").grid(row=0, column=0, padx=5)
entry_pattern = tk.Entry(top_frame, width=40)
entry_pattern.insert(0, "계약서_{번호}")
entry_pattern.grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="시작 번호").grid(row=0, column=2, padx=5)
entry_start = tk.Entry(top_frame, width=10)
entry_start.insert(0, "1")
entry_start.grid(row=0, column=3, padx=5)

tk.Button(top_frame, text="미리보기 생성", command=make_preview).grid(row=0, column=4, padx=5)

middle_frame = tk.Frame(root)
middle_frame.pack(fill="both", expand=True, padx=15, pady=10)

left_frame = tk.Frame(middle_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=5)

right_frame = tk.Frame(middle_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=5)

tk.Label(left_frame, text="현재 PDF 파일명").pack()
list_original = tk.Listbox(left_frame, width=50, height=25)
list_original.pack(fill="both", expand=True)

tk.Label(right_frame, text="변경될 PDF 파일명").pack()
list_new = tk.Listbox(right_frame, width=50, height=25)
list_new.pack(fill="both", expand=True)

bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=15, pady=10)

tk.Button(bottom_frame, text="PDF 폴더 선택", command=choose_folder, width=20).pack(side="left", padx=5)
tk.Button(bottom_frame, text="이름 변경 실행", command=rename_files, width=20).pack(side="right", padx=5)

root.mainloop()
