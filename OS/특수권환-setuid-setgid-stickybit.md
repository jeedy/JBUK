# 특수 권한(setuid, setgid, sticky bit)
tags: RGID, RUID, setgid 비드, setuid 비트, sticky bit, sticky 비트, 특수권한, linux 특수권한, unix 특수권한, 유효 사용자 ID
, 유효 사용자 그룹ID, 소유주 권한

참고 자료: https://eunguru.tistory.com/115

## 프로세스 번호
UNIX 시스템에서 프로세스에 다섯 가지 번호 부여

### 1) 프로세스에 부여되는 번호들
- 프로세스 식별자(PID)
- 실제 사용자 ID(RUID)
- 유효 사용자 ID(EUID)
- 실제 사용자 그룹 ID(RGID)
- 유효 사용자 그룹 ID(EGID)


### 2) 사용용도
- 계정 관리: RUID, RGID
- 접근 권한 결정에 사용: EUID, EGID(보안에 주의)
- 일반적으로 실제사용자(그룹), 유효사용자(그룹) ID 값은 동일하다


## 시스템에서 사용자가 명령 실행시 명령어를 찾는 경로와 절차

![명령어 실형 절차](./images/system-command-workflow.jpg)



## 접근권한

- 접근 권한은 8진수 또는 r(읽기권한,4), w(쓰기권한,2), x(실행권한,1) 문자로 표현 가능
- 8진수로 표현할 때는 권한의 합으로 표시함 (예: 읽기+쓰기 6, 읽기+실행 5 등)
- 8진수 3자리(3bit)로 수유자, 그룹 소유자, 기타 사용자를 위한 파일 모드 설정

접근권한 예:
> 접근 권한을 755로 표현하는 것과 0755로 표현하는 것은 동일한 표현, 네 자리가 되지 않으면 앞에 0이 생략된다.

![접근 권한 설정 예제](./images/chmod-755-example.jpg)


## 특수권한
- UNIX 시스템은 파일에 대한 접근 권한 및 파일 종류를 나타내기 위해 16bit를 사용한다.
- 각 3bit씩 총 9bit는 소유자 접근권한(user), 그룹 소유자 접근권한(group), 기타 사용자 접근권한(other)을 기술하는데 사용
- 4bit는 파일의 종류 표현에 사용
- 3bit는 특수권한에 사용

각 비트에 대한 설명: <br>
![비트에 대한 설명](./images/chmod-0755-description.jpg)

<table cellspacing="0" cellpadding="0" border="0">
<thead>
<tr><td colspan="4"><p><b> 파일종류</b></p></td>
<td colspan="4"><p style="text-align: center;"><b><span style="color: rgb(255, 94, 0);">특수권한</span></b></p></td>
<td colspan="3"><p style="text-align: center;"><b>소유자접근권한</b></p></td>
<td colspan="3"><p style="text-align: center;"><b>그룹 소유자 접근권한</b></p></td>
<td colspan="3"><p style="text-align: center;"><b>기타 사용자 접근 권한</b></p></td>
</tr>
</thead>
<tbody>
<tr><td colspan="4" rowspan="2"><p style="text-align: center;">-,d,c,b,s,l,p</p></td>
<td><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">4</span></p></td>
<td><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">2</span></p></td>
<td colspan="2"><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">1</span></p></td>
<td><p style="text-align: center;">4</p></td>
<td><p style="text-align: center;">2</p></td>
<td><p style="text-align: center;">1</p></td>
<td><p style="text-align: center;">4</p></td>
<td><p style="text-align: center;">2</p></td>
<td><p style="text-align: center;">1</p></td>
<td><p style="text-align: center;">4</p></td>
<td><p style="text-align: center;">2</p></td>
<td><p style="text-align: center;">1</p></td>
</tr>
<tr>
<td><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">setuid</span></p></td>
<td><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">setgid</span></p></td>
<td colspan="2"><p style="text-align: center;"><span style="color: rgb(255, 94, 0);">sticky bit</span></p></td>
<td><p style="text-align: center;">r</p></td>
<td><p style="text-align: center;">w</p></td>
<td><p style="text-align: center;">x</p></td>
<td><p style="text-align: center;">r</p></td>
<td><p style="text-align: center;">w</p></td>
<td><p style="text-align: center;">x</p></td>
<td><p style="text-align: center;">r</p></td>
<td><p style="text-align: center;">w</p></td>
<td><p style="text-align: center;">x</p></td>
</tr>
</tbody>
</table>