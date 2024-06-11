import random
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

random.shuffle(s)
sc = [0]*len(s)
while True:
    for question in s:
        japanese, korean = question
        user_input = input(f"{japanese}: ")
        if user_input == "exit" :
            for i in range(len(s)):
                s[i].append(sc[i])
            sorted_s = sorted(s, key=lambda x: x[2], reverse=True)
            for i in sorted_s : print(i)
            break
        elif user_input == korean:print("")
        else:
            for i, row in enumerate(s):
                if korean == row[1]:
                    sc[i] += 1
                    break

            print(f"{korean}\n")