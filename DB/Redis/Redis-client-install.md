# Redis Client install 방법
레디스 GUI 클라이언트 프로그램들의 설치하는 방법을 기록한다.

## Redis Desktop Manager for Windows (대표적인 클라이언트) 
설치 불편, 기본적으로 유료이다. 그러나 Github에서 다운받아 직접 빌드하면 1년동안 공짜(1년후에 다시 git 받아서 빌드해야한다. qt 플랫폼 필요.)
> 최신버전은 직접 빌드해야하는데 old 버전은 다운받을수있다. old 버전을 사용해도 아무런 이상없음.
  [RedisDesktopManager-0.8.8](https://github.com/uglide/RedisDesktopManager/releases/tag/0.8.8)


## Redis Client (redisdesktop for mac)
```bash
$ brew cask install rdm
```

## ~~iedis for Intellij plugin~~ 
이거 mybatis plugin이 필요한데 이 mybatis plugin이 유료임.


## redis-cli