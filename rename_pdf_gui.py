import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def rename_pdfs():
    folder = filedialog.askdirectory(title="PDF 폴더 선택")
    if not folder:
        return

    prefix = entry_prefix.get().strip()
    if not prefix:
        messagebox.showerror("오류", "파일 이름을 입력하세요")
        return

    start_num = entry_start.get().strip()
    if not start_num.isdigit():
        messagebox.showerror("오류", "시작 번호는 숫자여야 합니다")
        return

    start_num = int(start_num)

    target_folder = Path(folder)
    pdf_files = sorted(target_folder.glob("*.pdf"))

    if not pdf_files:
        messagebox.showwarning("알림", "PDF 파일이 없습니다")
        return

    for index, file in enumerate(pdf_files, start=start_num):
        new_name = f"{prefix}_{index:03d}.pdf"
        new_path = target_folder / new_name
        file.rename(new_path)

    messagebox.showinfo("완료", "이름 변경 완료")

root = tk.Tk()
root.title("PDF 이름 변경 프로그램")
root.geometry("400x220")

tk.Label(root, text="파일명 입력").pack(pady=5)
entry_prefix = tk.Entry(root)
entry_prefix.insert(0, "계약서")
entry_prefix.pack()

tk.Label(root, text="시작 번호").pack(pady=5)
entry_start = tk.Entry(root)
entry_start.insert(0, "1")
entry_start.pack()

tk.Button(root, text="폴더 선택 후 실행", command=rename_pdfs).pack(pady=20)

root.mainloop()
