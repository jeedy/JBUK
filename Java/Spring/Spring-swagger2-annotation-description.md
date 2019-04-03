# Spring framework 에서 사용 사용되는 Swagger 3 API @Annotation 정리

swagger 3.0 버전 Document 기준으로 설명한다.

## Controller 

### @Api(tags="항공")

#### Noncompliant Code Example
~~@Api(value="항공", description="항공")~~

- description : **deprecated**. 더이상 지원하지 않는다.
- value : 입력하지 않아도 자동으로 controller classname이 들어간다.

#### Compliant Solution
@Api(tags="항공")

- tags : API Controller 큰 카테고리 역활을 한다. <br>
value 또는 description(지원x) 에 넣었던 내용은 tags 로 대신한다. value 값은 입력하지 않아도 자동으로 controller classname을 가져간다.


### @ApiVersion(1)


### @ApiOperation(value="예약조회", notes="예약내역을 조회한다.")

#### Compliant Solution
@ApiOperation(value="예약조회", notes="예약내역을 조회한다.")

- value : 메소드 간략한 설명(summary)
- notes : 디테일한 설명을 입력 할 수 있다.(description) 

### @ApiParam(required=true, value="예약번호", example="0")

#### Noncompliant Code Example
~~@ApiParam(required=true, name="conversationId", value="예약번호")~~
- name : 굳이 입력하지 않아도 자동으로 parameter name을 가져간다. 오타로 인한 오해 소지가 있어 입력 하지 않는다.  

#### Compliant Solution
@ApiParam(required=true, value="예약번호")

- required : 필수 param 인지 여부 
- value : parameter의 설명 (description 항목에 들어감)
- allowableValues : 입력할 수 있는 항목들을 Enum 형식으로 전달할 수 있다.
- defaultValue : 입력값이 없을 경우 기본 값을 입력
- example : swagger에서 "Try it out" 할 경우 자동으로 들어간다. **(int, long 같은 Number type 선언시 필수 입력)**

## Model

### @ApiModel(value="AirReservationReqVO", description="항공예약정보 조회용")

#### Noncompliant Code Example
~~@ApiModel(value="항공예약정보 조회용")~~

#### Compliant Solution
@ApiModel(value="AirReservationReqVO", description="항공예약정보 조회용")
- value : classname을 넣는 것을 관례로 한다. 다른 VO 에서 같은 value 값을 가질 경우 충돌하여 한쪽 class만 참조한다.
- description : 설명이 필요한 내용은 description에 입력한다.

내부 클래스 선언시 아래처럼 value 값을 입력해준다. 
@ApiModel(value="AirReservationReqVO.DateSearch", description="날짜 검색용")


### @ApiModelProperty(notes = "국가명", required = true, example = "인도")

#### Noncompliant Code Example
~~@ApiModelProperty(value = "국가명", required = true, example = "인도")~~
- value : request를 위한 용도가 아닌 경우 되도록 사용하지 않는다.

#### Compliant Solution
@ApiModelProperty(notes = "국가명", required = true, example = "인도")
- notes : parameter의 설명 (decription)
- required : 필수 여부
- example : Example value 노출 **(int, long 같은 Number type 선언시 필수 입력)**

request 용도로 사용할 경우 [@ApiParam](#-apiparam-required-true-value-)  attributes 를 참고한다.