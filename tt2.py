import math

def split_file_into_parts(input_file, num_parts=10):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    lines_per_part = math.ceil(total_lines / num_parts)

    for i in range(num_parts):
        start = i * lines_per_part
        end = min(start + lines_per_part, total_lines)
        part_lines = lines[start:end]

        # 파일명: chats_part01.txt ~ chats_part10.txt
        part_file = f'chats_part{str(i+1).zfill(2)}.txt'
        with open(part_file, 'w', encoding='utf-8') as pf:
            pf.writelines(part_lines)

        print(f'{part_file}: {start+1}~{end}줄 저장 완료')

# 사용 예시
split_file_into_parts('chats.txt', 10)
