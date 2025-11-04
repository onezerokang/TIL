# ServerSocket, Socket

자바에서 네트워크를 통해 다른 프로세스와 통신하기 위해선 ServerSocket과 Socket을 사용해야 한다. 먼저 요청을 받을 서버를 만들어보자.

```java
@Slf4j
public class Server {
    private static final int PORT = 80000;

    public static void main(String[] args) throws IOException {
        log.info("서버 시작");
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            log.info("서버 소켓 시작, 포트:{}", PORT);
            try (Socket socket = serverSocket.accept()) {
                log.info("소켓 연결");
                DataInputStream input = new DataInputStream(socket.getInputStream());
                DataOutputStream output = new DataOutputStream(socket.getOutputStream());

                String request = input.readUTF()
                log.info("client -> server: {}", request);

                String response = request + " ACK";
                output.writeUTF(response);
                log.info("server -> client: {}", response);

            }
        }
    }
}
```

서버가 다른 컴퓨터의 요청을 받기 위해선 ServerSocket 인스턴스를 만들어야 하는데, 이때 포트를 지정할 수 있다. ServerSocket은 클라이언트가 접속할 때까지 기다리다가, 접속이 되면 serverSocket#accpet() 메서드를 호출해 Socket 인스턴스를 만든다. 이후 Socket 인스턴스의 inputStream과 outputStream을 이용해 통신할 수 있다. 현재 구조는 한번의 요청-응답을 거치면 JVM이 종료되는 간단한 구조다.

```java
@Slf4j
public class Client {
    private static final int PORT = 80000;

    public static void main(String[] args) {
        log.info("클라이언트 시작")
        try (Socket socket = new Socket("localhost", PORT)) {
            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());

            output.writeUTF("Hello");
            String response = inputStream.readUTF();
            log.info("Respones: {}", response);
        }
    }
}
```

클라이언트는 요청을 보낼 때 Socket의 인스턴스만 있으면 되며, 요청을 보낼 서버의 주소를 지정할 수 있다. 마찬가지로 연결이 되고난 후 InputStream과 OutputStream을 이용해 요청을 보내고, 응답을 받을 수 있다. 참고로 요청을 보낼 때 클라이언트의 포트를 지정할 필요는 없다(지정할 수는 있다). 자신의 포트를 로컬 포트라고 하는데, 요청을 보낼 땐 컴퓨터에 남는 포트를 알아서 사용하기 때문이다.
