# 27장 Serializable과 NIO도 살펴 봅시다

## Serializable

개발자가 만든 클래스를 파일에 읽거나 쓸 수 있도록 하거나, 다른 서버로 보내거나 받을 수 있도록 하려면 java.io 패키지의 Serializable 인터페이스를 구현하도록 해야 한다.

그리고, Serializable 인터페이스를 구현 한 후에는 serialVersionUID라는 값을 지정해주는 것을 권장한다(별도로 지정하지 않으면 컴파일 시 자동으로 생성된다).

```java
static final long serialVersionUID = 1L;
```

객체를 다른 서버와 주고 받으려면 양쪽다 같은 클래스를 갖고 있어야 한다. serialVersionUID는 객체의 버전이며, 이 버전이 다르거나 변수의 개수나 타입이 다를 경우 다른 클래스로 인식한다(클래스 명이 같더라도).

따라서 Serializable한 객체의 내용이 변경된다면 serialVersionUID의 값을 변경하는 습관을 가져야 한다(대부분의 자바 개발툴에서는 자동으로 serialVersionUID를 생성하는 기능을 제공한다).

## 객체 저장하기

ObjectOutputStream을 이용하면 객체를 저장할 수 있다.

먼저 DTO를 만들자.

```java
public class SerialDto implements Serializable{
    private String bookName;
    private int bookOrder;
    private boolean bestSeller;
    private long soldPerDay;

    public SerialDto(String bookName, int bookOrder, boolean bestSeller, long soldPerDay) {
        super();
        this.bookName = bookName;
        this.bookOrder = bookOrder;
        this.bestSeller = bestSeller;
        this.soldPerDay = soldPerDay;
    }

    @Override
    public String toString() {
        return "SerialDto{" +
                "bookName='" + bookName + '\'' +
                ", bookOrder=" + bookOrder +
                ", bestSeller=" + bestSeller +
                ", soldPerDay=" + soldPerDay +
                '}';
    }
}
```

이제 저장하는 클래스를 다음과 같이 만들자.

```java

public class ManageObject {
    public static void main(String[] args) {
        ManageObject manager = new ManageObject();
        String fullPath = separator + "Users" + separator + "wonyoung" + separator + "dev" + separator + "godofjava" + separator + "serial.obj";
        SerialDto dto = new SerialDto("GodOfJavaBook", 1, true, 100);
        manager.saveObject(fullPath, dto);
    }

    private void saveObject(String fullPath, SerialDto dto) {
        FileOutputStream fos = null;
        ObjectOutputStream oos = null;

        try {
            fos = new FileOutputStream(fullPath);
            oos = new ObjectOutputStream(fos);
            oos.writeObject(dto);
            System.out.println("Write Success");

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (oos != null) {
                try {
                    oos.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            if (fos != null) {
                try {
                    fos.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

위 코드를 실행해보면 serial.obj 파일로 객체가 저장된 것을 확인할 수 없다.
만약 SerialDto 클래스에서 Serializable을 구현하지 않았다면 NotSerializableException이 발생할 것이다.

## 객체 읽기

객체를 읽을 때는 Output 대신 Input으로 되어 있는 클래스들을 사용하며 된다.

```java
private void loadObject(String fullPath) {
    FileInputStream fis = null;
    ObjectInputStream ois = null;

    try {
        fis = new FileInputStream(fullPath);
        ois = new ObjectInputStream(fis);
        Object obj = ois.readObject();
        SerialDto dto = (SerialDto) obj;
        System.out.println(dto);

    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (ois != null) {
            try {
                ois.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        if (fis != null) {
            try {
                fis.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
```

SerialDto 클래스의 경우 toString() 메소드를 오버라이딩 했기 때문에, 위 메소드를 실행하면 다음과 같은 결과가 출력된다.

```
SerialDto{bookName='GodOfJavaBook', bookOrder=1, bestSeller=true, soldPerDay=100}
```

## transient

객체를 저장하거나, 다른 JVM으로 보낼 때, transient라는 예약어를 사용하여 선언한 변수는 Serializable의 대상에서 제외된다.

비밀번호 같이 저장되거나 전송된다면 보안상 큰 문제가 발생할 수 있는 변수에 transient를 붙여주는 것이다.

```java
transient private String password;
```

## 자바 NIO란?

NIO(New I/O)는 기존 IO보다 빠른 속도로 작업을 처리하기 위해 JDK 1.4에서 추가되었다.
NIO는 스트림을 사용하지 않고 Channel과 Buffer를 사용한다.

```java
public class NioSample {
    public static void main(String[] args) {
        NioSample sample = new NioSample();
        sample.basicWriteAndRead();
    }

    private void basicWriteAndRead() {
        String fileName = separator + "Users" + separator + "wonyoung" + separator + "dev" + separator + "godofjava" + separator + "nio.txt";
        try {
            writeFile(fileName, "My first NIO Sample");
            readFile(fileName);
        } catch (Exception e) {
            e.printStackTrace();
        }


    }


    private void writeFile(String fileName, String data) throws Exception {
        FileChannel channel = new FileOutputStream(fileName).getChannel(); // FileChannel을 만들기 위해서는 FileOutPutStream의 getChannel() 메소드를 호출해야 한다.
        byte[] byteData = data.getBytes();
        ByteBuffer buffer = ByteBuffer.wrap(byteData); // ByteBuffer 객체를 생성한다.
        channel.write(buffer); // FileChannel 클래스에 선언된 write() 메소드에 buffer 객체를 넘겨주면 파일을 작성하다.
        channel.close();
    }

    private void readFile(String fileName) throws Exception {
        FileChannel channel = new FileInputStream(fileName).getChannel(); // 파일을 읽기 위한 객체도 FileInputStream의 getChannel() 메소드를 호출해야 한다.
        ByteBuffer buffer = ByteBuffer.allocate(1024); // ByteBuffer 클래스의 allocate() 메소드를 통해 buffer 객체를 만든다.
        channel.read(buffer); // 데이터를 버퍼에 담으라고 알려준다.
        buffer.flip(); // buffer에 담겨있는 데이터의 가장 앞으로 이동한다.
        while(buffer.hasRemaining()) {
            System.out.print((char)buffer.get()); // 한 바이트씩 읽는 작업을 수행한다.
        }
        channel.close();
    }
}
```

위 코드를 실행하면 다음 내용이 출력된다.

```
My first NIO Sample
```

## NIO의 Buffer 클래스

NIO에서 제공하는 Buffer는 java.nio.Buffer 클래스를 확장하여 사용한다. Buffer는 ByteBuffer, CharBuffer, DoubleBuffer, FloatBuffer, IntBuffer, LongBuffer, ShortBuffer 등이 존재한다.

다음은 버퍼의 상태 및 속성을 확인하기 위한 메소드다.

- capacity(): 버퍼에 담을 수 있는 크기 리턴
- limit(): 버퍼에서 읽거나 쓸 수 있는 첫 위치 리턴
- position(): 현재 버퍼의 위치 리턴

버퍼는 CD처럼 위치가 있다. 버퍼에 데이터를 담거나, 읽는 작업을 수행하면 현재의 위치로 이동한다. 위의 예제에서 버퍼 객체 생성 시 지정한 것이 이 값들이다. 이 3개 값의 관계는 다음과 같다.

```
0 <= position <= limit <= capacity
```

NIO를 제대로 이해하려면 이 세 개의 값의 관계를 꼭 이해하고, 기억해야 한다.
예제를 통해 이 세 개의 메소드와 친해져보자.

```java
public class NioDetailSample {
    public static void main(String[] args) {
        NioDetailSample sample = new NioDetailSample();
        sample.checkBuffer();
    }

    private void checkBuffer() {
        try {
            IntBuffer buffer = IntBuffer.allocate(1024);
            for(int i=0; i<100; i++) {
                buffer.put(i);
            }
            System.out.println("Buffer capacity="+buffer.capacity()); // 1024
            System.out.println("Buffer limit="+buffer.limit()); // 1024
            System.out.println("Buffer position="+buffer.position()); // 100
            buffer.flip();
            System.out.println("Buffer flipped");
            System.out.println("Buffer limit="+buffer.limit()); // `100
            System.out.println("Buffer position="+buffer.position()); // 0
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

버퍼의 위치를 변경하는 메소드는 다음과 같다.

- flip(): limit 값을 현재 position으로 지정한 후, position을 0(가장 앞)으로 이동
- mark(): 현재 positon을 mark
- reset(): 버퍼의 position을 mark한 곳으로 이동
- rewind(): 현재 qjvjdml position을 0으로 이동
- remaining(): limit - position 계산 결과를 리턴
- hasRemaining(): position와 limit 값에 차이가 있을 경우 true를 리턴
- clear(): 버퍼를 지우고 현재 position을 0으로, limit을 버퍼의 크기로 변경

이렇게 버퍼에서 제공하는 메소드를 사용하면 데이터를 읽는데 큰 어려움이 없다.

NIO는 파일을 읽고 쓸 때만 사용하는 것이 아니라, 파일 복사를 하거나, 네트워크로 데이터를 주고 받을 때에도 사용할 수 있다.
