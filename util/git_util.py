import os


def git_state():
    result_list = os.popen('git config --list').readlines()
    for result in result_list:
        if "proxy" in result:
            return True
    return False


def open_git():
    os.system('git config --global http.proxy socks5://127.0.0.1:7890 && '
              'git config --global https.proxy socks5://127.0.0.1:7890')


def close_git():
    os.system('git config --global --unset http.proxy && git config --global --unset https.proxy')
