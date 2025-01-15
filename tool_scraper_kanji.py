import re
k = [


"強","違","告","乱","内","留","短","睡","会","苦","担","然","素","希","時","肉","礼","要","充","孤","負","金","際","理","日","報","必","資","小","問","普","約","料","週","失","束","語","全","快","方","眠","背","独","労","望","一","論","向","常","的","出","景","適","興","意","期","解","簡","葉","家","通","点","寝","勉","話","味","電","懸","作","生","保","今","単","容","爽","手","本","当","首","突","題","自","間","就","酬","部","広","用","敬","文","鶏","決","持","曜","命","分","炊","疑","現","敵","実","制","副","学","結","言","混","説",


]
l = [

]


def remove_brackets(text):
    # 숫자와 점 다음에 오는 괄호를 처리하는 정규 표현식
    numbered_bracket_pattern = re.compile(r"\d+\.\s*\([^)]+\)")
    
    # 숫자와 점 다음에 오는 괄호를 일시적으로 보호하기 위한 플레이스홀더
    placeholders = {}
    
    # numbered_bracket_pattern에 해당하는 모든 부분을 찾아서 일시적으로 대체
    def protect_numbered_brackets(match):
        placeholder = f"PLACEHOLDER_{len(placeholders)}"
        placeholders[placeholder] = match.group(0)
        return placeholder
    
    # 보호할 괄호 부분 대체
    protected_text = numbered_bracket_pattern.sub(protect_numbered_brackets, text)
    
    # 보호하지 않은 일반 괄호 처리
    def replace(match):
        content = match.group(1)
        if re.fullmatch(r"[\uAC00-\uD7AF]{1,3}", content):
            return f"({content})"
        else:
            return ""

    result = re.sub(r"\(([^)]+)\)", replace, protected_text)
    
    # 보호했던 부분을 원래대로 복구
    for placeholder, original in placeholders.items():
        result = result.replace(placeholder, original)
    
    return result

def find_next_sentence(text, keyword, number=1):
    # 텍스트를 줄바꿈으로 분리하여 문장 리스트 생성
    sentences = text.split('\n')
    # 키워드가 포함된 문장을 찾고 다음 문장을 반환
    for i in range(len(sentences) - 1):
        if keyword in sentences[i]:
            return sentences[i + number]  # 다음 문장 반환
    return "키워드를 포함하는 문장이 없습니다."

 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


for kan in k :
    driver = webdriver.Chrome()  # ChromeDriver 필요
    driver.get(f"https://ja.dict.naver.com/#/search?query={kan}&range=all")
    time.sleep(15)  # 페이지 로드 대기


    if len(kan) > 1 : 
        
        # 원하는 데이터 추출
        elements = driver.find_elements(By.CLASS_NAME, "has-saving-function")
        
        t = remove_brackets(elements[0].text)
        #한자, 발음, 뜻,
        end_keyword = "민중서림 엣센스 일한사전"
        t = t.split(end_keyword)[0]

        t_splited = t.split("\n")
        발음 = t_splited[0].split("[")[0].strip()
        
        
        뜻 = ""
        품사 = find_next_sentence(t, '단어장에 저장')
        뜻_부분 = find_next_sentence(t, '단어장에 저장', number=2)
        pattern = r'^\d+\.'
        print("*"*88)
        if re.match(pattern, 뜻_부분):
            뜻_부분 = ""
            #뜻이 여러개
            
            뜻_시작_줄 = 0 
            for i in range(len(t_splited) - 1):
                if '단어장에 저장' in t_splited[i]:
                    i = i + 1
                    break


            뜻 += f"[{t_splited[i]}] "#품사
            while True :
                i += 1
                if len(t_splited)-1 <= i   : break # -1 은 문단 뒤에 있는 '민중서림 엣센스 일한사전' 부분을 없애기 위해서이다.
                if re.match(pattern, t_splited[i]) : #숫자가 맞는지
                    뜻 += f"{t_splited[i]}".strip() # 숫자
                    i += 1
                    뜻 += f"{t_splited[i]}".strip().replace(".","")+" " # 의미
                else :
                    padding = ""
                    if not 뜻[-1] == " " :
                        padding = " "
                    #품사가 있다는 의미
                    뜻 += f"{padding}/ [{t_splited[i]}] "#품사
                    
                    continue #품사 기록하고 처음으로 돌아가기
                    
        else:
            #뜻이 한개
            뜻 = f"[{품사}] {뜻_부분}"

        print("발음 :",발음)
        print("뜻 :",뜻)
        t = {
            "kan":kan,
            "sound":발음,
            "mean":뜻.strip()
            }
        print("ghdwpaks"*3,t)
        l.append(t)


    
    else : 



        # 원하는 데이터 추출
        elements = driver.find_elements(By.CLASS_NAME, "addition_info")  # 클래스 이름을 변경해야 할 수 있음
        for element in elements:
            print("len(kan) :",len(kan))

            #단일글자라면
            t = {"k":kan,"s":"","m":"","p":""}

            # 줄 단위로 텍스트를 분리
            lines = element.text.strip().split("\n")

            # "음독"과 "훈독" 다음 줄의 내용을 추출하여 t 변수에 추가
            for i, line in enumerate(lines):
                if line == "음독" and i + 1 < len(lines):
                    t["s"] += lines[i + 1]  # 음독 다음 줄을 "s"에 추가
                elif line == "훈독" and i + 1 < len(lines):
                    t["m"] += lines[i + 1]  # 훈독 다음 줄을 "m"에 추가
                elif line == "부수" and i + 1 < len(lines):
                    t["p"] += lines[i + 1]  # 훈독 다음 줄을 "m"에 추가
            print(t)
            l.append(t)

    driver.quit()

print(l)










'''


{'k': '味', 's': 'み', 'm': 'あじ·あじわう', 'p': '口 (3획)'}

DevTools listening on ws://127.0.0.1:50692/devtools/browser/b5d6889c-a955-470f-90df-cf736a70b2c8
[123772:59176:0113/021040.959:ERROR:device_event_log_impl.cc(201)] [02:10:40.959] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '構', 's': 'こう', 'm': 'かまう·かまえる', 'p': '木 (4획)'}

DevTools listening on ws://127.0.0.1:50759/devtools/browser/84e56b72-46e3-403c-b16a-7f5c92493312
[42984:124184:0113/021104.055:ERROR:device_event_log_impl.cc(201)] [02:11:04.056] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '難', 's': 'なん', 'm': 'むずかしい·かたい', 'p': '隹 (8획)'}

DevTools listening on ws://127.0.0.1:50796/devtools/browser/2e10aa9a-6406-4d58-8d10-6ef3635b5d88
[42012:46784:0113/021129.136:ERROR:device_event_log_impl.cc(201)] [02:11:29.136] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '姿', 's': 'し', 'm': 'すがた', 'p': '女 (3획)'}

DevTools listening on ws://127.0.0.1:50835/devtools/browser/95f1c533-2432-4536-839c-bf9ac5de670f
[36052:44340:0113/021153.758:ERROR:device_event_log_impl.cc(201)] [02:11:53.758] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '恋', 's': 'れん', 'm': 'こい·こいしい·こう', 'p': '心 (4획)'}

DevTools listening on ws://127.0.0.1:50890/devtools/browser/778b32cf-537e-45a8-b0a9-003333428f37
[77012:77212:0113/021217.747:ERROR:device_event_log_impl.cc(201)] [02:12:17.747] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '親', 's': 'しん', 'm': 'おや·したしい·したしむ', 'p': '見 (7획)'}

DevTools listening on ws://127.0.0.1:50924/devtools/browser/f7690544-67d8-4be8-999b-9f5e44d387fa
[59716:69628:0113/021240.615:ERROR:device_event_log_impl.cc(201)] [02:12:40.615] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '家', 's': 'か·け', 'm': 'いえ·や', 'p': '宀 (3획)'}

DevTools listening on ws://127.0.0.1:50952/devtools/browser/1b33e06e-6d62-46af-8511-0a18ec7b9130
[101380:101544:0113/021305.362:ERROR:device_event_log_impl.cc(201)] [02:13:05.362] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: ?붿냼媛 ?놁뒿?덈떎. (0x490)
0)
Created TensorFlow Lite XNNPACK delegate for CPU.
len(kan) : 1
{'k': '安', 's': 'あん', 'm': 'やすい', 'p': '宀 (3획)'}


'''

