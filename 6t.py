import subprocess

def find_commit_by_message(search_word):
    try:
        git_log_output = subprocess.check_output(['git', 'log', '--oneline', '--decorate', '--pretty=full'])
        git_log_output = git_log_output.decode('utf-8')
        

        commit_lines = git_log_output.split('\n')
        current_commit = None
        commits = []

        for line in commit_lines:
            if line.startswith('commit'):
                if current_commit:
                    commits.append(current_commit)
                current_commit = {'commit_hash': line.split(' ')[1]}
            elif line.startswith('    '):
                current_commit['message'] = line.strip()
            else:
                continue

        if current_commit:
            commits.append(current_commit)

        found_commits = []
        for commit in commits:
            if 'message' in commit and search_word in commit['message']:
                found_commits.append(commit['commit_hash'])

        if found_commits:
            print(f"Commit with search term {search_word}:")
            for commit_hash in found_commits:
                print(commit_hash)
        else:
            print(f"Commitment containing search term '{search_word}' was not found.")

    except subprocess.CalledProcessError as e: print(f"errer inbound : {e}")
    except Exception as e: print(f"error contact : {e}")

search_word = input("enter whats your want to search : ")
find_commit_by_message(search_word)
