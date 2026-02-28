# File, Files

- 자바에서 파일, 디렉토리를 다룰 때는 File, Files, Path 클래스를 사용한다.
  - Java 1.0에서 File이 나왔고 1.7에서 Files와 Path가 등장했다.
  - Files, Path: File의 성능과 편의성을 개선한 버전.
    - FileInputStream, FileWriter 사용을 고민하기전 Files로 처리할 수 있는지 먼저 확인하자.
    - 더 편하고 최적화되어 있다.

## Files 자주 사용하는 메서드

```java
import java.nio.file.Path;

public static void main(String[] args) {
    final Path filePath = Path.of("java-adv2/temp/example.txt");
    final Path dirPath = Path.of("java-adv2/temp/exampleDir");

    // static 메서드로 기능을 제공한다.
    System.out.println("File exists: " + Files.exists(filePath));
    System.out.println("Directory exists: " + Files.exists(dirPath));

    // 파일 생성
    try {
        Files.createFile(filePath);
        System.out.println("File created");
    } catch (FileAlreadyExistsException e) {
        System.out.println(filePath + " File already exists");
    }

    // 디렉터리 생성
    try {
        Files.createDirectory(dirPath);
        System.out.println("Directory created");
    } catch (FileAlreadyExistsException e) {
        System.out.println(dirPath + " Directory already exists");
    }

    // 파일 정보 확인
    System.out.println("Is regular file: " + Files.isRegularFile(filePath));
    System.out.println("Is directory: " + Files.isDirectory(dirPath));
    System.out.println("File name: " + filePath.getFileName());
    System.out.println("File size: " + Files.size(filePath) + "bytes");

    // 파일 이동
    final Path newFilePath = Path.of("java-adv2/temp/newExample.txt");
    Files.move(filePath, newFilePath, StandardCopyOption.REPLACE_EXISTING);

    // 파일 속성 확인
    final BasicFileAttributes attrs = Files.readAttributes(newFilePath, BasicFileAttributes.class);
    System.out.println("==== Attributes ====");
    System.out.println("Creation time: " + attrs.creationTime());
    System.out.println("Is directory: " + attrs.isDirectory());
    System.out.println("Is regular file: " + attrs.isRegularFile());
    System.out.println("Is symbolic link: " + attrs.isSymbolicLink());
    System.out.println("size: " + attrs.size());

    // 파일 삭제
    Files.delete(newFilePath);
    System.out.println("File deleted");
}
```

## Files로 문자 파일 읽기

- 문자로된 파일을 읽고 쓸 때 FileReader, FileWriter 같은 스트림 클래스를 사용하면 코드가 장황해진다.
- 반복문을 작성해야 하며, 한 줄씩 읽고 싶다면 BufferedReader 같은 클래스를 추가해야 했다.
- Files를 사용하면 문자를 간결하게 읽을 수 있다.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public static void main(String[] args) {
    final Path path = Path.of("java-adv2/temp/hello2.txt");

    // 파일에 쓰기
    Files.writeString(path, "Hello\nFiles!");

    // 파일을 읽기
    final String readString = Files.readString(path);
    System.out.println("readString = " + readString);

    // 파일을 읽고 한줄 단위로 나눠 반환하기
    final List<String> lines = Files.readAllLines(path);
    for (String line : lines) {
        System.out.println(line);
    }

    // 파일을 스트림 단위로 읽어오기
    // 모든 파일을 메모리에 올리지 않고 부분적으로 읽기에 메모리를 절약할 수 있다.
    try (final Stream<String> lineStream = Files.lines(path)) {
        lineStream.forEach(System.out::println);
    }
}
```

## 파일 복사 최적화

파일을 복사해보면서 왜 Files를 사용하는 것이 좋은지 알아보자.

- 방법 1
  - FileInputStream#readAllBytes()를 통해 모두 읽어오고 FileOutputStream#write()을 통해 한꺼번에 저장한다.
  - 파일(copy.dat) -> 자바(byte) -> 파일(copy_new.dat)
  - 자바가 copy.dat 파일의 데이터를 자바 프로세스가 자용하는 메모리에 불러온다. 그리고 메모리에 있는 데이터를 copy_new.dat에 전달한다.

```java
import java.io.*;

public static void main(String[] args) {
    try (final FileInputStream fis = new FileInputStream("/tmp/target.dat");
         final FileOutputStream fos = new FileOutputStream("/tmp/copied.dat")) {
        final byte[] bytes = fis.readAllBytes();
        fos.write(bytes);
    }
}
```

- 방법 2
  - InputStream#transferTo(OutputStream): 쭉 읽어서 OutputStream로 전달한다.
  - 내부적으로 성능 최적화가 되어있다.
  - 파일(copy.dat) -> 자바(byte) -> 파일(copy_new.dat) 과정을 거친다.

```java
import java.io.*;

public static void main(String[] args) {
    try (final FileInputStream fis = new FileInputStream("/tmp/target.dat");
         final FileOutputStream fos = new FileOutputStream("/tmp/copied.dat")) {
        fis.transferTo(fos);
    }
}
```

- 방법 3
  - Files#copy()를 사용하면 훨씬 InputStream#transferTo()보다 빠르게 처리할 수 있다.
  - 방법 1,2 번은 파일을 모두 메모리에 올렸다.
  - Files#copy는 운영체제의 파일 복사 기능을 사용한다. 파일 -> 파일
  - 따라서 가장 빠르다. 파일을 다룰 일이 있다면 항상 Files의 기능을 먼저 찾아보자.

```java
import java.nio.file.Files;

public static void main(String[] args) {
    final Path source = Path.of("java-adv2/temp/copy.dat");
    final Path target = Path.of("java-adv2/temp/copy_new.dat");
    Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
}
```

## 정리

- File은 자바 1.0에 나온 기능으로 레거시 코드다.
- 1.7에 등장한 Files가 최적화/간결함에서 압승이다.
- 파일을 처리할 상황이 있다면 Files이 제공하는 메서드를 찾아보자.
- Files를 사용하면 Reader를 사용하는 것보다 훨씬 편리하게 파일을 읽을 수 있다.
- Files#lines()를 활용하면 한줄씩 메모리에 올려서 읽을 수도 있다.
- Files#copy()를 호출하면 파일을 메모리에 올리지 않고, 운영체제의 파일 복사 기능을 활용하기 떄문에 훨씬 빠르게 처리할 수 있다.

## 출처

- [김영한의 실전 자바 고급 2](https://www.inflearn.com/course/%EA%B9%80%EC%98%81%ED%95%9C%EC%9D%98-%EC%8B%A4%EC%A0%84-%EC%9E%90%EB%B0%94-%EA%B3%A0%EA%B8%89-2)
