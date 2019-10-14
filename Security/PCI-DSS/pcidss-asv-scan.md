# PCI-DSS ASV 스캔 취약점

## 보안 헤더 처리
1. HTTP 보안 헤더가 검색되지 않은 취약점
    - **X-Frame-Option 또는 콘텐츠 보안정책에 HTTP 헤더가 442 포트에서 누락되었습니다.**<br>
    이 옵션은 사이트의 페이지 구성 시 삽입된 프레임의 출처를 검증하여 허용되지 않는 페이지 URL일 경우 해당 프레임을 포함하지 않는 확장응답 헤더 입니다.<br>
    예를 들면 악의적 목적의 공격자가 프리비아의 도메인 주소와 비슷한 도메인을 사서 가짜 프리비아의 피싱 사이트를 구성할 때, 실제 프리비아 사이트의 페이지를 iframe, frame, object 태그로 페이지를 삽입하여 진짜 프리비아 사이트 처럼 보이게 만들 수 있습니다. 옵션이 활성화 되어 있으면 위와 같은 페이지의 구성을 막을 수 있습니다.
        
         - **X-Frame-Options: DENY (프레임 안에 절대 들어가지 못하게 한다)**
         - **X-Frame-Options: SAMEORIGIN (같은 origin일 경우에만 허용한다)**
         - **X-Frame-Options: ALLOW FROM hxtp://some-domain.com (특정 origin에서만 허용한다)**

        - 참조자료
            - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
            - https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet

    - **X-XSS-Protection 헤더가 442 포트에서 누락되었습니다.**<br>
    이 옵션은 웹 브라우저의 내장 XSS Filter 기능을 사용하도록 하는 옵션입니다. 
    해당 옵션이 설정되면 사이트 간 스크립팅 공격이 감지 될 때 웹 브라우저에서 해당 페이지 로딩을 중지하게 됩니다. 
    프리비아 사이트 내에서 XSS 공격을 진행하기 위해서는 게시판에 사용자가 직접 HTML을 이용하여 공격코드를 삽입한 
    게시물을 등록하고 이를 열람한 사용자에게 공격을 진행할 수 있습니다. 
    하지만 프리비아 사이트에는 이러한 게시판이 존재하지 않기 때문에 해당사항이 없습니다. 만약, 사용자가 글을 
    입력하여 서버에 저장하는 기능의 페이지가 존재할 경우, HTML 및 javascript의 삽입을 제한하면 XSS 공격이 
    발생할 수 없기 때문에 X-XSS_Protection 헤더 옵션의 설정 유무는 큰 의미가 없습니다. 하지만 해당 옵션을 설정하면
     보다 높은 보안수준으로 웹 사이트를 운영할 수 있을 것 입니다.
     
        - 참조자료
            - https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/X-XSS-Protection

     - **X-Content-Type-Options HTTP 헤더가 442 포트에서 누락되었습니다.**<br>
     이 옵션은 IE 및 Chrome 브라우저에서 컨텐츠 유형의 응답을 무시하는 것을 방지할 수 있는 옵션입니다. 
     예를 들면 javascript 파일 .js의 확장자를 .jpg로 변경하여 사용하는 것을 말합니다. 
     (ex `<script src="./test.jpg">`) 이러한 형태로 신뢰되지 않은 컨텐츠가 사용자 브라우저에서 실행되게끔 할 수 
     있는데, 이 공격은 사용자가 프리비아 사이트에서 HTML 사용이 가능한 게시물 작성이 가능할 때 공격을 진행할 수 
     있습니다. 현재 프리비아 사이트에서는 이러한 환경이 아니기 때문에 해당 사항이 없으며, 만약 글 등록이 
     가능한 부분이 있다면 HTML 사용을 차단하여 공격을 제한할 수 있습니다. 해당 옵션을 설정이 꼭 필요할 경우에는 
     아래 URL을 통해 설정을 진행하시면 될 것 같습니다.
     
        - 참조자료
            - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
     
     - **Content-Security-Policy HTTP 헤더가 442포트에서 누락되었습니다.**<br>
     이 옵션은 외부에 있는 스크립트를 이용한 XSS 공격을 방어하는 옵션으로, 위의 옵션과 동일하게 프리비아 사이트 내의 
     게시판 같은 곳에 특정 사용자가 직접 HTML을 작성한 게시물을 생성하여 이를 열람한 사용자에게 공격을 진행하는 
     형태입니다. 프리비아 사이트에서는 이러한 게시판이 존재하지 않아 해당 사항이 없습니다. 
     하지만 해당 옵션을 설정하면 보다 높은 보안수준으로 웹 사이트를 운영할 수 있을 것 입니다.
     
        - 참조자료
            - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
            - https://dvcs.w3.org/hg/user-interface-safety/raw-file/tip/user-interface-safety.html#generatedID
            - https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet
            - https://www.html5rocks.com/en/tutorials/security/content-security-policy/
            - 아파치 : http://httpd.apache.org/docs/2.2/mod/mod_headers.html
            - NginX : http://nginx.org/en/docs/http/ngx_http_headers_module.html



2. 세션쿠키에 ‘Secure’ 속성 미적용
세션쿠키에 ‘Secure’ 속성을 적용하는 것은 해당 쿠키 값에 민감한 정보가 들어 있을 경우 해당 정보를 보호하기 위해 
HTTPS 프로토콜 상에서 암호화된 요청일 경우에만 전송되는 쿠키 속성 값입니다. Secure 속성이 지정 되지 않으면 암호화 
되지 않은 HTTP 페이지에 액세스 하는 경우에도 전송 되어 버리기 때문에 스니핑에 의해 노출 될 위험이 있습니다.
 
세션쿠키를 포함한 모든 쿠키 값에 민감한 정보가 평문(Plain Text)으로 존재할 경우, Secure 속성이 필요할 수 있겠으나, 
프리비아 사이트에서 사용하는 쿠키 값은 확인 불가능한 알고리즘의 해시 값 형태로 사용되고 있고, 민감한 정보가 포함되어 
있지 않아 Secure 속성 적용 여부는 큰 의미가 없습니다.

