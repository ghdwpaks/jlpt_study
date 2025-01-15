
from getpass import getpass 
import getpass
import sys
import re
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'

def hide_cursor():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()

def g(prompt=''):
    try:
        # Hide the cursor
        hide_cursor()
        # Use getpass to get the input without echoing
        password = getpass.getpass(prompt)
    finally:
        # Ensure the cursor is shown again
        show_cursor()
    return password

hanta_to_hangul_map = {
    'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
    'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ',
    'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ', 'ho': 'ㅙ',
    'hl': 'ㅚ', 'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ',
    'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ', 'fg': 'ㅀ',
    'qt': 'ㅄ'
}
def hanta_to_hangul(eng):
    return hanta_to_hangul_map.get(eng, '')

def convert_hanta_to_hangul(input_string):
    # 두 글자씩 처리하는데, 만약 마지막 글자가 하나 남으면 단독으로 처리
    result = []
    i = 0
    while i < len(input_string):
        if i + 1 < len(input_string):
            combined = input_string[i] + input_string[i + 1]
            if combined in hanta_to_hangul_map:
                result.append(hanta_to_hangul(combined))
                i += 2
                continue
        result.append(hanta_to_hangul(input_string[i]))
        i += 1
    
    return normalize_hangul(''.join(result))

def compose_hangul(jamos):
    # 한글 자모 테이블 정의
    initial_consonants = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    medial_vowels = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
    final_consonants = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

    # 초성, 중성, 종성 인덱스 가져오기
    initial_index = initial_consonants.index(jamos[0])
    medial_index = medial_vowels.index(jamos[1])
    final_index = 0 if len(jamos) < 3 else final_consonants.index(jamos[2])

    # 유니코드 조합
    syllable_code = 0xAC00 + (initial_index * 21 * 28) + (medial_index * 28) + final_index
    return chr(syllable_code)

def normalize_hangul(jamo_string):
    jamo_string = list(jamo_string)
    result = []

    i = 0
    while i < len(jamo_string):
        if jamo_string[i] in "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" and i + 1 < len(jamo_string):
            if jamo_string[i + 1] in "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ":
                if i + 2 < len(jamo_string) and jamo_string[i + 2] in "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ":
                    result.append(compose_hangul(jamo_string[i:i + 3]))
                    i += 3
                else:
                    result.append(compose_hangul(jamo_string[i:i + 2]))
                    i += 2
            else:
                result.append(jamo_string[i])
                i += 1
        else:
            result.append(jamo_string[i])
            i += 1

    return ''.join(result)

s1 = [
["ア","아"],["イ","이"],["ウ","우"],["エ","에"],
["オ","오"],["カ","카"],["キ","키"],["ク","쿠"],
["ケ","케"],["コ","코"],["サ","사"],["シ","시"]
]
s2 = [
["ス","스"],["セ","세"],["ソ","소"],["タ","타"],
["チ","치"],["ツ","츠"],["テ","테"],["ト","토"],
["ナ","나"],["ニ","니"],["ヌ","누"],["ネ","네"],
]
s3 = [
["ノ","노"],["ハ","하"],["ヒ","히"],["フ","후"],
["ヘ","헤"],["ホ","호"],["マ","마"],["ミ","미"],
["ム","무"],["メ","메"],["モ","모"],["ヤ","야"],
]
s4 = [
["ユ","유"],["ヨ","요"],["ラ","라"],["リ","리"],
["ル","루"],["レ","레"],["ロ","로"],["ワ","와"],
["ヲ","오"],["ン","은"],["キャ","캬"],["キュ","큐"],
]
s5 = [
["キョ","쿄"],["シャ","샤"],["シュ","슈"],["ショ","쇼"],
["チャ","챠"],["チュ","츄"],["チョ","쵸"],["ニャ","냐"],
["ニュ","뉴"],["ニョ","뇨"],["ヒャ","햐"],["ヒュ","휴"],
]
s6 = [
["ヒョ","효"],["ミャ","먀"],["ミュ","뮤"],["ミョ","묘"],
["リャ","랴"],["リュ","류"],["リョ","료"],["ギャ","갸"],
["ギュ","규"],["ギョ","교"],["ジャ","자"],["ジュ","주"],
]
s7 = [
["ジョ","조"],["ビャ","뱌"],["ビュ","뷰"],["ビョ","뵤"],
["ピャ","피야"],["ピュ","퓨"],["ピョ","표"],["ィ","이"],
["ガ","가"],["ギ","기"],["グ","구"],["ゲ","게"],
]
s8 = [
["ゴ","고"],["ザ","자"],["ジ","지"],["ズ","즈"],
["ゼ","제"],["ゾ","조"],["ダ","다"],["ヂ","지"],
["ヅ","즈"],["デ","데"],["ド","도"],["バ","바"],
]
s9 = [
["ビ","비"],["ブ","부"],["ベ","베"],["ボ","보"],
["パ","파"],["ピ","피"],["プ","푸"],["ペ","페"],
["ポ","포"],
]

out = [
    ["ク","쿠"],["オ","오"],["ケ","케"],["サ","사"],["シ","시"],
    ["タ","타"],["チ","치"],["ヌ","누"],["ツ","츠"],['マ', '마'],
    ['ホ', '호'],['ヒ', '히'],['ノ', '노'],['フ', '후']

]
if __name__ == "__main__":

    # 숫자 구분하는 코드
    def extract_numbers(text):
        match = re.match(r'^out(\d+)$', text)
        if match:
            number_string = match.group(1)
            return [int(char) for char in number_string]
        return []

    sector_number = input("sector(1~9):")
    s = None
    if sector_number in ["1","2","3","4","5","6","7","8","9"] :
        s=eval(f's{sector_number}')

    elif sector_number == "out" :
        s=eval(f'out')

    elif bool(re.match(r'^out\d+$', sector_number)) :
        s = []
        sectors = []
        for i in extract_numbers(sector_number) :
            if i in [1,2,3,4,5,6,7,8,9] :
                eval(f'sectors.extend(s{i})')
        sectors_keys = [k for k, v in sectors]
        out_keys = [k for k, v in out]
        for out_word in out:
            for sector in sectors:
                if sector[0] == out_word[0]:
                    s.append(out_word)

    elif len(sector_number) > 1 :
        s = [] 
        sector_numbers = list(sector_number)
        for sector_number in sector_numbers :
            s.extend(eval(f's{sector_number}'))
            
    sc = [0]*len(s)
    if len(sc) > 0 : 
        while True:
            random.shuffle(s)
            for question in s:
                japanese, korean = question
                user_input = g(f"{japanese} ").strip()
                if user_input == "exit" :
                    for i in range(len(s)):
                        s[i].append(sc[i])
                    sorted_s = sorted(s, key=lambda x: x[2], reverse=True)
                    for i in sorted_s : print(i)
                    exit()
                elif user_input == korean or convert_hanta_to_hangul(user_input) == korean:
                    print("")
                    pass
                else:
                    for i, row in enumerate(s):
                        if korean == row[1]:
                            sc[i] += 1
                            break

                    print(f"{korean}\n")  







































