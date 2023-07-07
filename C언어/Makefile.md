# Makefile

컴파일 할 소스코드가 많아지면 gcc 방식으로 하나하나 입력하는 것은 번거로운 일이다.
이런 문제를 해결할 때 make와 Makefile을 이용하게 된다.
make 명령어를 실행하면 Makefile을 읽어 매크로를 수행한다.

## Makefile 작성법

Makefile을 작성할 때는 다음과 같은 형식을 이룬다.

```
${macro}

${target} : ${dependency}
    ${command}
```

- target: 명령을 수행하고 결과를 저장할 파일
- dependency: 목적 파일을 만들기 위한 재료 파일들
- command: 실행 되어야 할 명령어들
- macro: 코드 단순화에 이용

다음은 Makefile의 예시이다.

```makefile
app : file1.o file2.o main.o
    gcc -o app file1.o file2.o main.o

file1.o : file1.c
    app -c -o file1.o file1.c

file2.o : file2.c
    app -c -o file2.o file2.c

main.o : main.c
    app -c -o main.o main.c

clean :
    rm *.o app
```

이후 make 명령어를 입력하면 app, file1.o file2.o main.o 파일이 생성된 것을 확인할 수 있다.

## 매크로로 Makefile 개선하기

매크로를 사용하면 위에 작성된 Makefile의 중복을 개선할 수 있다. 매크로는 다음과 같은 규칙을 준수하며 작성한다.

- 매크로의 정의는 사용되는 곳보다 항상 잉전에 정의되어야 한다.
- 정의된 매크로를 사용할 때는 $()에서 괄호 안에 매크로 이름을 넣어 사용한다.

다음은 매크로를 사용하여 개선한 Makefile이다.

```makefile
CC = gcc
CFLAGS = -W -WALL
TARGET = app
OBJECTS = file1.o file2.o main.o

all : $(TARGET)

$(TARGET) : $(OBJECTS)
    $(CC) $(CFLAGS) -o $@ $^

clean :
    rm *.o app
```

- CC: 컴파일러
- CFLAGS: 컴파일 옵션
- LDFLAGS: 링크 시 옵션(라이브러리)를 줄 수 있다.
- TARGET: 목적 파일
- OBJECTS: 의존 파일들
- $@: 현재 타겟의 이름을 나타내는 매크로
- $^: 현재 타겟이 의존하는 모든 종속 파일을 나타내는 매크로

## 참조

- [make와 Makefile의 필요성](https://bigpel66.oopy.io/library/c/chewing-c/2)
- [[c언어] make, Makefile 이해하기](https://losskatsu.github.io/programming/c-make/)
