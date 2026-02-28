# Reader, Writer

- InputStream과 OutputStream을 사용하면 네트워크, 파일등으로부터 데이터를 바이트로 읽고 쓸 수 있다.
- Stream은 바이트만 사용할 수 있기 때문에 문자를 처리할 경우 개발자가 직접 인코딩/디코딩을 해줘야 한다.
- Reader, Writer 추상 클래스를 사용하면 귀찮은 인코딩/디코딩 과정을 생략할 수 있다.

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import static java.nio.charset.StandardCharsets.UTF_8;

public static void main(String[] args) {
    // Writer의 구현체인 OutputStreamWriter
    // 생성자로 OutputStream과 인코딩 문자집합을 받는다.
    // 내부에서 문자를 인코딩한 후, OutputStream에 전달한다.
    try (final OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream("temp/writer.txt"), UTF_8)) {
        osw.write("Hello, Java I/O!");
    }

    // Reader의 구현체인 InputStreamReader
    // 생성자로 InputStream과 디코딩 문자집합을 받는다.
    // 내부에서 문자를 디코딩한 후, InputStream에 전달한다.
    final StringBuilder stringBuilder = new StringBuilder();
    try (final InputStreamReader isr = new InputStreamReader(new FileInputStream("temp/reader.txt", UTF_8))) {
        int c;
        while ((c = isr.read()) != -1) {
            stringBuilder.append((char) c);
        }
    }
    System.out.println(stringBuilder);
}
```

- OutputStreamWriter, InputStreamReader를 사용하면 바이트 대신 문자를 저장하고 읽을 수 있다.
- 이는 Reader와 Writer의 구현체가 내부적으로 인코딩/디코딩을 대신 처리해주기 때문이다.
- OutputStreamWriter, InputStreamReader를 감싼 FileWriter와 FileReader를 사용할 수도 있다.

```java
import java.io.FileWriter;
import java.io.FileReader;
import java.nio.charset.StandardCharsets;

import static java.nio.charset.StandardCharsets.UTF_8;

public static void main(String[] args) {
    try (final FileWriter fw = new FileWriter("temp/writer.txt", UTF_8)) {
        fw.write("Hello, Java I/O!");
    }

    final StringBuilder stringBuilder = new StringBuilder();
    try (final FileReader fr = new FileReader("temp/reader.txt", UTF_8)) {
        int c;
        while ((c = fr.read()) != -1) {
            stringBuilder.append((char) c);
        }
    }
    System.out.println(stringBuilder);
}
```

## BufferWriter, BufferReader

- 이전의 예제는 문자를 한 글자씩 읽고 있는데, BufferReader를 사용하면 한 줄씩 읽을 수 있다.

```java
public class ReaderWriterMainV4 {
    public static final String FILE_NAME = "temp/buffer.txt";
    public static final int BUFFER_SIZE = 8192;

    public static void main(String[] args) throws IOException {
        try (final BufferedWriter bw = new BufferedWriter(new FileWriter(FILE_NAME, UTF_8), BUFFER_SIZE)) {
            bw.write("abc\n가나다");
        }

        final StringBuilder content = new StringBuilder();
        try (final BufferedReader br = new BufferedReader(new FileReader(FILE_NAME, UTF_8), BUFFER_SIZE)) {
            // -1을 반환할 수 없기에 null을 반환한다.
            String line;
            while ((line = br.readLine()) != null) {
                content.append(line).append("\n");
            }
        }
        System.out.println(content);
    }
}
```

## 출처

- [김영한의 실전 자바 고급 2](https://www.inflearn.com/course/%EA%B9%80%EC%98%81%ED%95%9C%EC%9D%98-%EC%8B%A4%EC%A0%84-%EC%9E%90%EB%B0%94-%EA%B3%A0%EA%B8%89-2)
