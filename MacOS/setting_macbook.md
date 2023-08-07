# 맥북 초기셋팅

## 1. 홈브류(https://brew.sh/) 셋팅

## 2. iterm2 설치
```sh
$ brew install --cask iterm2

# 디렉토리 생성
$ mkdir ~/.ssh

# 소유자에 읽기, 쓰기, 실행 권한 부여
$ chmod 700 ~/.ssh
```

### 2.1. ppl → pem 키 변환
ref. [mac 에서 ssh ppk 키 pem 키로 변환 및 접속](https://lab.naminsik.com/4043)

```sh
$ brew install putty
$ cd {ppk 저장된 경로}
$ puttygen {사용자PPK키}.ppk -O private-openssh -o ~/.ssh/{사용자PPK키}.pem
$ chmod 600 ~/.ssh/{사용자PPK키}.pem
```

### 2.2. ssh_config 파일 수정
```sh
# 어드민 권한으로 열어야 수정이 가능하다.
vim ~/.ssh/ssh_config

Host *
    SendEnv LANG LC_*
    PubkeyAcceptedKeyTypes=+ssh-rsa
    HostKeyAlgorithms=+ssh-rsa
```

## 3. 한영키 셋팅

### 3.1. "이전 입력소스 선택" 비활성화
"이전 입력 소스 선택"은 한영 변환이 느려서 아예 꺼놓자
```
Setting > 키보드 > 키보드 단축키... 클릭 > 입력 소스 > "이전 입력 소스 선택" 체크박스 해제
```

### 3.2. 한영 단축키 변경

1. Finder의 메뉴 중 Go > Go to Folder (Cmd+Shift+G)를 선택하여서, "~/Library/Preferences/com.apple.symbolichotkeys.plist" 파일오픈 (Xcode로 열것)
1. 61 > value > parameters > Item 0 = 32, Item 1 = 49, Item 2 = 131072 
1. (반드시)재부팅 필수

## 4. Oh my zsh 설치
ref. https://ohmyz.sh/

```sh
# omz 설치
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
$ brew install zsh
$ brew install zsh-autosuggestions
$ brew install zsh-syntax-highlighting
```

### 4.1. 테마 셋팅
1. [.zshrc 파일 복붙](./asset/.zshrc)

