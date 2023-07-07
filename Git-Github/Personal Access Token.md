# Personal Access Token

2021년 8월 13일부터 깃헙에서 Git 작업 진행시 더 이상 계정 비밀번호를 이용할 수 없다.
대신 개인용 접근 토큰(Personal Access Token, 이하 PAT)을 만들어 사용해야 한다.

## 생성 방법

1. Github 로그인
2. Settings > Developer settings > Personal access tokens
3. 토큰 정보, 유효기간, 접근 범위 설정 후 토큰 생성
4. 생성된 토큰은 페이지를 벗어나면 다시 확인할 수 없으므로 안전한 곳에 보관

## GCM

PAT를 생성하면 두가지 문제에 대해 생각해보게 된다.

1. PAT를 어디에 저장할 것인가
2. Github 작업을 할 때마다 username과 PAT를 입력하는 것이 번거롭다

**GCM(git credential manager)**를 사용하면 위 두가지 문제를 해결하는데 도움이 된다.
GCM은 Git 클라이언트에서 PAT를 안전하게 저장하고 검색하기 위한 방법이다.

## 출처

- [Git에서 GitHub 자격 증명 캐싱](https://docs.github.com/ko/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
