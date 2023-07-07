# 파이썬과 다른 C언어 특성들

파이썬과 다른 C언어 특성들에 대해 공부한 내용을 정리하였다.

## 선언(declaration)과 정의(definition)의 개념 (.h파일, .c파일)

- 선언
  - 변수나 함수가 파일에서 사용 되고 있다는 것을 컴파일러에게 알린다.
  - 아직 값을 변수나 함수에 값을 정의하지 않았기 때문에 메모리를 사용하지 않는다.
- 정의

  - 실제 메모리에 데이터를 저장한다.

- 헤더 파일

```c
#include <stdio.h>

int main() {
    int num; // 컴파일러에게 num 변수에 int 데이터를 저장할 것을 알려준다.
    num = 10; // 정수형 10 데이터를 정의했다.
    printf("num: %d \n", num);

    return 0;
}
```

## 전방선언(forward declaration)

변수나 함수를 정의하기 전에 선언하는 것이다.
함수의 경우 함수의 원형(prototype)을 전방선언함으로써 컴파일러에게 해당 파일에 함수가 존재한다는 것을 알리고
컴파일러는 함수를 호출하는 코드를 만났을 때 함수가 정의 되어있지 않더라도 에러를 발생시키지 않는다.

```c
#include <stdio.h>

int sum(int x, int y); // 함수의 원형은 리턴 값, 함수명, 매개변수로 선언한다.

int main() {
    int a = 10;
    int b = 20;

    result = sum(a, b);
    printf("%d \n", result);

    return 0;
}

// 함수를 정의한다.
int sum(int x, int y) {
    return x + y;
}
```

main 함수 위쪽에 함수를 정의하면 전방선언을 하지 않아도 된다.
하지만 해당 방식은 함수가 많고 복잡해질 경우 함수의 호출 순서를 파악하기 어려워진다는 단점이 있다.
때문에 많은 프로그래머가 함수의 원형을 전방선언하여 가독성을 높이는 방법을 선호한다.

## static, extern의 개념

- static
  - 지역 변수에 사용할 경우 함수가 종료 되더라도 해당 변수를 파괴하지 않는다. 이를 이용해 함수의 호출 순서를 카운트 하는 등의 작업을 할 수 있다.
  - 전역 변수에 사용할 경우 해당 변수는 해당 파일에서만 사용가능한 private variable이 된다.
- extern
  - 외부 파일의 함수나 변수를 가져와 사용한다.

## enum, union 개념

- enum
  - enum, 한국어로는 열거형이라고 불리는 것은 비슷한 상수의 집합을 정의한다.
  - 상수는 정수와 매칭된다. 코드의 가독성을 높일 수 있다.

```c
#include <stdio.h>

enum Role {
    ADMIN,
    BASIC,
    VIP,
};

int main() {
    enum Role user = BASIC;
    printf("user: %d \n", user); // 1

    switch(user) {
        case ADMIN:
            printf("관리자 계정입니다.");
            break;
        case BASIC:
            printf("일반 계정입니다.");
            break;
        case VIP:
            printf("VIP 계정입니다.");
            break;
    }

}
```

- union
  - struct 같이 여러 타입의 멤버를 사용하는 새로운 타입을 정의할 수 있다.
  - union과 struct의 차이점은 union의 경우 모든 멤버가 같은 메모리 주소를 사용하기 때문에 하나의 멤버만을 사용할 수 있다.
  - union의 메모리 크기는 멤버의 타입 중 가장 큰 데이터 타입의 크기다.
  - 가장 마지막에 정의한 멤버가 기존 데이터를 덮어쓴다.

```c
#include <stdio.h>
#include <string.h>

union Data {
    char c;
    int i;
    char str[20];
};

int main() {
    union Data data;
    printf("size: %d \n", sizeof(data));

    data.c = 'a';
    data.i = 827;
    strcpy(data.str, "Hello, World!");

    // 마지막에 설정한 data.str의 값으로 overwrite 되었다.
    printf("data.i : %d\n", data.i);
    printf("data.c : %f\n", data.c);
    printf("data.str : %s\n", data.str);

    return 0;
}

```

## 컴파일과 링크를 통해 실행파일이 어떻게 만들어 지는가

컴파일은 C언어 코드를 기계가 이해할 수 있는 실행파일로 만드는 작업이다. 다음은 컴파일의 과정이다.

1. 전처리
   - 전처리기가 전처리 명령어의 지시문을 따라 코드를 변형한다.
2. 컴파일
   - 소스 코드를 어셈블리어로 변경한 목표파일(object file)을 생성한다.
3. 링크
   - 여러 목표파일과 라이브러리를 연결하여 하나의 실행 파일을 생성한다.

## 포인터

포인터는 데이터의 주소값을 저장하는 변수다.

## malloc, free

프로그램이 실행될 때 운영체제로 부터 메모리를 할당 받아 프로그램이 메모리에 로드된다.
메모리는 코드 영역, 데이터 영역, 스택 영역, 힙 영역으로 나뉜다.

힙 영역은 런타임 때 사용자가 메모리를 할당하고 해제할 수 있는 영역인데 malloc() 함수와 free() 함수로 동적 할당, 해제를 할 수 있다.

- malloc의 원형

```c
#include <stdlib.h>

void *malloc(size t);
```

메모리를 동적으로 할당한 후 더 이상 사용하지 않는다면 해제해야 한다. 안그러면 메모리 누수가 발생한다.

- free의 원형

```c
#include <stdlib.h>

void free(void *ptr, size t);
```

## 배열의 개념 (배열도 포인터와 유사한 개념으로 이해하는 게 도움됩니다.)

배열은 같은 타입의 데이터를 메모리에 연속되게 저장하는 자료구조다.
다음은 배열의 사용법을 확인할 수 있는 예시 코드다.

```c
#include <stdio.h>

int main() {
    int arr[10]
    int char[10]
}
```

배열의 이름은 컴파일 시 첫번째 요소의 메모리 주소로 치환된다.
따라서 다음과 같은 사용이 가능하다.

```c
#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int i;

    for (i = 0; i < 5; i++) {
        printf("%d 번쨰 원소: %d", i, arr[i]);
        printf("%d 번쨰 원소: %d", i, *(ptr + i));
    }
}
```

## Call By Value, Call By Reference의 개념

- call by value
  - 함수에 인자를 넘길 때 값으로 넘긴다.
  - 넘긴 인자의 값이 매개변수로 복사된다.
  - 함수 내에서 인자의 값에 어떤 작업을 하더라도 원본 변수에 영향을 주지 않는다.
- call by reference
  - 함수에 인자를 넘길 때 변수의 메모리 주소를 넘긴다.
  - 함수 내에서 메모리 주소에 접근할 수 있기 때문에 원본 변수의 값에 영향을 준다.

다음은 call by value와 call by reference의 차이를 보여주는 코드이다.

```c
#include <stdio.h>

void CallByValue(int num) {
    num++;
}

void CallByReference(int *ptr_num) {
    *ptr_num++;
}

int main() {
    int num = 1;

    CallByValue(num);
    printf("%d \n", num); // 1

    CallByReference(num);
    printf("%d \n", num); // 2
}
```

## 가변인자 (va_start, va_end)

함수의 매개변수 개수가 불확실 할 때 가변인자를 사용할 수 있다.

## 전처리 명령어(#define, #include, #typedef 등등)

전처리 명령어란 컴파일 전 전처리기에 의해 실행되는 명령이다.

다음은 전처리 명령어의 종류이다.

- `#include`: 외부에 선언된 함수나 상수를 사용하기 위해, 외부 파일을 현재 파일에 포함할 때 사용한다.
- `#define`: 함수나 상수를 단순화해주는 매크로를 정의할 때 사용한다.
- `#undef`: #define으로 정의된 매크로를 삭제할 때 사용한다.
- `#error`: 오류를 출력하고, 컴파일 과정을 중단한다.
- `#pragma`: 운영체제별로 달라지는 지시사항을 컴파일러에 전달한다.
- `#typedef`: 기존 데이터 타입에 새로운 이름을 지정한다(주로 struct에 사용한다).
- `#if`,`#ifdef`,`#ifndef`,`#elif`,`#else`,`#endlif`: 조건부 컴파일 지시자

## bit 연산자

bit 연산자는 ~~~ 이다. 다음은 bit 연산자의 종류이다.

- &
- |
- ^
- ~
- <<, >>
