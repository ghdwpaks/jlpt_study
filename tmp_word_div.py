import re
t1 = """めいじん [名人]
듣기
JLPT 3
어휘등급
めいじん 단어장에 저장
명사
1.
명인.
2.
그 분야에서 솜씨가 뛰어난 사람. (=達人, 名手)
3.
바둑이나 장기에서, 최고위(位)의 칭호의 하나.
민중서림 엣센스 일한사전"""


t2 = """ひとり [一人·独り]
듣기
JLPT 5
어휘등급
ひとり 단어장에 저장
명사
1.
한 사람, 한 명. (=いちにん)
2.
혼자, 단 한 사람.
부사
1.
(뒤에 부정(否定)의 말이 와서) 비단, 단지, 다만, 단순히.
2.
홀로, 혼자(서).
민중서림 엣센스 일한사전"""

t3 = """こうかい [後悔]
듣기
JLPT 1
어휘등급
こうかい 단어장에 저장
명사, ス자동사·타동사
후회, 뉘우침.
민중서림 엣센스 일한사전"""



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

#명사,동사,형용사,형용동사,대명사,부사,조사,감탄사,연결사,ダナ,ス타동사,명사ノナ,명ノナ

품사목록 = ["명사","동사","형용사","형용동사","대명사","부사","조사","감탄사","연결사","ダナ","ス타동사","명사ノナ","명ノナ"]

tl = [t1, t2, t3]
for t in tl : 
    t = remove_brackets(t)
    #발음, 뜻, 문법
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
                #품사가 있다는 의미
                뜻 += f" / [{t_splited[i]}] "#품사
                
                continue #품사 기록하고 처음으로 돌아가기
                
    else:
        #뜻이 한개
        뜻 = 뜻_부분
    
    print("뜻 :",뜻)



    '''
    #뜻이 여러개가 아닌경우에는 품사와 의미가 붙는 문제때문에 각주처리.
    try : 
        start_keyword = "단어장에 저장"
        end_keyword = "민중서림 엣센스 일한사전"
        start_index = t.find(start_keyword) + len(start_keyword)+1
        end_index = t.find(end_keyword)
        뜻 = t[start_index:end_index].strip()
        뜻 = 뜻.replace("\n", "")
        뜻 = remove_brackets(뜻)
        print("뜻뜻뜻뜻뜻 :",뜻)
        print("*"*88)
    except : pass



    부수 k 
[{'k': '金', 's': 'きん·こん', 'm': 'かな·かね', 'p': '金 (8획)'}, {'k': '風', 's': 'ふう·ふ', 'm': 'かざ·かぜ', 'p': ' 風 (9획)'}, {'k': '田', 's': 'でん', 'm': 'た', 'p': '田 (5획)'}, {'k': '阜', 's': 'ふ', 'm': '', 'p': '阜 (8획)'}, {'k': '入', 's': 'にゅう', 'm': 'いる·いれる·はいる', 'p': '入 (2획)'}, {'k': '音', 's': 'おん·いん', 'm': 'おと·ね', 'p': '音 (9획)'}, {'k': '酉', 's': 'ゆう', 'm': 'とり·ひよみのとり', 'p': '酉 (7획)'}, {'k': '斗', 's': 'と', 'm': '', 'p': ' 斗 (4획)'}, {'k': '弓', 's': 'きゅう', 'm': 'ゆみ', 'p': '弓 (3획)'}, {'k': '方', 's': 'ほう', 'm': 'かた', 'p': '方 (4 획)'}, {'k': '又', 's': '', 'm': 'また', 'p': '又 (2획)'}, {'k': '比', 's': 'ひ', 'm': 'くらべる', 'p': '比 (4획)'}, {'k': '矢', 's': 'し', 'm': 'や', 'p': '失 (5획)'}, {'k': '皿', 's': '', 'm': 'さら', 'p': '皿 (5획)'}, {'k': '文', 's': ' ぶん·もん', 'm': 'ふみ', 'p': '文 (4획)'}, {'k': '面', 's': 'めん', 'm': 'おも·おもて·つら', 'p': '面 (9획)'}, {'k': '辛', 's': 'しん', 'm': 'からい', 'p': '辛 (7획)'}, {'k': '首', 's': 'しゅ', 'm': 'くび', 'p': '首 (9획)'}, {'k': '氏', 's': 'し', 'm': 'うじ', 'p': '氏 (4획)'}, {'k': '臼', 's': 'きゅう', 'm': 'うす', 'p': '臼 (6획)'}, {'k': '頁', 's': 'けつ·よう', 'm': 'かしら·ページ', 'p': '頁 (9획)'}, {'k': '高', 's': 'こう', 'm': 'たか·たかい·たかまる·たかめる', 'p': '高 (10획)'}, {'k': '馬', 's': 'ば', 'm': 'うま·ま', 'p': '馬 (10획)'}, {'k': '山', 's': 'さん', 'm': 'やま', 'p': '山 (3획)'}, {'k': '甘', 's': 'かん', 'm': 'あまい·あまえる·あまやかす', 'p': '甘 (5획)'}, {'k': '工', 's': 'く·こう', 'm': '', 'p': '工 (3획)'}, {'k': '用', 's': 'よう', 'm': 'もちいる', 'p': '用 (5획)'}, {'k': '車', 's': 'しゃ', 'm': 'くるま', 'p': '車 (7획)'}, {'k': '飛', 's': 'ひ', 'm': 'とばす·とぶ', 'p': '飛 (9획)'}, {'k': '足', 's': 'そく', 'm': 'あし·たす·たりる·たる', 'p': '\ue848 (7획)'}, {'k': '刀', 's': 'とう', 'm': 'かたな', 'p': '刀 (2획)'}, {'k': '長', 's': 'ちょう', 'm': 'ながい', 'p': '長 (8획)'}, {'k': '欠', 's': 'けつ', 'm': 'かく·かける', 'p': '欠 (4획)'}, {'k': '皮', 's': 'ひ', 'm': 'かわ', 'p': '皮 (5획)'}, {'k': '肉', 's': 'にく', 'm': '', 'p': '肉 (6획)'}, {'k': '里', 's': 'り', 'm': 'さと', 'p': '里 (7획)'}, {'k': '人', 's': 'じん·にん', 'm': 'ひと', 'p': '人 (2획)'}, {'k': '鬼', 's': 'き', 'm': 'おに', 'p': '鬼 (10획)'}, {'k': '豆', 's': 'ず·とう', 'm': 'まめ', 'p': '豆 (7획)'}, {'k': '乙', 's': 'おつ', 'm': '', 'p': '乙 (1획)'}, {'k': '寸', 's': 'すん', 'm': '', 'p': '寸 (3획)'}, {'k': '矛', 's': 'む', 'm': 'ほこ', 'p': '矛 (5획)'}, {'k': '瓜', 's': 'か', 'm': 'うり', 'p': '瓜 (6획)'}, {'k': '糸', 's': 'し', 'm': 'いと', 'p': '糸 (6획)'}, {'k': '舟', 's': 'しゅう', 'm': 'ふな·ふね', 'p': '舟 (6획)'}, {'k': '犬', 's': 'けん', 'm': 'いぬ', 'p': '犬 (4획)'}, {'k': '八', 's': 'はち', 'm': 'や·やつ·やっつ·よう', 'p': '八 (2획)'}, {'k': '己', 's': 'こ·き', 'm': 'おのれ', 'p': '己 (3획)'}, {'k': '牙', 's': 'げ·が', 'm': 'きば', 'p': '牙 (4획)'}, {'k': '穴', 's': 'けつ', 'm': 'あな', 'p': '穴 (5획)'}, {'k': '走', 's': 'そう', 'm': 'はしる', 'p': '走 (7획)'}, {'k': '十', 's': 'じっ·じゅう', 'm': 'と·とお', 'p': '十 (2획)'}, {'k': '玉', 's': 'ぎょく', 'm': 'たま', 'p': '玉 (5획)'}, {'k': '羽', 's': 'う', 'm': 'は·はね', 'p': '羽 (6획)'}, {'k': '臣', 's': 'しん·じん', 'm': '', 'p': '臣 (7획)'}, {'k': '非', 's': 'ひ', 'm': '', 'p': '非 (8획)'}, {'k': '士', 's': 'し', 'm': '', 'p': '士 (3획)'}, {'k': '雨', 's': 'う', 'm': 'あま·あめ', 'p': '雨 (8획)'}, {'k': '土', 's': 'と·ど', 'm': 'つち', 'p': '土 (3획)'}, {'k': '爪', 's': '', 'm': 'つま·つめ', 'p': '爪 (4획)'}, {'k': '牛', 's': 'ぎゅう', 'm': 'うし', 'p': '牛 (4획)'}, {'k': '米', 's': 'べい·まい', 'm': 'こめ', 'p': '米 (6획)'}, {'k': '老', 's': 'ろう', 'm': 'おいる·ふける', 'p': '老 (6획)'}, {'k': '水', 's': 'すい', 'm': 'みず', 'p': '水 (4획)'}, {'k': '耳', 's': 'じ', 'm': 'みみ', 'p': '耳 (6획)'}, {'k': '石', 's': 'しゃく·せき·こく', 'm': 'いし', 'p': '石 (5획)'}, {'k': '子', 's': 'し·す', 'm': 'こ', 'p': '子 (3획)'}, {'k': '生', 's': 'しょう·せい', 'm': 'いかす·いきる·いける·うまれる·うむ·なま·はえる·はやす·おう·き', 'p': '生 (5획)'}, {'k': '食', 's': 'しょく·じき', 'm': 'くう·たべる·くらう', 'p': '食 (9획)'}, {'k': '自', 's': 'し·じ', 'm': 'みずから', 'p': '自 (6획)'}, {'k': '止', 's': 'し', 'm': 'とまる·とめる', 'p': '止 (4획)'}, {'k': '立', 's': 'りつ·りゅう', 'm': 'たつ·たてる', 'p': '立 (5획)'}, {'k': '目', 's': 'もく·ぼく', 'm': 'め·ま', 'p': '目 (5획)'}, {'k': '舌', 's': 'ぜつ', 'm': 'した', 'p': '舌 (6획)'}, {'k': '貝', 's': '', 'm': 'かい', 'p': '貝 (7획)'}, {'k': '川', 's': 'せん', 'm': 'かわ', 'p': '川 (3획)'}, {'k': '示', 's': 'じ·し', 'm': 'しめす', 'p': '示 (5획)'}, {'k': '手', 's': 'しゅ', 'm': 'て·た', 'p': '手 (4획)'}, {'k': '缶', 's': 'かん', 'm': '', 'p': '缶 (6획)'}, {'k': '見', 's': 'けん', 'm': 'みえる·みせる·みる', 'p': '見 (7획)'}, {'k': '夕', 's': 'せき', 'm': 'ゆう', 'p': '夕 (3획)'}, {'k': '色', 's': 'しき·しょく', 'm': 'いろ', 'p': '色 (6획)'}, {'k': '日', 's': 'じつ·にち', 'm': 'か·ひ', 'p': '日 (4획)'}, {'k': '干', 's': 'かん', 'm': 'ほす·ひる', 'p': '干 (3획)'}, {'k': '言', 's': 'げん·ごん', 'm': 'いう·こと', 'p': '言 (7획)'}, {'k': '骨', 's': 'こつ', 'm': 'ほね', 'p': '骨 (10획)'}, {'k': '谷', 's': 'こく', 'm': 'たに', 'p': '谷 (7획)'}, {'k': '几', 's': 'き', 'm': 'つくえ·ひじかけ', 'p': '几 (2획)'}, {'k': '大', 's': 'たい·だい', 'm': 'おお·おおいに·おおきい', 'p': '大 (3획)'}, {'k': '女', 's': 'じょ·にょ·にょう', 'm': 'おんな·め', 'p': '女 (3획)'}, {'k': '斤', 's': 'きん', 'm': '', 'p': '斤 (4획)'}, {'k': '白', 's': 'はく·びゃく', 'm': 'しら·しろ·しろい', 'p': '白 (5획)'}, {'k': '角', 's': 'かく', 'm': 'かど·つの', 'p': '角 (7획)'}, {'k': '王', 's': 'おう', 'm': '', 'p': '王 (4획)'}, {'k': '赤', 's': 'せき·しゃく', 'm': 'あか·あかい·あからむ·あからめる', 'p': '赤 (7획)'}, {'k': '辰', 's': 'しん', 'm': 'たつ·とき·ひ', 'p': '辰 (7획)'}, {'k': '戶', 's': 'こ', 'm': 'と', 'p': '戸 (4획)'}, {'k': '月', 's': 'がつ·げつ', 'm': 'つき', 'p': '月 (4획)'}, {'k': '羊', 's': 'よう', 'm': 'ひつじ', 'p': '羊 (6획)'}, {'k': '至', 's': 'し', 'm': 'いたる', 'p': '至 (6획)'}, {'k': '支', 's': 'し', 'm': 'ささえる', 'p': '支 (4획)'}, {'k': '門', 's': 'もん', 'm': 'かど', 'p': '門 (8획)'}, {'k': '戈', 's': 'か', 'm': 'いくさ·ほこ', 'p': ' 戈 (4획)'}, {'k': '毛', 's': 'もう', 'm': 'け', 'p': '毛 (4획)'}, {'k': '虫', 's': 'ちゅう', 'm': 'むし', 'p': '虫 (6획)'}, {'k': '竹', 's': 'ちく', 'm': 'たけ', 'p': '竹 (6획)'}, {'k': '瓦', 's': 'が', 'm': 'かわら', 'p': '瓦 (5획)'}, {'k': '木', 's': 'ぼく·もく', 'm': 'き·こ', 'p': '木 (4획)'}, {'k': '血', 's': 'けつ', 'm': 'ち', 'p': '血 (6획)'}, {'k': ' 行', 's': 'ぎょう·こう·あん', 'm': 'いく·おこなう·ゆく', 'p': '行 (6획)'}, {'k': '口', 's': 'く·こう', 'm': 'くち', 'p': '口 (3획)'}, {'k': '火', 's': 'か', 'm': 'ひ·ほ', 'p': '火 (4획)'}, {'k': '一', 's': 'いち·いつ', 'm': 'ひと·ひとつ', 'p': '一 (1획)'}, {'k': '衣', 's': 'い', 'm': 'ころも', 'p': '衣 (6획)'}, {'k': '香', 's': 'こう·きょう', 'm': 'か·かおり·かおる', 'p': '香 (9획)'}, {'k': '二', 's': 'に', 'm': 'ふた·ふたつ', 'p': '二 (2획)'}, {'k': '巾', 's': 'きん', 'm': '', 'p': '巾 (3획)'}, {'k': '身', 's': 'しん', 'm': 'み', 'p': '身 (7획)'}, {'k': '力', 's': 'りき·りょく', 'm': 'ちから', 'p': '力 (2획)'}, {'k': '邑', 's': 'おう·ゆう', 'm': 'うれえる·くに·みやこ·むら', 'p': '邑 (7획)'}, {'k': '心', 's': 'しん', 'm': 'こころ', 'p': '心 (4획)'}, {'k': '片', 's': 'へん', 'm': 'かた', 'p': '片 (4획)'}, {'k': '卜', 's': 'ほく· ぼく', 'm': 'うらない·うらなう', 'p': '卜 (2획)'}, {'k': '革', 's': 'かく', 'm': 'かわ', 'p': '革 (9획)'}, {'k': '玄', 's': 'げん', 'm': '', 'p': '玄 (5획)'}, {'k': '靑', 's': 'せい·しょう', 'm': 'あお·あおい', 'p': '青 (8획)'}, {'k': '父', 's': 'ふ', 'm': 'ちち', 'p': '父 (4획)'}, {'k': '小', 's': 'しょう', 'm': 'お·こ·ちいさい', 'p': '小 (3획)'}]

    '''




