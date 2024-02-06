# MySQL 아키텍처

## 개요

MySQL 서버는 사람의 머리 역할을 담당하는 MySQL 엔진과 손발 역할을 담당하는 스토리지 엔진으로 구분할 수 있다. 그리고 스토리지 엔진은 핸들러 API를 만족하면 누구든지 스토리지 엔진을 구현하고 MySQL 서버에 추가해서 사용할 수 있다.

- MySQL 엔진
- 스토리지 엔진
  - InnoDB 스토리지 엔진
  - MyISAM 스토리지 엔진

## MySQL 엔진 아키텍처

MySQL 서버는 다른 DBMS에 비해 구조가 독특하다. 이런 독특한 구조 때문에 다른 DMBS에서 가질 수 없는 엄청난 혜택을 누릴 수 있으며, 반대로 다른 DMBS에서는 문제되지 않을 것들이 가끔 문제가 되기도 한다.

_MySQL의 전체 구조는 p.77에 있다(나중에 추가할 것)_

MySQL은 각 프로그래밍 언어의 표준에 맞는 드라이버를 제공하기에 모든 언어로 MySQL 서버에서 쿼리를 사용할 수 있다.

MySQL 서버는 크게 MySQL 엔진과 스토리지 엔진으로 구분할 수 있다.

### MySQL 엔진

MySQL 엔진은 클라이언트의 접속 및 쿼리 요청을 처리하는 커넥션 핸들러와 SQL 파서 및 전처리기, 쿼리의 최적화된 실행을 위한 옵티마이저로 구성되어있다.

### 스토리지 엔진

MySQL 엔진이 요청된 SQL 문장을 분석하거나 최적화하는 등 DMBS의 두뇌에 해당하는 처리를 한다면, 실제 데이터를 디스크 스토리지에 저장하거나, 디스크 스토리지로부터 조회하는 부분은 스토리지 엔진이 전담한다. MySQL 서버에서 MySQL 엔진은 하나지만 스토리지 엔진은 여러 개를 동시에 사용할 수 있다.

다음은 특정 테이블이 사용할 스토리지 엔진을 지정하는 예시다.

```sql
CREATE TABLE test_table (fd1 INT, fd2 INT) ENGINE=INNODB;
```

잉제 test_table에 대한 INSERT, SELECT, UPDATE, DELETE 작업은 InnoDB 스토리지 엔진이 담당한다. 그리고 각 스토리지 엔진은 성능 향상을 위해 키 캐시(MyISAM 스토리지 엔진)이나 InnoDB 버퍼풀(InnoDB 스토리지 엔진)과 같은 기능을 내장하고 있다.

### 핸들러 API

MySQL 엔진이 쿼리 실행기에서 데이터를 쓰거나 읽을 때 핸들러를 통해 각 스토리지 엔진에 읽기/쓰기 작업을 요청하는데, 이런 요런 요청을 핸들러 요청이라 하고, 이때 사용되는 API를 핸들러 API라고 한다. 이 핸들러 API를 통해 얼마나 많은 레코드 작업이 있었는지는 SHOW GLOBAL STATUS LIKE 'Handler%`; 명령어로 확인할 수 있다.

## MySQL 스레딩 구조

MySQL 서버는 프로세스 기반이 아닌 스레드 기반으로 작동하며, 크게 포그라운드(Foreground) 스레드와 백그라운드(background) 스레드로 구분할 수 있다.

performance_schema 데이터베이스의 threads 테이블을 조회하여 실행 중인 스레드 목록을 확인할 수 있다.

? performan

```sql
SELECT thread_id, name, type, processlist_user, processlist_host
FROM performance_schema.threads
ORDER BY type, thread_id;

+-----------+---------------------------------------------+------------+------------------+------------------+
| thread_id | name                                        | type       | processlist_user | processlist_host |
+-----------+---------------------------------------------+------------+------------------+------------------+
|         1 | thread/sql/main                             | BACKGROUND | NULL             | NULL             |
|         3 | thread/innodb/io_ibuf_thread                | BACKGROUND | NULL             | NULL             |
|         4 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         5 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         6 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         7 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         8 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|         9 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        10 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        11 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        12 | thread/innodb/page_flush_coordinator_thread | BACKGROUND | NULL             | NULL             |
|        14 | thread/innodb/log_checkpointer_thread       | BACKGROUND | NULL             | NULL             |
|        15 | thread/innodb/log_flush_notifier_thread     | BACKGROUND | NULL             | NULL             |
|        16 | thread/innodb/log_flusher_thread            | BACKGROUND | NULL             | NULL             |
|        17 | thread/innodb/log_write_notifier_thread     | BACKGROUND | NULL             | NULL             |
|        18 | thread/innodb/log_writer_thread             | BACKGROUND | NULL             | NULL             |
|        19 | thread/innodb/log_files_governor_thread     | BACKGROUND | NULL             | NULL             |
|        24 | thread/innodb/srv_lock_timeout_thread       | BACKGROUND | NULL             | NULL             |
|        25 | thread/innodb/srv_error_monitor_thread      | BACKGROUND | NULL             | NULL             |
|        26 | thread/innodb/srv_monitor_thread            | BACKGROUND | NULL             | NULL             |
|        27 | thread/innodb/buf_resize_thread             | BACKGROUND | NULL             | NULL             |
|        28 | thread/innodb/srv_master_thread             | BACKGROUND | NULL             | NULL             |
|        29 | thread/innodb/dict_stats_thread             | BACKGROUND | NULL             | NULL             |
|        30 | thread/innodb/fts_optimize_thread           | BACKGROUND | NULL             | NULL             |
|        31 | thread/mysqlx/worker                        | BACKGROUND | NULL             | NULL             |
|        32 | thread/mysqlx/acceptor_network              | BACKGROUND | NULL             | NULL             |
|        33 | thread/mysqlx/worker                        | BACKGROUND | NULL             | NULL             |
|        37 | thread/innodb/buf_dump_thread               | BACKGROUND | NULL             | NULL             |
|        38 | thread/innodb/clone_gtid_thread             | BACKGROUND | NULL             | NULL             |
|        39 | thread/innodb/srv_purge_thread              | BACKGROUND | NULL             | NULL             |
|        40 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        41 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        42 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        44 | thread/sql/signal_handler                   | BACKGROUND | NULL             | NULL             |
|        45 | thread/mysqlx/acceptor_network              | BACKGROUND | NULL             | NULL             |
|        43 | thread/sql/event_scheduler                  | FOREGROUND | event_scheduler  | localhost        |
|        47 | thread/sql/compress_gtid_table              | FOREGROUND | NULL             | NULL             |
|        48 | thread/sql/one_connection                   | FOREGROUND | root             | localhost        |
+-----------+---------------------------------------------+------------+------------------+------------------+
```

### 포그라운드 스레드(클라이언트 스레드)

클라이언트가 MySQL 서버에 접속하면 MySQL 서버는 클라이언트의 요청을 처리해줄 스레드를 생성해 할당하는 데, 이를 포그라운드 스레드(혹은 클라이언트 스레드)라고 한다.

포그라운드 스레드는 최소한 MySQL에 접속한 클라이언트의 수만큼 존재하며, 클라이언트가 요청하는 쿼리 문장을 처리한다. 커넥션이 종료될 경우 해당 커넥션을 담당하던 스레드는 다시 스레드 캐시로 되돌어가거나 thread_cache_size 시스템 변수 설정에 따라 종료된다.

포그라운드 스레드는 데이터를 MySQL의 데이터 버퍼나 캐시로부터 가져오는데, 캐시된 데이터가 없을 경우 직접 디스크나 인덱스 파일로부터 데이터를 읽어와야 한다. MyISAM 테이블은 디스크 쓰기 작업까지 포그라운드 스레드가 처리하지만 InnoDB 테이블은 버퍼나 캐시까지만 포그라운드 스레드가 처리하고, 나머지 버퍼로부터 디스크까지 기록하는 작업은 백그라운드 스레드가 처리한다.

### 백그라운드 스레드

InnoDB는 다음과 같이 여러 가지 작업이 백그라운드로 처리된다.

- 인서트 버퍼(Insert Buffer)를 병합하는 스레드
- 로그를 디스크로 기록하는 스레드
- InnoDB 버퍼 풀의 데이터를 디스크에 기록하는 스레드
- 데이터를 버퍼로 읽어 오는 스레드
- 잠금이나 데드락을 모니터링하는 스레드

MySQL 5.5부터 데이터 쓰기 스레드와 읽기 쓰레드의 개수를 2개 이상 지정할 수 있게 됐으며, innodb_write_io_threads와 innodb_read_id_threads 시스템 변수로 스레드 개수를 설정한다. InnoDB에서도 데이터를 읽는 작업은 주로 클라 스레드가 처리하기에 읽기 스레드는 많이 설정할 필요가 없지만 쓰기 스레드는 아주 많은 작업을 백그라운드로 처리하기에 일반적인 내장 디스크를 사용할 때는 2 ~ 4개 정도, \_DAS나 SAN 같은 스토리지를 사용할 때는 디스크를 최적으로 사용할 수 있을 만큼 충분히 설정하는 것이 좋다.

_사용자 요청을 처리하는 중 쓰기 작업은 지연(버퍼링)되어 처리될 수 있지만, 읽기는 절대 지연되서는 안된다. 그래서 일반적인 상용 DMBS에서는 쓰기 작업을 버퍼링해서 일괄 처리하는 기능이 탑재돼 있으며, InnoDB 또한 이런 방식으로 처리한다. 하지만 MyISAM은 사용자 스레드가 쓰기 작업까지 함께 처리하기에 쓰기 버퍼링 기능을 사용할 수 없다._

### 메모리 할당 및 사용 구조

MySQL에서 사용되는 메모리 영역은 크게 글로벌 메모리 영역과 로컬 메모리 영역으로 구분된다.

#### 글로벌 메모리 영역

MySQL 서버가 시작될 때 운영체제로부터 할당되며, 모든 스레드에 의해 공유된다.

대표적인 글로벌 메모리 영역은 다음과 같다.

- 테이블 캐시
- InnoDB 버퍼 풀
- InnoDB 어댑티드 해시 인덱스
- InnoDB 리두 로그 버퍼

#### 로컬 메모리 영역

클라이언트 스레드가 쿼리를 처리할 때 사용되는 영역으로 세션(커넥션) 메모리 영역 또는 클라이언트 메모리 영역이라고도 한다.

로컬 메모리는 각 클라이언트 스레드별로 독립적으로 할당되며 절대 공유되어 사용되지 않는다. 로컬 메모리 공간의 중요한 특징 중 하나는 요청된 쿼리에서 메모리 공간을 필요로 할 때만 공간이 할당되고 필요하지 않은 경우 MySQL이 메모리 공간을 할당조차도 하지 않을 수 있다는 점이다. 대표적으로 소트 버퍼나 조인 버퍼와 같은 공간이 그렇다.

대표적인 로컬 메모리 영역은 다음과 같다.

- 정렬 버퍼(Sort buffer)
- 조인 버퍼
- 바이너리 로그 캐시
- 네트워크 버퍼

### 플러그인 스토리지 엔진 모델

_p.86 MySQL 플러그인 모델 이미지_

MySQL의 독특한 구조 중 대표적인 것이 바로 플러그인 모델이다. 스토리지 엔진이나 사용자 인증을 위한 Native Authentication과 Caching SHA-2 Authentication 등도 모두 플러그인으로 구현되어 제공된다. 따라서 필요에 따라 사용자가 직접 스토리지 엔진을 개발할 수 있다.

MySQL에서 쿼리가 실행될 때 대부분의 작업을 MySQL 엔진에서 처리하고, 마지막 '데이터 읽기/쓰기' 작업만 스토리지 엔진에 의해 처리된다(즉 스토리지 엔진을 개발해도 일부분의 기능만 수행하는 엔진을 작성하게 된다는 의미다).

_p.86 MySQL 엔진과 스토리지 엔진의 처리 영역_

스토리지 영역이 처리하는 데이터 읽기/쓰기 작업은 대부분 1건의 레코드 단위(ex. 특정 인덱스의 레코드 1건 읽기 또는 다음 또는 이전 렐코드 읽기)로 처리된다.

MySQL을 사용하다보면 핸들러(Handler)라는 단어를 자주 등장하는데, 이는 MySQL 엔진이 스토리지 엔진을 조정하기 위해 사용하는 객체를 의미한다. 즉 MySQL 엔진이 각 스토리지 엔진에 명령하려면 반드시 핸들러를 통해야 한다.

이 파트에서 중요한 부분은 '하나의 쿼리 작업은 여러 하위 작업으로 나뉘는데, 각 하위 작업이 MySQL 엔진 영역에서 처리되는지 아니면 스토리지 엔진 영역에서 처리되는지 구분할 줄 알아야 한다'는 점이다.

MySQL 서버에서 지원되는 스토리지 엔진을 확인해보자.

```SQL
SHOW ENGINES;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| ndbcluster         | NO      | Clustered, fault-tolerant tables                               | NULL         | NULL | NULL       |
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| ndbinfo            | NO      | MySQL Cluster system information storage engine                | NULL         | NULL | NULL       |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
```

Support 칼럼에 표시될 수 있는 값은 다음 4가지다.

- **YES**: MySQL 서버에 해당 스토리지 엔진이 포함돼 있고, 사용 가능으로 활성화된 상태
- **DEFAULT**: 'YES'와 동일하지만 필수 스토리지 엔진임을 의미함(없으면 MySQL가 시작되지 않을 수도 있다)
- **NO**: 현재 MySQL 서버에 포함되지 않았음을 의미함
- **DISABLED**: 현재 MysQL 서버에는 포함됐지만 파라미터에 의해 비활성화된 상태

MySQL 서버에 포함됟지 않은 스토리지 엔진을 사용하고 싶다면 플러그인 형태로 빌드된 스토리지 엔진 라이브러리를 다운로드해서 끼워 넣기만 하면 된다.

모든 플러그인의 내용은 다음과 같이 확인할 수 있다.

```sql
SHOW PLUGINS
+----------------------------------+----------+--------------------+---------+---------+
| Name                             | Status   | Type               | Library | License |
+----------------------------------+----------+--------------------+---------+---------+
| binlog                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| mysql_native_password            | ACTIVE   | AUTHENTICATION     | NULL    | GPL     |
| sha256_password                  | ACTIVE   | AUTHENTICATION     | NULL    | GPL     |
| caching_sha2_password            | ACTIVE   | AUTHENTICATION     | NULL    | GPL     |
| sha2_cache_cleaner               | ACTIVE   | AUDIT              | NULL    | GPL     |
| daemon_keyring_proxy_plugin      | ACTIVE   | DAEMON             | NULL    | GPL     |
| CSV                              | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| MEMORY                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| InnoDB                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| INNODB_TRX                       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP                       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_RESET                 | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM                    | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM_RESET              | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_PER_INDEX             | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_PER_INDEX_RESET       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_PAGE               | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_PAGE_LRU           | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_POOL_STATS         | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TEMP_TABLE_INFO           | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_METRICS                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_DEFAULT_STOPWORD       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_DELETED                | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_BEING_DELETED          | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_CONFIG                 | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_INDEX_CACHE            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_INDEX_TABLE            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLES                    | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLESTATS                | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_INDEXES                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLESPACES               | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_COLUMNS                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_VIRTUAL                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CACHED_INDEXES            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_SESSION_TEMP_TABLESPACES  | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| MyISAM                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| MRG_MYISAM                       | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| PERFORMANCE_SCHEMA               | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| TempTable                        | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| ARCHIVE                          | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| BLACKHOLE                        | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| FEDERATED                        | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndbcluster                       | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndbinfo                          | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndb_transid_mysql_connection_map | DISABLED | INFORMATION SCHEMA | NULL    | GPL     |
| ngram                            | ACTIVE   | FTPARSER           | NULL    | GPL     |
| mysqlx_cache_cleaner             | ACTIVE   | AUDIT              | NULL    | GPL     |
| mysqlx                           | ACTIVE   | DAEMON             | NULL    | GPL     |
+----------------------------------+----------+--------------------+---------+---------+
```

### 컴포넌트

MySQL 8.0부터는 기존의 플러그인 아키테처를 대체하기 위해 컴포넌트 아키텍처가 지원된다.

다음은 MySQL 서버의 플러그인이 갖는 단점들이다.

- 플러그인은 오직 MySQL 서버와 인터페이스할 수 있고, 플러그인끼리는 통신이 불가함
- 플러그인은 MySQL 서버의 변수나 함수를 직접 호출하기 때문에 안전하지 않음(캡슐화 안 됨)
- 플러그인은 상호 의존 관계를 설정할 수 없어서 초기화가 어려움

MySQL 5.7까지는 비밀번호 검증 기능이 플러그인 형태로 제공됐지만 MySQL 8.0부터는 컴포넌트로 개선됐다.

### 쿼리 실행 구조

_p.91 쿼리 실행 구조_

위 그림은 쿼리를 실행하는 관점에서 MySQL 구조를 간략하게 표현한 것이다.

#### 쿼리 파서

쿼리 파서는 들어온 쿼리 문장을 토큰(MySQL이 인식할 수 있는 최소 단위의 어휘나 기호)로 분리해 트리 형태의 구조로 만들어 내는 작업을 의미한다. 쿼리 문장의 기본적인 문법 오류는 이 과정에서 발견되고 사용자에게 오류 메시지를 전달하게 된다.

#### 전처리기

파서 과정에서 만들어진 트리를 기반으로 쿼리 문장에 구조적인 문제점이 있는지 확인한다. 각 토큰을 테이블명, 칼럼명, 또는 내장 함수와 같은 개체를 매핑해 해당 객체의 존재 여부와 접근 권한 등을 확인하는 과정을 이 단계에서 수행한다. 존재하지 않거나 권한상 사용핢 수 없는 개체의 토큰은 이 단계에서 걸러진다.

#### 옵티마이저

DBMS의 두뇌 역할로 쿼리 문장을 저렴한 비용으로 가장 빠르게 처리할지를 결정하는 역할을 담당한다. 옵티마이저의 역할은 중요하기에 옵티마이자거 더 나은 선택을 할 수 있게 유도해야 한다.

#### 실행 엔진

옵티마이저가 방향을 결정한다면, 실행 엔진은 만들어진 계획대로 각 핸들러에게 요청해서 받은 결과를 또 다른 핸들러 요청의 입력으로 연결하는 역할을 수행한다.

다음은 옵티마이저가 GROUP BY를 처리하기 위해 임시 테이블을 사용하기로 결정한 상황에서 핸들러가 수행하는 작업이다.

1. 실행 엔진이 핸들러에게 임세 테이블을 만들라고 요청
2. 다시 실행 엔진은 WHERE 절에 일치하는 레코드를 읽어오라고 핸들러에게 요청
3. 읽어온 레코드들을 1번에서 준비한 임시 테이블로 저장하라고 핸들러에게 요청
4. 데이터가 준비된 임시 테이블에서 필요한 방식으로 데이터를 읽어오라고 핸들러에게 요청
5. 최종적으로 실행 엔진은 결과나 사용자를 다른 모듈에게 넘김

#### 핸들러(스토리지 엔진)

핸들러는 스토리지 엔진을 의미하며, MySQL 실행 엔진의 요청에 따라 데이터를 디스크로 저장하고, 디스크로부터 읽어오는 역할을 담당한다. InnoDB 테이블을 조작하면 핸들러가 InnoDB 스토리지 엔진이되고, MyISAM 테이브을 조작할 때는 핸들러가 MyISAM 스토리지 엔진이 된다.

### 복제

MySQL 서버에서 복제(Replication)은 매우 중요한 역할을 담당한다. MySQL 서버의 복제에 관해서는 별도의 장에서 다루고, 기본적인 복제 아키텍처 또한 16장 '복제'에서 다루겠다.

### 쿼리 캐시

쿼리 캐시는 SQL의 실행 결과를 메모리에 캐시하고, 동일 SQL 쿼리 실행 시 즉시 결과를 반환하여 매우 빠른 성능을 보였다. 허나 데이터가 수정될 때마다 캐시에 저장된 값을 삭제해야했기에 오히려 병목이 되었고 결국 MySQL 8.0으로 올라오면서 쿼리 캐시는 MySQL 서버의 기능에서 완전히 제거되었다.

### 스레드 풀

_해당 부분은 그냥 읽어보고, 필요할 때 다시 찾아보면 좋을 것 같음_

스레드풀은 MySQL 서버 엔터프리이즈 에디션에서만 지원된다.

만약 스레드풀을 커뮤니티 에디션에서 사용하고 싶다면 Percona Server에서 스레드 플러그인 라이브러리를 MySQL 커뮤니티 에디션 서버에 설치하면 된다.

Percona Server의 스레드 풀은 기본적으로 CPU 코어의 개수만큼 스레드 그룹을 생성한다. 스레드 풀 개수는 thread_pool_size 시스템 변수로 조정 가능하지만 일반적으로 코어의 개수와 맞추는 것이 CPU 프로세서 친화도를 높이는 데 좋다.

### 트랜잭션 지원 메타데이터

데이터베이스 서버에서 테이블 구조 정보와 스토어드 프로그램 등의 정보를 데이터 딕셔너리 또는 메타데이터라고 하는데, MySQL 5.7까지는 이를 파일 기반으로 관리했다. 하지만 파일 기반 메타데이터는 트랜잭션을 지원하지 않아, 테이블 구조 변경 도중, MySQL 서버가 비정상적으로 종료되면 테이블 구조가 깨지는 문제가 있었다.

MySQL 8.0부터는 이런 문제를 해결하기 위해 테이블의 구조 정보나 스토어드 프로그램의 코드 관련 정보, 시스템 테이블을 모두 InnoDB의 테이블에 저장하도록 개선했다.

## InnoDB 스토리지 엔진 아키텍처

### 프라이머리 키에 의한 클러스터링

### 외래 키 지원

### MVCC(Multi Version Concurrency Control)

### 잠금 없는 일고나된 읽기(Non-Locking Consistent Read)

### 자동 데드락 감지

### 자동화된 장애 복구

### InnoDB 버퍼 풀

#### 버퍼 풀의 크기 설정

#### 버퍼 풀의 구조

#### 버퍼 풀과 리두 로그

#### 버퍼 풀 플러시(Buffer Pool Flush)

#### 플러시 리스트 플러시

#### 리스트 플러시

### 버퍼 풀 상태 백업 및 복구

### 버퍼 풀의 적재 내용 확인

### Double Write Buffer

### 언두 로그

#### 언두 로그 모니터링

#### 언두 테이블스페이스 관리

### 체인지 버퍼

### 리두 로그 및 로그 버퍼

#### 리두 로그 아카이빙

#### 리두 로그 활성화 및 비활성화

### 어댑티브 해시 인덱스

### InnoDB와 MyISAM, MEMORY 스토리지 엔진 비교
