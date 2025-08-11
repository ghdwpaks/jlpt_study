"""
open_csv_utf8.py

CSV 파일을 utf-8 인코딩으로 열고, 각 행을 딕셔너리(dict) 형태로 변환해 리스트(list_dict)에 저장하는 코드입니다.
customtkinter로 한 번에 한 행만 집중적으로 수정하고, '이전'/'다음' 버튼으로 행을 이동하며 수정할 수 있도록 한 GUI 버전입니다.
'1' 키를 누르면 현재 보고 있는 행의 'T' 컬럼 값을 print 하고, 네이버 일본어사전에서 검색합니다.
Enter(엔터) 키를 누르면 어디에 포커스가 있든 바로 다음 행으로 이동(go_next)하고, 그 직전에 현재 행이 csv 파일에 즉시 저장됩니다.
"""
import csv
import customtkinter as ctk
import tkinter.messagebox
import tkinter as tk
import webbrowser
from get_chrome_path import get_chrome_path
from one import FlashcardApp as capp
import one


csv_file_path = '心.csv'  # 파일명/경로를 필요에 따라 수정
list_dict = one.read_and_process_csv(file_path=csv_file_path)

# 필드 이름 가져오기
if list_dict:
    fieldnames = list(list_dict[0].keys())
else:
    fieldnames = []

# customtkinter GUI (한 행 집중 + 이전/다음)
class CsvRowEditorApp(ctk.CTk):

    p_label = "" #부수 및 획수
    s_label = "" #음독
    km_label = "" #훈독
    m_label = "" #한국어 뜻
    word_label = "" #한자

    def __init__(self, data, fieldnames):
        super().__init__()
        self.title("CSV 한 행 집중 수정기")
        self.geometry("500x350")
        self.data = data
        self.fieldnames = fieldnames
        self.cur_idx = 0
        self.entries = []

        # 행 번호 표시
        self.idx_label = ctk.CTkLabel(self, text="")
        self.idx_label.pack(pady=6)

        # Entry 영역
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=16)

        for i, field in enumerate(self.fieldnames):
            row = ctk.CTkFrame(self.form_frame)
            row.pack(fill="x", pady=3)
            label = ctk.CTkLabel(row, text=field, width=120, anchor="w")
            label.pack(side="left")
            entry = ctk.CTkEntry(row, width=260)
            entry.pack(side="left")
            self.entries.append(entry)

        # 이동 및 저장 버튼
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        self.prev_btn = ctk.CTkButton(btn_frame, text="이전", width=80, command=self.go_prev)
        self.prev_btn.pack(side="left", padx=6)
        self.save_btn = ctk.CTkButton(btn_frame, text="저장", width=90, fg_color="#008800", command=self.update_row)
        self.save_btn.pack(side="left", padx=6)
        self.next_btn = ctk.CTkButton(btn_frame, text="다음", width=80, command=self.go_next)
        self.next_btn.pack(side="left", padx=6)

        # 전체 저장 버튼
        self.save_all_btn = ctk.CTkButton(self, text="CSV 전체 저장", fg_color="#333399", command=self.save_csv)
        self.save_all_btn.pack(pady=6)

        self.show_row()

        # 키 바인딩: 1 누르면 T 컬럼 print 및 네이버 사전 검색
        self.bind('<Key>', self.key_event)
        self.bind('<Return>', self.enter_event)  # 어디서든 Enter 누르면 go_next

        self.bind("1", lambda event: capp.search(self=self,target=1))
        self.bind("2", lambda event: capp.search(self=self,target=2))
        self.bind("3", lambda event: capp.search(self=self,target=3, event=event))
        self.bind("4", lambda event: capp.search(self=self,target=4))
        self.bind("q", lambda event: capp.search(self=self,target=11));self.bind("Q", lambda event: capp.search(self=self,target=11))
        self.bind("e", lambda event: capp.search(self=self,target=12));self.bind("E", lambda event: capp.search(self=self,target=12))
        self.bind(";", lambda event: capp.search(self=self,target=13))


        self.focus_set()

    def enter_event(self, event):
        # 어디서든 엔터 누르면 현재 행 저장 후 go_next
        self.update_row()
        self.go_next()

    def key_event(self, event):
        if event.char == '1':
            t_value = self.data[self.cur_idx].get('T', None)
            url = f"https://ja.dict.naver.com/#/search?query={t_value}"
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(get_chrome_path()))
            webbrowser.get('chrome').open(url)

    def show_row(self):

        # 현재 인덱스 행 Entry에 표시
        for i, field in enumerate(self.fieldnames):
            value = self.data[self.cur_idx][field]
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, value if value is not None else "")
        self.idx_label.configure(text=f"{self.cur_idx+1} / {len(self.data)}행 수정 중")
        self.prev_btn.configure(state="normal" if self.cur_idx > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.cur_idx < len(self.data)-1 else "disabled")
        
        #value = self.data[self.cur_idx][field]
        
        data = self.data[self.cur_idx]
        self.p_label = data['p'] #부수_및_획수
        self.s_label = data['s'] #음독
        self.m_label = data['m'] #훈독
        self.km_label = data['km'] #한국어_뜻
        self.word_label = data['k']



    def update_row(self):
        # Entry 값으로 현재 행 갱신 + csv 파일 내용 즉시 변경
        for i, field in enumerate(self.fieldnames):
            self.data[self.cur_idx][field] = self.entries[i].get()
        self.save_csv()
        #tk.messagebox.showinfo("저장", f"{self.cur_idx+1}번째 행이 저장되었습니다.")

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
        try:
            # 헤더와 변환 데이터 준비
            header = ['T', 'D', 'P', 'E']
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:

                header = ['T', 'D', 'P', 'E']
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                for data in self.data:
                    row = {
                        'T': data['k'],
                        'D': data['km'],
                        'P': f"{data['s']}/{data['m']}",
                        'E': data['p']
                    }
                    writer.writerow(row)


                #writer.writeheader()
                #writer.writerows(self.data)
            #tk.messagebox.showinfo("저장 완료", "CSV 파일이 저장되었습니다.")
        except Exception as e:
            tk.messagebox.showerror("저장 실패", str(e))

if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # 또는 "dark"
    app = CsvRowEditorApp(list_dict, fieldnames)
    app.mainloop()
