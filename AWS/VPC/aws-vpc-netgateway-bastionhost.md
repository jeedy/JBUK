# AWS VPC를 디자인해보자(3) -  Private Network을 위한 NAT Gateway 와 Bastion 호스트
VPC(Virtual Private Cloud) 서비스는 AWS 사용자가 직접 가상 네트워크 환경을 구성하는 서비스이다. 
이 서비스를 이용하면 Public network 환경과 Private network 환경을 사용자가 원하는대로 디자인하고 구축할 수 있게 된다.

또한 다양한 부가 기능을 통해 VPC 환경 내 네트워크 흐름을 제어할 수 있기 때문에 나만의 가상 데이터 센터를 구축하여 
사용할 수 있게 된다.

이번 포스팅에는 VPC의 Private Subnet을 위한 NAT Gateway 와 Bastion host에 대해 알아보자.

## 출처
 - https://bluese05.tistory.com/48
 
##  