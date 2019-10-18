# VPC를 디자인해보자 (1) - Multi AZ를 활용한 고가용성
VPC(Virtual Private Cloud) 서비스는 AWS 사용자가 직접 가상 네트워크 환경을 구성하는 서비스이다. 이 서비스를 이용하면 
Public / Private network 환경을 사용자가 원하는대로 디자인하고 구축할 수 있게 되며, 다양한 부가 기능을 통해 VPC 환경 내 네트워크 흐름을 제어할 수 있다. 

먼저 VPC를 이해하려면, 기존의 물리 IDC 환경을 디자인 할 때 상황을 비교해서 생각해 보면 쉽게 이해할 수 있다. 
이번 포스팅에는 데이터 센터 구성에서도 Multi 데이터센터 구성과 AWS의 VPC 서비스를 비교해 보고자 한다. 

## 출처
 - https://bluese05.tistory.com/45
 
## 1. Multi AZ VPC를 활용한 Multi 데이터센터(IDC) 구성 효과