from pathlib import Path

folder_name = "PDF파일"
prefix = "계약서"

desktop = Path.home() / "Desktop"
target_folder = desktop / folder_name

pdf_files = sorted(target_folder.glob("*.pdf"))

if not pdf_files:
    print("PDF 파일이 없습니다.")
    exit()

for index, file in enumerate(pdf_files, start=1):
    new_name = f"{prefix}_{index:03d}.pdf"
    new_path = target_folder / new_name

    file.rename(new_path)
    print(f"{file.name} → {new_name}")

print("완료")
