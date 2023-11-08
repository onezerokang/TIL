# JSP 기초 사용법

## 1. JSP란

> JSP(JavaServer Pages)는 동적 페이지를 작성하는데 사용되는 자바의 표준 기술로서 HTML 응답을 생성하는데 필요한 기능을 제공하고 있다.

## 2. JSP에서 HTML을 생성하는 기본 구조

HTML 문서를 생성하는 JSP 코드는 크게 **설정 부분**과 **응답 생성 부분**으로 구성된다.

```jsp
<!-- JSP 페이지에 대한 설정 정보  -->
<%@ page contentType = "text/html; charset=utf-8" %>
<!-- HTML 코드 및 JSP 스크립트 -->
<html>
<head>
  <title>HTML 문서 제목</title>
</head>
<body>
<!-- scriptlet -->
<%
  String bookTitle = "JSP 프로그래밍";
  String author = "최범균";
%>
<!-- expression -->
<b><%= bookTitle %></b>(<%= author%>)입니다.
</body>
</html>
```

## 3. JSP 페이지의 구성 요소

- **디렉티브(Directive)**: JSP 페이지에 대한 정보를 설정할 때 사용된다.
- **스트립트(script)**:
  - **스크립트릿(Scriptlet)**: 자바 코드를 작성할 수 있는 부분이다.
  - **표현식(Expression)**: 변수, 숫자, 문자열, 함수 같이 값을 출력할 수 있다.
  - **선언부(Declaration)**: 메서드를 선언함
- **표현 언어(Expression Language)**:
- **기본 객체(Implicit Object)** JSP에서 제공되는 객체로 request, response, session 등
- **정적인 데이터**
- **표준 액션 태그(Action Tag)**: JSP에서 제공하는 태그로, 이를 활용하여 JSP를 보다 편리하게 사용할 수 있다.
- **커스텀 태그(Custom Tag)와 표준 태그 라이브러리(JSTL)**: 커스텀 태그란 개발자가 개발한 태그이며, JSTL은 자주사용되는 커스텀 태그들을 모아둔 라이브러리다.

### 3.1. 디렉티브

JSP 페이지에 대한 설정 정보를 지정할 때 사용된다.

- 구문

```jsp
<%@ 디렉티브이름 속성1="값1" 속성2="값2" ... %>
```

- 예시

```jsp
<%@ page contentType = "text/html; charset=utf-8" %>
```

위 코드의 디렉티브 이름은 page가 되고, contentType이라는 속성을 사용했으며, contentType 속성의 값은 text/html; charset=utf-8가 된다.

다음은 JSP가 제공하는 디렉티브다.

- page: JSP 페이지에 대한 정보 저장. 문서의 타입, 출력 버퍼의 크기, 에러페이지 등
- taglib: JSP 페이지에서 사용할 태그 라이브러리를 지정한다.
- include: JSP 페이지의 특정 영역에 다른 문서를 포함한다.

### 3.2. 스크립트 요소

스크립트 요소는 JSP 문서의 내용을 동적으로 생성하기 위해 사용된다.

JSP의 스크립트 요소는 다음과 같이 세 가지가 있다.

- **표현식(Expression)**: 값을 출력한다.
- **스크립트릿(Scriptlet)**: 자바 코드를 실행한다.
- **선언부(Declaration)**: 자바 메서드를 만든다.

### 3.3. 기본 객체

JSP는 웹 애플리케이션 프로그래밍을 하는 데 필요한 기능을 제공해주는 기본 객체(implicit object) 제공한다. request, response, session, application, page 등 다수의 기본 객체가 존재한다.

### 3.4 표현 언어

JSP의 스크립트 요소는 자바 문법을 그대로 사용할 수 있기에, 자바 언어의 특징을 그대로 사용할 수 있다는 장점이 있다. 하지만 스크립트 요소를 사용하면 JSP 코드가 다소 복잡해진다.

```jsp
<%
  int a = Integer.parseInt(request.getParameter("a"));
  int b = Integer.parseInt(request.getParameter("b"));
%>
a * b = <%= a * b %>
```

위 코드를 표현 언어(expression language)로 작성하면 다음과 같이 간결해진다.

```jsp
a * b = ${param.a * param.b}
```

표현 언어는 '%{'와 '}' 사이에 정해진 문법을 따르는 식을 입력한다. 스크립트 코드를 사용하는 것보다 표현 언어를 사용하는 것이 간단하기에 특별한 이유가 없는 한 표현 언어를 주로 사용한다.

### 3.5 표준 액션 태그와 태그 라이브러리

액션 태그는 <jsp:액션태그이름>의 형태를 띄며, 이를 활용하여 JSP를 보다 편리하게 사용할 수 있다.

커스텀 태그는 개발자가 직접 개발한 태그다. 일반적으로 JSP 코드에서는 중복을 모듈화하거나 스크립트 코드를 사용할 때 발생하는 소스 코드의 복잡함을 없애기 위해 커스텀 태그를 사용한다.

커스텀 태그 중 자주 사용하는 것들을 별도로 표준화한 태그 라이브러리가 있는데 이를 JSTL(JavaServer Pages Tab Library)이다. JSTL은 조건문, 반복문 등을 커스텀 태그를 이용해서 구현할 수 있도록 해준다.

## page 디렉티브

page 디렉티브는 JSP 페이지에 대한 정보를 입력하기 위해 사용된다. 이를 통해 JSP 페이지가 어떤 문서를 생성하는지, 어떤 자바 클래스를 사용하는지, 세션에 참여하는지, 출력 버퍼의 존재 여부와 같이 JSP 페이지를 실행하는데 필요한 정보를 입력할 수 있다.

- 예시

```jsp
<%@ page contentType = "text/html; charset=utf-8" %>
<%@ page import="java.util.Date" %>
```

- **page 디렉티브의 주요 속성**:
  - **contentType**:
  - **import**:
  - **session**:
  - **buffer**:
  - **autoFlush**:
  - **info**:
  - **errorPage**:
  - **isErrorPage**:
  - **pageEncoding**:
  - **isELIgnored**:
  - **deferredSyntaxAllowedAsLiteral**:
  - **trimDirectiveWhitespaces**:

### contentType 속성과 캐릭터 셋

page 디렉티브의 contentType 속성은 JSP가 생성할 문서의 MIME 타입과 캐릭터 셋을 입력한다. JSP에서 주로 사용하는 MIME 타입은 "text/html"이고 필요에 따라 "text/xml", "application/json" 등을 사용하기도 한다.

> MIME은 Multipurpose Internet Mail Extensions의 약자로서 이메일의 내용을 설명하기 위해 정의되었다. 하지만 메일뿐만 아니라 HTTP 등의 프로토콜에서도 응답 데이터의 내용을 설명하기 위해 MIME을 사용하고 있다.

### import 속성

JSP는 페이지 디렉티브의 import 속성을 사용해서 JSP 코드에서 자바 클래스를 사용할 수 있다.

```jsp
<!-- import 속성 사용 방법 -->
<%@ page import = "java.util.Calendar" %>
<%@ page import = "java.util.Date" %>

<!-- 여러 타입 지정하기 -->
<%@ page import = "java.util.Calendar, java.util.Date" %>
```

### trimDirectiveWhitespaces 속성을 이용한 공백 처리

JSP 2.1부터 page 디렉티브에 추가된 trimDirectiveWhitespaces 속성을 사용하면 불필요하게 생성되는 줄바꿈 공백 문자를 제거할 수 있다. 해당 속성을 true로 지정하면 디렉티브나 스크립트 코드 위치에서 발생하는 줄바꿈 공백 문자를 제거해준다.

### JSP 페이지의 인코딩과 pageEncoding 속성

톰캣 같은 컨테이너는 JSP 코드를 분석하는 과정에서 어떤 인코딩을 이용해서 코드를 작성했는지 검사하며, 그 결과로 선택한 캐릭터 셋을 이용해서 JSP 페이지의 문자를 읽어오게 된다.

웹 컨테이너가 JSP 페이지를 읽어올 때 사용할 캐릭터 셋을 결정하는 기본 과정은 다음과 같다.

1. 파일이 BOM으로 시작하지 않을 경우

- 기본 인코딩을 이용해서 파일을 처음부터 읽고, page 디렉티브의 pageEncoding 속성을 검색한다. 단, pageEncoding 속성을 찾기 이전에 ASCII 문자 이외의 글자가 포함되어 있지 않은 경우에만 적용된다.
- pageEncoding 속성이 값을 갖고 있다면, contentType 속성을 검색한다. contentType 속성이 존재하고 charset을 이용해서 캐릭터 셋을 지정했다면, 파일을 읽어올 때 사용할 캐릭터 셋으로 charset에 지정ㅇ한 값을 사용한다. 단, contentType 속성을 찾기 이전에 ASCII 문자 이외의 글자가 포함되어 있지 않은 경우에만 적용된다.
- 모두 해당되지 않을 경우 ISO-8859-1을 캐릭터 셋으로 사용한다.

2. 파일이 BOM으로 시작할 경우

- BOM을 이용해서 결정된 인코딩을 이용하여 파일을 읽고, page 디렉티비의 pageEncoding 속성을 검색한다.
- 만약 pageEncoding 속성의 값과 BOM을 이용해서 결정된 인코딩이 다르면 에러를 발생시킨다.

3. 1 또는 2 과정을 통해 설정된 캐릭터 셋을 이용해서 JSP 소스 코드를 읽는다.

위 과정을 보면 JSP 파일을 읽을 때는 page 디렉티브의 pageEncoding 속성과 contentType 속성을 사용해서 캐릭터 인코딩을 결정한다는 것을 알 수 있다.

> BOM: Byte Order Mark의 약자로 UTF-8, UTF-16, UTF-32와 같은 유니코드 인코딩에서 바이틔 순서가 리틀 엔디언인지 빅 엔디언인지 여부를 알려주는 16비트 값이다.

해당 내용 다시 읽어보자

## 스크립트 요소

JSP의 스크립트 요소는 다음 세가지가 있다.

- 스크립트릿(Scriptlet)
- 표현식(Expression)
- 선언부(Declaration)

### 스크립트릿

스크립트릿은 JSP 페이지에서 자바 코드를 실행할 때 사용하는 코드 블록이다.

스크립트릿의 구문은 다음과 같다.

```
<%
  ... 실행할 자바 코드
%>
```

다음은 1부터 10까지의 합을 구하는 JSP 페이지다.

```jsp
<%@ page contentType="text/html;charset=utf-8" %>
<html>
<head><title>1~10까지의 합</title></head>
<body>
<%
  int sum = 0;
  for(int i = 1; i <= 10; i++) {
    sum += i;
  }
%>
1부터 10까지의 합은 <%= sum%>입니다.
</body>
</html>
```

### 표현식

표현식은 어떤 값을 출력 결과에 포함시키고자 할 때 사용된다.

표현식의 구문은 다음과 같다.

```
<%= 값 %>
```

표현식읜 값 부분에는 변수나, 문자열, 숫자 등이 들어올 수 있다.

### 선언부

JSP 페이지의 스크립트릿이나 표현식에서 사용할 수 있는 메서드를 작성할 때는 선언부를 사용한다. 선언부에서 정의한 메서드는 스크립트릿과 표현식에서 사용할 수 있다.

선언부는 다음과 같은 문법 구조를 갖는다.

```jsp
<%!
  public 리턴타입 메서드이름(파라미터목록) {
    자바코드1;
    자바코드2;
    return 값;
  }
%>
```

다음은 선언부를 사용하여 두 정수의 합을 계산해주는 예시 코드다.

```jsp
<%@ page contentType="text/html; charset=utf-8" %>
<%!
  public int plus(int a, int b) {
    return a + b;
  }
%>
<html>
<head><title>선언부를 사용한 두 정수의 합</title></head>
<body>
10 + 25 = <%= plus(10, 25)%>
</body>
</html>
```

## request 기본 객체

request 기본 객체는 웹 브라우저가 전송한 요청 정보를 제공하는 객체다.

request 기본 객체가 제공하는 기능은 다음과 같이 구분된다.

- 클라이언트와 관련된 정보 읽기 기능
- 서버와 관련된 정보 읽기 기능
- 클라이언트가 전송한 요청 파라미터 읽기 기능
- 클라이언트가 전송한 요청 헤더 읽기 기능
- 클라이언트가 전송한 쿠키 읽기 기능
- 속성 처리 기능

### 클라이언트 정보 및 서버 정보 읽기

다음은 request 객체에서 제공하는 클라이언트의 정보와 서버 정보를 구할 수 있는 메소드다.

- **getRemoteAddr()**: 클라이언트의 IP 주소를 리턴한다.
- **getContentLength()**: 클라이언트가 전송한 요청 정보의 길이를 리턴한다.
- **getCharacterEncoding()**: 클라이언트가 요청 정보를 전송할 때 사용한 캐릭터의 인코딩을 리턴한다.
- **getContentType()**: 클라이언트가 요청 정보를 전송할 때 사용한 컨텐츠 타입을 리턴한다.
- **getProtocol()**: 클라이언트가 요청한 프로토콜을 구한다.
- **getMethod()**: 웹 브라우저가 정보를 전송할 때 사용한 방식을 구한다.
- **getRequestURI()**: 웹 브라우저가 요청한 URL에서 경로를 구한다.
- **getContextPath()**: JSP 페이지가 속한 웹 어플리케이션의 컨텍스트 경로를 구한다.
- **getServerName()**: 연결할 때 사용한 서버 이름을 구한다.
- **getServerPort()**: 서버가 실행중인 포트 번호를 구한다.

### 요청 파라미터 처리

다음 HTML 폼을 보자.

```jsp
<form action="/chap03/viewParameter.jsp" method="post">
  이름: <input type="text" name="name" size="10" /> <br />
  주소: <input type="text" name="address" size="30" /> <br />
  좋아하는 동물:
  <input type="checkbox" name="pet" value="dog" /> 강아지
  <input type="checkbox" name="pet" value="cat" /> 고양이
  <input type="checkbox" name="pet" value="pig" /> 돼지
  <br />
  <input type="submit" value="전송" />
</form>
```

위 폼에서 내용을 입력하고 전송 버튼을 클릭하면, 파라미터이름=값 형태로 서버에 전송되는데, request 객체의 메서드를 통해 받을 수 있다.

- **getParameter(String name)**: 이름이 name인 파라미터의 값을 구한다.
- **getParameterValues(String name)**: 이름이 name인 모든 파라미터의 값을 배열로 구한다.
- **getParameterNames()**: 웹 브라우저가 전송한 파라미터 이름 목록을 구한다.
- **getParameterMap()**: 웹 브라우저가 전송한 파라미터의 맵을 구한다.

### GET 방식 전송과 POST 방식 전송

웹 브라우저는 GET 방식과 POST 방식의 두 가지 방식 중 한 가지를 사용해서 파라미터를 전송한다. 두 방식의 차이점은 전송 방식인데, GET 방식은 요청 URL에 파라미터 값을 붙여서 전송한다(query string). 반면 POST 방식은 데이터 영역을 이용해서 데이터를 전송한다.

### 요청 파라미터 인코딩

웹 브라우저는 웹 서버에 파라미터를 전송할 때 알맞은 캐릭터 셋을 이용해서 파라미터 값을 인코딩한다. 반대로 웹 서버는 알맞은 캐릭터 셋을 이용해서 웹 브라우저가 전송한 파라미터 데이터를 디코딩한다.

어떤 캐릭터 셋을 사용할지의 여부는 GET 방식과 POST 방식에 따라 달라진다.

## response 기본 객체

response 기본 객체는 클라이언트에게 보내는 응답 정보를 담는다.

response 기본 객체가 응답 정보와 관련해서 제공하는 기능은 다음과 같다.

- 헤더 정보 입력
- 리다이렉트 하기

### 웹 브라우저에 헤더 정보 전송하기

- addDateHeader(String name, long date)
- addHeader(String name, String value)
- addIntHeader(String name, int value)
- setDateHeader(String name, long date)
- setHeader(String name, String value)
- setIntHeader(String name, int value)
- containsHeader(String name)

응답 헤더를 직접 설정해야 하는 경우가 많진 않은데, 그중 하나는 캐시와 관련된 것이다.

### 웹 브라우저 캐시 제어를 위한 응답 헤더 입력

JSP를 비롯한 웹 어플리케이션을 개발하다보면 새로운 내용을 DB에 추가했는데도 웹 브라우저에 출력되는 내용이 바뀌지 않는 경우가 있다. 이는 웹 브라우저가 서버가 생성한 결과를 출력하지 않고 캐시에 저장된 데이터를 출력하기 때문이다.

내용이 자주 바뀌지 않는 사이트는 웹 브라우저 캐시를 사용해서 보다 빠른 응답을 제공할 수 있다. 하지만, 게시판처럼 내용이 자주 변경되는 사이트는 웹 브라우저 캐시가 적용되면 변경된 내용을 확인할 수 없게 된다.

HTTP는 응답 헤더를 ㄹ통해 웹 브라우저가 응답 결과를 캐시할지에 대한 여부를 설정할 수 있다.

- Cache-Control: 이 헤더의 값을 no-cache로 지정 시 응답 결과를 캐시하지 않는다.
- Pragma: no-cache로 지정하면 ㄴ웹 브라우저는 응답 결과를 캐시에 저장하지 않는다.
- Expires: 응답 결과의 만료일을 지정한다.

Cache-Control은 HTTP 1.1 버전에서만 유효하기에 Pragma 또한 no-cache로 설정해주자.

```jsp
<%
  response.setHeader("Cache-Control", "no-cache");
  response.addHeader("Cache-Control", "no-store");
  response.setHeader("Pragma", "no-cache");
  response.setDateHeader("Expires", 1L);
%>
```

### 리다이렉트를 이용해서 페이지 이동하기

리다이렉트란 웹 서버가 웹 브라우저에게 다른 페이지로 이동하라고 응답하는 기능이다.

- response.sendRedirect(String location)

웹 서버에 전송할 파라미터 값은 알맞게 인코딩해야 한다. java.net.URLEncoder 클래스를 사용해 문자열을 인코딩해주자.

## 참조

- 최범균의 JSP 2.3 웹 프로그래밍 : 기초부터 중급까지, 최범균, CHAPTER 03 JSP로 시작하는 웹 프로그래밍
