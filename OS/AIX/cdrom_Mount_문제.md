# [AIX] cdrom Mount 문제

상황 : File명이 임의로 변경되는 문제

`jboss-eap-5.0` 이 file명이 였다면, `jbosse~1`

### 5.9.2.3. ISO 9660

1987년에 ISO (International Organization for Standardization)에서는 9660 표준을 발표하였습니다. ISO 9660은 CD-ROM 파일 형식을 규정합니다. Red Hat Enterprise Linux 시스템 관리자들은 ISO 9660 형식 자료를 다음과 같은 두가지 데이터에서 자주 볼 수 있습니다

- CD-ROM
-  ISO 이미지라고 부르는 파일은 완전한 ISO 9660 파일 시스템으로서 CD-R 이나 CD-RW 매체에 기록 가능합니다.

기본 ISO 9660 표준은 다른 최신 파일 시스템과 비교하였을때 기능면에서 비교적 제한됩니다. 파일 이름은 최대한 7개 글자까지 가능하며 확장자는 3 글자 이상 사용 불가능합니다. 그러나 시간이 흐르면서 다음과 같이 표준에 다양한 확장이 추가되었습니다

- Rock Ridge — ISO 9660에는 정의되지 않은 일부 영역을 사용하여 긴 소문자, 대문자 구분 가능한 파일 이름 및 심볼릭 링크, 중첩 디렉토리(nested directory: 디렉토리 내에 또 다른 디렉토리를 포함하는 것)와 같은 기능을 추가 지원합니다.
- Joliet — Microsoft가 개발한 ISO 9660 표준 확장으로서 유니코드 문자 세트를 사용하여 CD-ROM에서 긴 파일 이름을 사용할 수 있게 지원해줍니다.

Red Hat Enterprise Linux는 Rock Ridge와 Joliet 확장을 모두 이용하여 ISO 9660 파일 시스템을 정확히 해석할 수 있습니다.

원본 위치 <http://web.mit.edu/rhel-doc/4/RH-DOCS/rhel-isa-ko-4/s1-storage-rhlspec.html>


### 12. 다른 파일 시스템을 붙이고 떼기: mount, umount

윈도우에서는 cd-rom이나 floppy, 물리적 또는 논리적인(파티션에의한 디스크의 논리적 분할)하드 디스크를 각각의 드라이브로 인식한다.
그러나 리눅스에서는 각각의 드라이브들을 mount 과정을 통해서 디렉터리로 인식한다.

예를 들면 플로피는 mnt/floppy로 cd-rom은 mnt/cdrom으로 인식된다.
리눅스에서 마운트 시킬 수 있는 시스템은 fat, vfat, fat32, ext2fs... 등으로 매우 다양합니다.
윈도우에서는 상상도 못하는 일이죠. 윈도우로 부팅해보세요 리눅스 파티션이 보이지 않습니다.

`mount` 명령은 장치명과 마운트 시킬 디렉터리를 적어주어야 한다.
만약 프라이머리 마스터에 장착된 하드의 첫 번째 파티션을 /mnt/win으로 마운트하려면 먼저 /mnt/win 디렉터리를 만든다
그 다음 `$ mount /dev/hda1 /mnt/win` 이라고 하면 된다.
파일 시스템은 리눅스가 자동으로 판단하나 그렇지 못할 경우 -t옵션을 사용한다.
윈도우 파티션의 경우는 vfat으로 마운트해야 긴 파일명을 볼 수 있다.
붙였던 장치를 떼어내려면 `umount`명령을 사용한다.

 각 디스크별 장치명은 다음과 같다.
- 프라이머리 마스터: hda
- 프라이머리 슬레이브: hdb
- 세컨더리 마스터: hdc (주로 cd-rom이 사용한다)
- 세컨더리 슬레이브: hdd
- SCSI 장치: sda, sdb ....
- 플로피 드라이브: fd0

※하드디스크에 파티션이 여러 개라면 뒤에 파티션 번호를 적는다. ex) hda1, hda2 ....
- mount -[w(읽기,쓰기)/r(읽기)/t 파일시스템유형 /f(마운트점검)] [디바이스] [마운트할디텍토리]
- mount -t iso9660 /dev/cdrom /mnt/cdrom
- mount -t msdos /dev/fd0 /mnt/floppy
- mount -t ext3 /dev/hdb /data : 리눅스 파일 시스템
- mount -t vfat /dev/hdb /data : 윈도우 파일 시스템
- mount /dev/fd0 /mnt/floppy
- umount /mnt/floppy
- mount /dev/hdc /mnt/cdrom
- umount /mnt/cdrom

### 13. 호스트 컴퓨터 이름 알기: hostname
