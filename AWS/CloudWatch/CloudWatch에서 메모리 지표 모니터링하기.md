# CloudWatch에서 메모리 지표 모니터링하기

오늘 작업중인 서버가 터져서 원인을 파악하려고 CloudWatch에서 메모리 사용지표를 확인해보려 했다.
하지만 기본적으로 EC2는 메모리, 디스크 사용 지표를 CloudWatch에 보내지 않았다.

CloudWatch에서 메모리 사용 지표를 확인하기 위한 방법은 다음과 같다.

1. CloudWatchAgentServerPolicy 정책이 연결된 IAM 역할을 생성하고 EC2에 부여
2. EC2에 CloudWatch agent 설치
3. CloudWatch agent 구성 파일 작성(메모리 지표를 보내도록)
4. CloudWatch 재시작

이후에는 CloudWatch에서 메모리 사용 지표를 확인할 수 있게 된다.

더 자세한 내용은 나의 블로그에 따로 작성해뒀다.

[[RoadMaker] 인스턴스 연결성 검사 실패 해결 + 메모리 지표 모니터링하기](https://techpedia.tistory.com/)
