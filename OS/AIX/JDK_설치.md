# [AIX] JDK 설치

## JDK 다운로드

http://www.ibm.com/developerworks/java/jdk/aix/j564/fixinfo.html

```bash
[X2:root] / > lslpp -l |grep Java5_64
  Java5_64.ext.commapi     5.0.0.175  COMMITTED  Java SDK 64-bit Comm API
  Java5_64.samples         5.0.0.175  COMMITTED  Java SDK 64-bit Samples
  Java5_64.sdk             5.0.0.235  COMMITTED  Java SDK 64-bit
  Java5_64.source          5.0.0.235  COMMITTED  Java SDK 64-bit Source

  Java5_64.sdk             5.0.0.235  COMMITTED  Java SDK 64-bit
```


## java5_64 지우기
```bash
[X2:root] / >smitty remove
                                                        [Entry Fields]
* SOFTWARE name                            [ESC+4 > java5_64파일셋을 ESC+7로 모두선택]                      +
  PREVIEW only? (remove operation will NOT occur)     yes(tab키를 이용하여 no로 바꿈)
  REMOVE dependent software?                          no                     +
  EXTEND file systems if space needed?                no                     +
  DETAILED output?                                    no                     +
Enter 2번 OK 프롬포트 확인 후 ESC+0으로 빠져나옴
[X2:root] / > lslpp -l |grep Java5_64 //java5_64 삭제확인
```


## 인스톨 하기
```bash
[X2:root] /home/itcen/java베이스레벨/ >smitty install_latest
* INPUT device / directory for software              [.](로컬디렉토리 .)     + 엔터
* INPUT device / directory for software               .
* SOFTWARE to install                                [_all_latest]           +
  PREVIEW only? (install operation will NOT occur)    no                     +
  COMMIT software updates?                            yes                    +
  SAVE replaced files?                                no                     +
  AUTOMATICALLY install requisite software?           yes                    +
  EXTEND file systems if space needed?                yes                    +
  OVERWRITE same or newer versions?                   no                     +
  VERIFY install and check file sizes?                no                     +
  Include corresponding LANGUAGE filesets?            yes                    +
  DETAILED output?                                    no                     +
  Process multiple volumes?                           yes                    +
  ACCEPT new license agreements?                      no(tab키를 이용하여 yes)
  Preview new LICENSE agreements?                     no                     +
```

엔터2번 OK 프롬포트확인 후 ESC+0으로 빠져나옴


## 업데이트 하기
```bash
[X2:root] /home/itcen/java업데이트레벨/ >smitty update_all
* INPUT device / directory for software              [.](로컬디렉토리 .)     + 엔터 
* INPUT device / directory for software               .
* SOFTWARE to update                                  _update_all
  PREVIEW only? (update operation will NOT occur)     no                     +
  COMMIT software updates?                            yes                    +
  SAVE replaced files?                                no                     +
  AUTOMATICALLY install requisite software?           yes                    +
  EXTEND file systems if space needed?                yes                    +
  VERIFY install and check file sizes?                no                     +
  DETAILED output?                                    no                     +
  Process multiple volumes?                           yes                    +
  ACCEPT new license agreements?                      no(tab키를 이용하여 yes)
  Preview new LICENSE agreements?                     no                     +

```

엔터2번 OK 프롬포트확인 후 ESC+0으로 빠져나옴

## 자바 버전확인
```
[X2:root] /home/itcen/java업데이트레벨/ >java -version
```

