import random
import threading
import sys
s = [
['あ', '아'],['い', '이'],
['う', '우'],['え', '에'],
['お', '오'],['か', '카'],
['き', '키'],['く', '쿠'],
['け', '케'],['こ', '코'],
['さ', '사'],['し', '시'],
['す', '스'],['せ', '세'],
['そ', '소'],['た', '타'],
['ち', '치'],['つ', '츠'],
['て', '테'],['と', '토'],
['な', '나'],['に', '니'],
['ぬ', '누'],['ね', '네'],
['の', '노'],['は', '하'],
['ひ', '히'],['ふ', '후'],
['へ', '헤'],['ほ', '호'],
['ま', '마'],['み', '미'],
['む', '무'],['め', '메'],
['も', '모'],['や', '야'],
['ゆ', '유'],['よ', '요'],
['ら', '라'],['り', '리'],
['る', '루'],['れ', '레'],
['ろ', '로'],['わ', '와'],
['を', '오'],['ん', '은'],
]


s2 = [
    ['ほ', '호'],
    ['は', '하'],
    ['ぬ', '누'],
    ['へ', '헤'],
    ['ろ', '로'],
    ['ふ', '후'],
    ['き', '키'],
    ['や', '야'],
    ['れ', '레'],
    ['ち', '치'],
    ['お', '오'],
    ['に', '니'],
    ['め', '메'],
    ['ら', '라'],
]

s3 = [
    ["いぬ", "이누"],
    ["えび", "에비"],
    ["かさ", "카사"],
    ["くま", "쿠마"],
    ["こえ", "코에"],
    ["しお", "시오"],
    ["せみ", "세미"],
    ["たに", "타니"],
    ["つき", "츠키"],
    ["とり", "토리"],
    ["にわ", "니와"],
    ["ねこ", "네코"],
    ["はな", "하나"],
    ["ふね", "후네"],
    ["ほし", "호시"],
    ["みみ", "미미"],
    ["めだか", "메다카"],
    ["やま", "야마"],
    ["よる", "요루"],
    ["りんご", "린고"],
    ["れんげ", "렌게"],
    ["わたし", "와타시"],
    ["ごはん", "고한"],
    ["あめ", "아메"],
    ["うみ", "우미"],
    ["おと", "오토"],
    ["きつね", "키츠네"],
    ["けむし", "케무시"],
    ["さくら", "사쿠라"],
    ["すし", "스시"],
    ["そら", "소라"],
    ["ちず", "치즈"],
    ["てがみ", "테가미"],
    ["なつ", "나츠"],
    ["ぬの", "누노"],
    ["のり", "노리"],
    ["ひかり", "히카리"],
    ["へび", "헤비"],
    ["まど", "마도"],
    ["むし", "무시"],
    ["もり", "모리"],
    ["ゆき", "유키"],
    ["らいおん", "라이온"],
    ["るす", "루스"],
    ["ろく", "로쿠"],
    ["をかし", "오카시"],
]

s = s
'''
['ほ', '호', 10]
['ろ', '로', 9]
['ぬ', '누', 9]
['ま', '마', 6]
'''


def get_input():
    try:
        return input()
    except EOFError:
        return None

def timeout_input(timeout=2):
    user_input = [None]
    
    def get_user_input():
        user_input[0] = get_input()

    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()
    input_thread.join(timeout)  # 주어진 시간 동안 입력 대기
    
    if input_thread.is_alive():
        input_thread.join()  # 스레드 종료
        return None
    else:
        return user_input[0]

# 타임어택 모드 활성화 여부를 묻는 코드
print("타임어택 모드를 활성화하시겠습니까? (y/n): ", end="")
time_attack = get_input() == 'y'

random.shuffle(s)
sc = [0] * len(s)

while True:
    for i, question in enumerate(s):  # 인덱스 추적을 위해 enumerate 사용
        japanese, korean = question
        print(f"{japanese}: ", end="")
        if time_attack:
            user_input = timeout_input(2)
        else:
            user_input = get_input()

        if user_input == "exit":
            for j in range(len(s)):
                s[j].append(sc[j])
            sorted_s = sorted(s, key=lambda x: x[2], reverse=True)
            for item in sorted_s:
                print(item)
            sys.exit()  # 프로그램 종료

        elif user_input == korean:
            print("")
        elif user_input is None:  # 시간 초과
            print(f"{korean}\n")
            sc[i] += 1  # 이제 i는 올바르게 추적됨
        else:
            print(f"{korean}\n")
            sc[i] += 1  # 마찬가지로 틀린 경우도 i를 사용하여 인덱스 추적