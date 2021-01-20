# Jboss 관련 자료

## 목차
- [JBoss 쓰레드풀 설정 방법](./jboss-threadpool-configuration.md)
- [Jboss deploy 에 대해서]()


## 배포시 marker filetype 상세 설명
참고: https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/6.4/html/administration_and_configuration_guide/sect-deploy_with_the_deployment_scanner

Filename | origin | Description
| - | - | - |
.dodeploy | 사용자 생성 | 콘텐츠가 런타임에 배포 또는 재배포되어야 함을 나타냅니다.
.skipdeploy | 사용자 생성 | 존재하는 동안 애플리케이션의 자동 배포를 비활성화합니다. 배포시 위험 있는 콘텐츠의 자동 배포를 일시적으로 차단하여 불완전한 콘텐츠 편집이 라이브로 푸시되는 위험을 방지하는 방법으로 유용합니다. 스캐너가 압축 된 콘텐츠에 대한 진행중인 변경 사항을 감지하고 완료 될 때까지 대기하지만 압축 된 콘텐츠와 함께 사용할 수 있습니다.
.isdeploying | 시스템 생성	| 배포 시작을 나타냅니다. 배포 프로세스가 완료되면 마커 파일이 삭제됩니다.
.deployed | 시스템 생성 | 콘텐츠가 배포되었음을 나타냅니다. 이 파일이 삭제되면 콘텐츠가 배포 해제됩니다.
.failed | 시스템 생성 | 배포 실패를 나타냅니다. 마커 파일에는 실패 원인에 대한 정보가 포함되어 있습니다. 마커 파일이 삭제되면 콘텐츠가 자동 배포에 다시 표시됩니다.
.isundeploying | 시스템 생성 | `.deployed`파일 삭제에 대한 응답을 나타냅니다. 콘텐츠 배포가 취소되고 완료시 마커가 자동으로 삭제됩니다.
.undeployed | 시스템 생성 | 콘텐츠가 배포 취소되었음을 나타냅니다. 마커 파일을 삭제해도 콘텐츠 재배포에 영향을주지 않습니다.
.pending | 시스템 생성 | 발견 된 문제가 해결 될 때까지 배포 지침이 서버로 전송 될 것임을 나타냅니다. 이 마커는 글로벌 배포로드 블록 역할을합니다. 스캐너는이 조건이 존재하는 동안 다른 콘텐츠를 배포하거나 배포 취소하도록 서버에 지시하지 않습니다.

> auto deploy 가 걸려있지 않다면 `.dodeploy` 파일을 touch 해야 재배포를 진행한다.

```bash
[user@host bin]$ touch EAP_HOME/standalone/deployments/example.war.dodeploy
```