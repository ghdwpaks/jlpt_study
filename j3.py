import random
s = [

["ア","아"],["イ","이"],["ウ","우"],["エ","에"],
["オ","오"],["カ","카"],["キ","키"],["ク","쿠"],
["ケ","케"],["コ","코"],["サ","사"],["シ","시"],
["ス","스"],["セ","세"],["ソ","소"],["タ","타"],
["チ","치"],["ツ","츠"],["テ","테"],["ト","토"],
["ナ","나"],["ニ","니"],["ヌ","누"],["ネ","네"],
["ノ","노"],["ハ","하"],["ヒ","히"],["フ","후"],
["ヘ","헤"],["ホ","호"],["マ","마"],["ミ","미"],
["ム","무"],["メ","메"],["モ","모"],["ヤ","야"],
["ユ","유"],["ヨ","요"],["ラ","라"],["リ","리"],
["ル","루"],["レ","레"],["ロ","로"],["ワ","와"],
["ヲ","오"],["ン","은"],["キャ","캬"],["キュ","큐"],
["キョ","쿄"],["シャ","샤"],["シュ","슈"],["ショ","쇼"],
["チャ","챠"],["チュ","츄"],["チョ","쵸"],["ニャ","냐"],
["ニュ","뉴"],["ニョ","뇨"],["ヒャ","햐"],["ヒュ","휴"],
["ヒョ","효"],["ミャ","먀"],["ミュ","뮤"],["ミョ","묘"],
["リャ","랴"],["リュ","류"],["リョ","료"],["ギャ","갸"],
["ギュ","규"],["ギョ","교"],["ジャ","자"],["ジュ","주"],
["ジョ","조"],["ビャ","뱌"],["ビュ","뷰"],["ビョ","뵤"],
["ピャ","피야"],["ピュ","퓨"],["ピョ","표"],["ィ","이"],
["ガ","가"],["ギ","기"],["グ","구"],["ゲ","게"],
["ゴ","고"],["ザ","자"],["ジ","지"],["ズ","즈"],
["ゼ","제"],["ゾ","조"],["ダ","다"],["ヂ","지"],
["ヅ","즈"],["デ","데"],["ド","도"],["バ","바"],
["ビ","비"],["ブ","부"],["ベ","베"],["ボ","보"],
["パ","파"],["ピ","피"],["プ","푸"],["ペ","페"],
["ポ","포"],

]

sc = [0]*len(s)
while True:
    random.shuffle(s)
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







































