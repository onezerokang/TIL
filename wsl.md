# 윈도우에서 WSL2 설치하기

일단 WSL을 사용하기 위해서는 Windows 10 버전 2004 이상 혹은 Windows 11을 사용하고 있어야 한다.

wsl이 컴퓨터에 깔려 있지 않다면 다음 명령어로 간단하게 설치할 수 있다.

```
wsl --install
```

이 명령은 자동으로 필요한 선택적 구성 요소를 사용하도록 설정하고, 최신 Linux 커널을 다운로드하고, WSL 2를 기본값으로 설정하고, Linux 배포판 (기본적으로 Ubuntu이며, 변경 방법은 아래 참조) 을 설치합니다
새로 설치된 Linux 배포판을 처음 시작하면 콘솔 창이 열리고 파일의 압축이 풀리고 머신에 저장될 때까지 기다리라는 메시지가 표시됩니다. 이후의 모든 시작은 1초도 걸리지 않습니다.

> 출처
> https://docs.microsoft.com/ko-kr/windows/wsl/install
> https://docs.microsoft.com/ko-kr/windows/wsl/setup/environment
