from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

def get_jlpt_words_from_jisho(kanji: str):
    search_url = f"https://jisho.org/search/{quote(kanji)}%20%23words%20%23jlpt"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    time.sleep(2)
    jlpt_words = []
    entries = driver.find_elements(By.CSS_SELECTOR, '.concept_light.clearfix')
    for idx, entry in enumerate(entries):
        jlpt_tags = entry.find_elements(By.CSS_SELECTOR, '.concept_light-tag.label')
        tag_texts = [tag.text.lower() for tag in jlpt_tags]
        if any('jlpt' in t for t in tag_texts):
            try:
                text_elem = entry.find_element(By.CSS_SELECTOR, '.text')
                word = text_elem.text.strip()
                if word:
                    jlpt_words.append(word)
            except Exception as e:
                pass
    driver.quit()
    return jlpt_words

def remove_hiragana_if_not_multiple_kanji(word):
    # 한자(統一表記법) 범위: \u4e00-\u9fff
    kanji_count = len(re.findall(r'[\u4e00-\u9fff]', word))
    if kanji_count >= 2:
        return word
    # 히라가나, 가타카나 제거
    return re.sub(r'[ぁ-ゖァ-ヺ]+', '', word)



def remove_hiragana_if_not_multiple_kanji(item):
    """
    입력값이 문자열이면 한 개만 처리, 리스트면 map 적용 후 리스트 반환.
    한자가 2개 이상이면 원본 반환,
    그렇지 않으면 히라가나(ぁ-ゖ) 및 가타카나(ァ-ヺ) 제거
    """
    def process(word):
        kanji_count = len(re.findall(r'[\u4e00-\u9fff]', word))
        if kanji_count >= 2:
            return word
        return re.sub(r'[ぁ-ゖァ-ヺ]+', '', word)
    if isinstance(item, str):
        return process(item)
    elif isinstance(item, list):
        return [process(w) for w in item]
    else:
        raise TypeError('입력값은 str 또는 list만 허용됩니다.')
    
THREAD_COUNT = 1

if __name__ == '__main__':
    result = []
    kanji_list = input("검색할 한자들을 입력하세요(皮...披)\n: ").strip()
    kanji_list = list(kanji_list)
    # 병렬 처리(스레드 수는 환경에 따라 조정, 너무 크면 CPU/RAM 과부하)
    
    THREAD_COUNT = len(kanji_list)
    THREAD_COUNT = 3
    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        future_to_kanji = {executor.submit(get_jlpt_words_from_jisho, kanji): kanji for kanji in kanji_list}
        for future in as_completed(future_to_kanji):
            kanji = future_to_kanji[future]
            try:
                words = future.result()
                print(f"words for '{kanji}':", words)
                result.extend(words)
            except Exception as exc:
                print(f"[ERROR] {kanji} 처리 중 예외 발생:", exc)
    print("*"*88)
    result = remove_hiragana_if_not_multiple_kanji(result)
    result = [word for word in result if len(word) >= 2]
    print(result)
