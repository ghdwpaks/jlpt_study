import gspread

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "C:\\Users\\hjm79\\OneDrive\\문서\\카카오톡 받은 파일\\serious-octagon-413001-654e6c5552b0.json"
print("p1")
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/11tcTwdA8kIISyboJwElD3TNDfZAolcyA9K7RzdJw944/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("sheet1")
#gspread.service_account.open_by_url(spreadsheet_url).worksheet("sheet1")

print("ghdwpaks")
worksheet.update_cell(1,5,"test")
#세로줄 #가로줄
