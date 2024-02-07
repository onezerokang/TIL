# Docker Compose로 로컬 개발 환경 관리하기

## 배경

현재 필자는 예약 도메인에서 발생할 수 있는 동시성 문제를 알아보고 해결하는 GrabTable 프로젝트를 진행하고 있다.

본격적인 비즈니스 로직 구현에 앞서, 프로젝트 세팅을 진행하는 데 로컬 개발 환경 설정 문제에 직면했다. MySQL 8.0을 설치하고 실행하는 과정에서 예전에 설치했던 MySQL 5.X 버전과 포트 충돌이 발생한 것이다.

MySQL 5.X을 종료하는 것으로 문제는 해결되었지만 로컬 개발 환경 세팅에 대한 몇 가지 불편함을 느꼈다.

1. **중복 프로그램에 대한 포트 관리**: 같은 프로그램을 여러 버전별로 설치했을 때 포트 충돌이 발생한다. 만약 두 버전을 모두 실행하고 싶을 때는 어떻게 해야 할까?
2. **비효율적인 수동 설치**: 로컬 환경은 프로덕션 환경과 최대한 일치해야 한다. 따라서 기존 프로젝트에 참여할 때는 해당 애플리케이션이 의존하는 프로그램의 버전을 알아보고 일일이 내 컴퓨터에 설치해야 한다. 이는 너무 번거로운 과정이다.

이러한 문제를 해결하기 위한 방법을 찾기 시작했고, Docker Compose를 활용하면 편리하게 로컬 개발 환경을 설정할 수 있다는 것을 알았다.

## Docker란

먼저 Docker가 무엇인지 간략하게 알아보자.

Docker는 프로그램을 쉽게 배포하고, 설치하기 위한 툴이다. Docker를 사용하면 한줄 명령어로 원하는 프로그램을 설치하고 실행할 수 있다.

Docker의 핵심 키워드는 이미지와 컨테이너이다. 각 키워드에 대해 간단하게 알아보자.

- **이미지(image)**: 프로그램을 실행하는 데 필요한 모든 것(코드, 라이브러리, 런타임 등)들을 포함하는 독립적이며 실행 가능한 소프트웨어 패키지
- **컨테이너(container)**: 가져온 이미지를 실행하는 가상 환경(이미지의 인스턴스)

Docker를 사용하기 위해서는 각 운영체제에 맞는 Docker를 설치해줘야 한다. 다음 사이트에서 Docker를 설치하자([https://www.docker.com/](https://www.docker.com/)).

MySQL 컨테이너를 실행하는 명령어는 다음과 같다.

```shell
# 포트와 버전을 지정할 수 있다.
docker run --name <name> -e MYSQL_ROOT_PASSWORD=<password> -d -p <port>:3306 mysql:<version>
```

docker run 명령어는 컨테이너를 실행시키는 데, 만약 해당 이미지가 없다면 docker hub에서 이미지를 가져온 후 실행시킨다.

컨테이너를 중지/삭제하는 명령어는 다음과 같다.

```shell
# 컨테이너 이름 대신 ID도 가능하다.
docker stop <container_name>

docker rm <container_name>
```

## Docker Compose란

Docker를 사용하여 포트를 다르게 설정했지만, 작업을 진행할 때마다 수동으로 컨테이너를 띄우고 내리는 작업은 매우 번거롭다. 지금은 MySQL만 사용하지만 사용하는 컨테이너가 늘어나면 더 번거로워질 것이다. 이런 문제를 해결할 수 있는 것이 바로 Docker Compose다.

Docker Compose는 Docker 컨테이너들을 어떻게 실행할지 정의하고 실행할 수 있는 툴이다. Docker Compose 설정 파일을 정의해두고 다음 명령어 한줄이면 정의된 컨테이너가 모두 실행된다.

```shell
# -d는 datach 모드로 도커 컨테이너를 백그라운드에서 실행되도록 한다.
docker-compose up -d
```

## Docker Compose로 MySQL 연동하기

이제 Spring Boot 프로젝트에 Docker Compose를 이용하여 MySQL을 연동해보자. 먼저 루트 디렉토리에 docker-compose.yml 파일을 작성한다.

```yml
version: "3.8"
services:
  mysql:
    image: mysql:8.0.33
    container_name: grab_table_mysql
    ports:
      - "3308:3306"
    environment:
      MYSQL_DATABASE: "grab_table"
      MYSQL_USER: "admin"
      MYSQL_PASSWORD: "1234"
      MYSQL_ROOT_PASSWORD: "1234"
      TZ: Asia/Seoul
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

각 속성에 대한 의미는 아래와 같다.

- **container_name**: 실행할 컨테이너 이름을 지정한다.
- **ports**: 첫번째 포트(3308)는 로컬 컴퓨터에서 컨테이너에 접근할 때 사용할 포트고, 두번째 포트(3306)는 컨테이너 내부에서 MySQL이 갖는 포트다. 첫번째 포트를 3308로 설정한 이유는, 기존 로컬 환경에 3306을 사용하는 MySQL이 있었기 때문이다.
- **command**: mysql 컨테이너를 실행할 때 추가로 입력할 명령어다. 위 파일에서는 한글과 이모티콘을 문제 없이 저장할 수 있도록 캐릭터셋 등을 설정했다.
- **volumes**: 데이터가 저장될 공간이다.

이제 application.yml에 MySQL 연결을 위한 정보를 넣어주자. MySQL 컨테이너의 포트는 docker-compose.yml 파일에서 3308로 설정되었으므로, application.yml 파일의 url에도 3308로 지정해야 한다.

```yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3308/spring_lab
    username: admin
    password: 1234
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      show_sql: true
      format_sql: true
```

이제 다음 명령어를 실행하면 MySQL 컨테이너가 실행될 것이다.

```shell
docker-compose up -d
```

이렇게 Docker Compose를 이용한 로컬 개발 환경을 설정을 마쳤다. 마지막으로 Docker Compose를 활용한 로컬 환경 관리의 장점을 정리하며 글을 마무리 하겠다.

1. 한번에 필요한 컨테이너를 모두 띄울 수 있다.
2. 프로젝트에 참여하는 모두가 같은 버전으로 개발 환경을 설정 할 수 있다.

## 참조

- [Docker Compose 로 local 개발 환경 쉽게 관리하기](https://blog.gangnamunni.com/post/docker-compose-for-local-env/)
- [docker-compose를 이용하여 로컬 개발환경 구성하기(Part1)](https://dev.gmarket.com/72)
- [따라하며 배우는 도커와 CI환경](https://www.inflearn.com/course/%EB%94%B0%EB%9D%BC%ED%95%98%EB%A9%B0-%EB%B0%B0%EC%9A%B0%EB%8A%94-%EB%8F%84%EC%BB%A4-ci)
