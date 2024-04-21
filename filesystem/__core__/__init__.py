import requests
from filesystem import console

__version__ = "1.0.2.0"

def __checkupdates__(user, repo):
    ### TAG PATTERN: v1.2.3.4
    current_version_string = ''.join(filter(str.isdigit, __version__))
    current_version = int(current_version_string)
    update_version = 0

    ### Check updates online using 'requests'
    url = f'https://api.github.com/repos/{user}/{repo}/releases'
    try:
        response = requests.get(url)
        # response.raise_for_status()
    except requests.exceptions.RequestException as err:
        # print(f"{Fore.RED} >> [FileSystem Pro] This exception: {Fore.YELLOW}{err}{Style.RESET_ALL}")
        return None, None
    releases = response.json()
    
    for release in releases:
        if update_version == 0:
            tag_name = f'{release["tag_name"]}'
            update_version_string = ''.join(filter(str.isdigit, tag_name))
            update_version = int(update_version_string)

    if current_version < update_version:
        print(f"[{console.fore.BLUE}Notice{console.style.RESET_ALL}]: A new release of FileSystemPro is available: {console.fore.RED}v{__version__}{console.style.RESET_ALL} -> {console.fore.GREEN}{tag_name}{console.style.RESET_ALL}")
        print(f"[{console.fore.BLUE}Notice{console.style.RESET_ALL}]: To update, run: {console.fore.GREEN}pip install --upgrade filesystempro{console.style.RESET_ALL}")