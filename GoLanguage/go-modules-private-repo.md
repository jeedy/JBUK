# Go 프라이빗 모듈 가져오기

참조: 
- https://mingrammer.com/go-modules-private-repo/
- https://johanlejdung.medium.com/a-mini-guide-go-modules-and-private-repositories-fa94c3726cf1

## Go Get 동작 방식 (bulid시 import 될 외부 모듈이 이씅ㄹ때 사용하는 go Command )
외부 패키지를 가져오는 `go get` 명령어는 기본적으로 import path를 보고 어떤 vcs를 사용하는지 판단한 뒤, 해당 vcs에 맞는 스키마를 통해 패키지를 다운로드 받는다. 이 글에서 import path로부터 vcs를 판단하는 모든 단계를 설명하지는 않지만, 기본적으로 import path가 github.com으로 시작하면 해당 패키지는 github.com 호스팅과 git vcs를 사용한다고 판단하며 `https://`와 `git+ssh://` 스키마 순서로 다운로드를 시도한다. 따라서 이미 ssh를 사용하고 있다면 ssh로 접근할 수 있는 모든 프라이빗 저장소의 패키지를 가져올 수 있다.

> 물론, ssh를 사용하지 않은 상태에서는 프라이빗 모듈을 가져올 수 없기 때문에 git config에서 ssh를 사용하도록 설정해줘야 한다.   
ssh 설정방법은 https://johanlejdung.medium.com/a-mini-guide-go-modules-and-private-repositories-fa94c3726cf1 참조
