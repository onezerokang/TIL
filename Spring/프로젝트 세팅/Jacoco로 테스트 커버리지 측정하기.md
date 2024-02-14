# Jacoco와 GitHub Actions로 테스트 커버리지 미달 시 main 브랜치 병합 차단하기

## 테스트 코드는 왜 필요할까?

테스트 코드는 소프트웨어가 의도한 대로 동작하는지 검증하여, **소프트웨어의 안정성을 보장하는 필수 요소이다**. 테스트 코드 없이 기능 개발을 진행하면, 단기적으로는 작업 속도가 빠르게 느껴질 수 있지만, 서비스가 복잡해지기 시작하면, 개발한 코드가 서비스에 문제를 일으키지 않을까 하는 불안감에 시달리게 될 것이다(경험담).

그럼에도 불구하고, 테스트 코드 작성은 번거롭기에, 마감일이 다가올수록 이를 미루게 된다. 이러한 상황에서 테스트 커버리지 측정은 큰 도움이 된다.

## 테스트 커버리지란?

테스트 커버리지는 코드가 얼마나 테스트되고 있는지를 나타내는 지표로, 이 지표가 설정한 목표에 도달하지 않으면 빌드 및 배포를 할 수 없도록 하는 것이 일반적이다.

이번 포스트에서는 **Jacoco(Java Code Coverage)**를 이용해 테스트 커버리지를 측정하고, 목표한 커버리지 수치에 도달하지 못할 경우 코드를 main 브랜치에 merge할 수 없도록 하는 방법을 알아보겠다.

## Jacoco

### Jacoco 플러그인 등록

Jacoco는 테스트 커버리지를 측정해주는 툴이다. Jacoco를 사용하기 위해서는 build.gradle에 **jacoco plugin**을 등록해줘야 한다.

```groovy
plugins {
	id 'java'
	id 'org.springframework.boot' version '3.2.2'
	id 'io.spring.dependency-management' version '1.1.4'
	id 'org.asciidoctor.jvm.convert' version '3.3.2'
    // jacoco 플러그인 등록
	id 'jacoco'
}

// 사용할 버전 명시
jacoco {
	toolVersion = "0.8.9"
}
```

### jacocoTestReport

테스트 커버리지를 측정하고, 측정한 결과를 리포트로 뽑아주려면 **jacocoTestReport** 태스크를 등록해줘야 한다.

```groovy
// test 태스크가 종료될 때, jacocoTestRport 태스크를 수행하도록 한다.
test {
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    // jacocoTestReport가 수행되기전에 test 태스크를 수행하도록 한다.
	dependsOn 'test'

	reports {
        // report를 어떤 포맷으로 생성할지에 대한 설정
		xml.required = true
		csv.required = true
		html.required = true
	}

    // 측정하지 않을 파일을 지정한다.
	afterEvaluate {
		classDirectories.setFrom(files(classDirectories.files.collect {
			fileTree(dir: it, exclude: [
					'**/*Application*',
			])
		}))
	}
}
```

한번 테스트 커버리지를 측정하고, 리포트를 확인해보자.

```shell
gradle test
```

만약 리포트가 생성될 경로를 따로 지정하지 않았다면 **build/reports/jacoco/test** 안에 리포트가 생성된다.

_이미지 첨부_

html 리포트를 브라우저에서 열면 다음과 같이 테스트 커버리지 측정 결과를 확인할 수 있다.

_이미지 첨부_

### jacocoTestCoverageVerification

만약 목표한 커버리지에 미달했을 때 빌드를 실패시키고 싶다면 **jacocoTestCoverageVerification** 태스크를 등록한다.

필자는 코드 커버리지 목표를 브랜치 커버리지를 90%, 라인 커버리지를 80%로 설정했다.

만약, 테스트 코드가 없는 프로젝트에 테스트 코드를 적용하고 싶은 경우에는, 이 수치를 낮게 잡은 후 조금씩 올려가면 된다.

```groovy
jacocoTestCoverageVerification {
	violationRules {
		rule {
			element = 'CLASS'

			limit {
				counter = 'BRANCH'
				value = 'COVEREDRATIO'
				minimum = 0.90
			}

			limit {
				counter = 'LINE'
				value = 'COVEREDRATIO'
				minimum = 0.80
			}
			// 커버리지 측정을 제외할 클래스
			excludes = [
					'*.*Application',
			]
		}
	}
}
```

jacocoTestReport 태스크가 종료될 때 jacocoTestCoverageVerification 태스크를 수행하도록 설정해주자.

```groovy
jacocoTestReport {
	dependsOn 'test'
    finalizedBy 'jacocoTestCoverageVerification'
	// ... 생략
}
```

build 태스크에는 test 태스크가 포함되어있기에 빌드를 수행했을 때 테스트 커버리지 수치에 도달하지 못하면 빌드가 실패한다.

```shell
gradle build
```

_실패 화면_

## Github Actions로 CI 구성하기

Github Actions는 특정 이벤트 발생 시 정의된 작업을 자동으로 수행한다. 이 기능을 활용하여 코드 변경 시 자동화된 빌드, 테스트 및 배포 과정을 설정할 수 있다.

루트 디렉토리에 **.github/workflows** 디렉토리를 생성하고, 이 안에 **ci.yml** 파일을 작성하여 CI를 설정해보자.

```yml
name: Java CI with Gradle

# 이벤트 설정: main 브랜치에 pull request가 생성될 때 작업 실행
on:
  pull_request:
    branches: [main]

# 수행될 작업들
jobs:
  # 빌드 작업
  build:
    runs-on: ubuntu-latest # 작업이 실행될 환경: 최신 Ubuntu

    steps:
      - uses: actions/checkout@v3 # 체크아웃

      # JDK 17 설치
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: "17"
          distribution: "temurin"

      # Gradlew 실행 권한 부여
      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      # 프로젝트 빌드
      - name: Build with Gradle
        run: ./gradlew clean --stacktrace --info build
```

이 설정을 통해 main 브랜치에 Pull Request가 생성할 때마다 프로젝트가 자동으로 빌드되며, 빌드 결과에 따라 PR의 병합 여부를 결정할 수 있다.

빌드 실패 시 PR을 main 브랜치에 병합하지 못하도록 설정하는 방법은 다음과 같다.

1. 리포지토리의 **'Settings > Branches'**로 이동한다.
2. **'Add branch protection rule'** 버튼을 클릭한다.
3. **'Require status checks to pass before merging'** 옵션을 체크한다.

이 설정을 적용하면, 빌드 실패 시 main 브랜치에 PR을 병합할 수 없다. 이를 통해 코드의 품질을 유지하고 안정적인 배포를 보장할 수 있다.

## 참조

- [The JaCoCo Plugin](https://docs.gradle.org/current/userguide/jacoco_plugin.html)
- [Gradle 프로젝트에 JaCoCo 설정하기](https://techblog.woowahan.com/2661/)
- [코드 커버리지(Code Coverage)란?](https://hudi.blog/code-coverage/)
