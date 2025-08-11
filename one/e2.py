"""
open_csv_utf8.py

None key가 포함된 dict 구조와, 리스트 값을 가진 None key도 수정/저장 가능한 customtkinter 기반 편집기.
입력 예시:
list_dict = [
    {None: ['いそぐ'], 'k': '急', 'km': '', 'p': 'きゅう', 's': '心 (4획)', 'm': ''},
    ...
]
"""
import csv
import customtkinter as ctk
import tkinter.messagebox
import tkinter as tk
import webbrowser
from get_chrome_path import get_chrome_path
import one


csv_file_path = '心.csv'  # 파일명/경로를 필요에 따라 수정

# None 키를 string으로 변환(내부적으로 'None'으로), 리스트는 '·'로 join
def dict_to_row(row):
    result = {}
    for k, v in row.items():
        key = str(k) if k is not None else 'None'
        if isinstance(v, list):
            value = '·'.join(map(str, v))
        else:
            value = v
        result[key] = value
    return result

# string key, 'None'이면 None, 값이 str에 구분자 있으면 list로 복원
def row_to_dict(row):
    result = {}
    for k, v in row.items():
        key = None if k == 'None' else k
        if key is None and v:  # None key의 값은 list로 변환
            if '·' in v:
                value = v.split('·')
            else:
                value = [v]
        else:
            value = v
        result[key] = value
    return result

# CSV 파일 불러오기
list_dict = []

csv_file_path = '心.csv'  # 파일명/경로를 필요에 따라 수정
list_dict = one.read_and_process_csv(file_path=csv_file_path)


# 필드 이름 처리: None key도 'None'(str)로 포함
if list_dict:
    fieldnames = []
    for k in list_dict[0].keys():
        fieldnames.append(str(k) if k is not None else 'None')
else:
    fieldnames = []

class CsvRowEditorApp(ctk.CTk):
    def __init__(self, data, fieldnames):
        super().__init__()
        self.title("CSV 한 행 집중 수정기 (None key 지원)")
        self.geometry("550x380")
        self.data = data
        self.fieldnames = fieldnames
        self.cur_idx = 0
        self.entries = []

        self.idx_label = ctk.CTkLabel(self, text="")
        self.idx_label.pack(pady=6)

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=16)

        for i, field in enumerate(self.fieldnames):
            row = ctk.CTkFrame(self.form_frame)
            row.pack(fill="x", pady=3)
            label = ctk.CTkLabel(row, text=field, width=120, anchor="w")
            label.pack(side="left")
            entry = ctk.CTkEntry(row, width=320)
            entry.pack(side="left")
            self.entries.append(entry)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        self.prev_btn = ctk.CTkButton(btn_frame, text="이전", width=80, command=self.go_prev)
        self.prev_btn.pack(side="left", padx=6)
        self.save_btn = ctk.CTkButton(btn_frame, text="저장", width=90, fg_color="#008800", command=self.update_row)
        self.save_btn.pack(side="left", padx=6)
        self.next_btn = ctk.CTkButton(btn_frame, text="다음", width=80, command=self.go_next)
        self.next_btn.pack(side="left", padx=6)
        self.save_all_btn = ctk.CTkButton(self, text="CSV 전체 저장", fg_color="#333399", command=self.save_csv)
        self.save_all_btn.pack(pady=6)

        self.show_row()

        self.bind('<Key>', self.key_event)
        self.bind('<Return>', self.enter_event)
        self.focus_set()

    def enter_event(self, event):
        self.update_row()
        self.go_next()

    def key_event(self, event):
        if event.char == '1':
            t_value = self.get_field_value('T')
            url = f"https://ja.dict.naver.com/#/search?query={t_value}"
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(get_chrome_path()))
            webbrowser.get('chrome').open(url)
            print(f"현재 행의 T 값: {t_value}")

    def get_field_value(self, key):
        # 'None'도 지원
        idx = self.fieldnames.index(key) if key in self.fieldnames else -1
        if idx == -1:
            return ""
        return self.entries[idx].get()

    def show_row(self):
        cur_row = dict_to_row(self.data[self.cur_idx])
        for i, field in enumerate(self.fieldnames):
            value = cur_row.get(field, "")
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, value if value is not None else "")
        self.idx_label.configure(text=f"{self.cur_idx+1} / {len(self.data)}행 수정 중")
        self.prev_btn.configure(state="normal" if self.cur_idx > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.cur_idx < len(self.data)-1 else "disabled")

    def update_row(self):
        # Entry 값 -> dict 구조로 변환 (None key와 list값 복원)
        row = {}
        for i, field in enumerate(self.fieldnames):
            key = None if field == 'None' else field
            val = self.entries[i].get()
            if key is None:  # None key 값은 항상 리스트
                if '·' in val:
                    val = val.split('·')
                elif val:
                    val = [val]
                else:
                    val = []
            row[key] = val
        self.data[self.cur_idx] = row
        self.save_csv()

    def go_prev(self):
        self.update_row()
        if self.cur_idx > 0:
            self.cur_idx -= 1
            self.show_row()

    def go_next(self):
        self.update_row()
        if self.cur_idx < len(self.data)-1:
            self.cur_idx += 1
            self.show_row()

    def save_csv(self):
        # None key, list value → string 변환해서 저장
        to_save = [dict_to_row(row) for row in self.data]
        try:
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(to_save)
        except Exception as e:
            tk.messagebox.showerror("저장 실패", str(e))

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")  # 또는 "dark"
    app = CsvRowEditorApp(list_dict, fieldnames)
    app.mainloop()
