# MySQL의 격리 수준(Isolation level)

## 개요

트랜잭션의 격리 수준(Isolation level)이란 여러 트랜잭션이 동시에 처리될 때, 특정 트랜잭션이 다른 트랜잭션에서 변경하거나 조회하는 데이터를 볼 수 있게 허용할지 말지를 결정하는 것이다.

트랜잭션 격리수준은 크게 READ UNCOMMITED, READ COMMITED, REPEATABLE READ, SERIALIZABLE로 나뉜다. 뒤로 갈수록 데이터 부정합 문제가 발생하지 않지만, 동시 처리 성능도 떨어진다.

|                 | DIRTY READ | NON-REPEATABLE READ | PHANTOM READ        |
| --------------- | ---------- | ------------------- | ------------------- |
| READ UNCOMMITED | 발생       | 발생                | 발생                |
| READ COMMITED   | 없음       | 발생                | 발생                |
| REPEATABLE READ | 없음       | 없음                | 발생(InnoDB는 없음) |
| SERIALIZABLE    | 없음       | 없음                | 없음                |

## READ UNCOMMITED

READ UNCOMMITED 격리 수준은 다른 트랜잭션에서 처리 중이거나, 커밋되지 않은 데이터를 다른 트랜잭션이 읽는 것을 허용하는 격리 수준을 말한다. 이렇게 작업이 완료되지 않은 데이터를 읽는 현상을 DIRTY READ라고 한다.

READ UNCOMMITED 격리 수준은 정합성에 문제가 많은 격리 수준이라 거의 사용되지 않는다.

## READ COMMITED

READ COMMITED 격리 수준은 커밋된 데이터만 읽을 수 있는 격리 수준이다. 이 격리 수준에서는 트랜잭션이 커밋된 데이터만 조회할 수 있기 때문에 DIRTY READ 현상이 발생하지 않는다.

그러나 READ COMMITED 격리 수준에서는 NON-REPEATABLE READ라는 데이터 부정합 문제가 발생할 수 있다. 이는 하나의 트랜잭션 내에서 동일한 데이터를 여러 번 조회했을 때, 조회마다 다른 결과를 얻는 현상이다.

이 문제는 처음 데이터를 조회했을 때 해당 데이터가 아직 다른 트랜잭션에 의해 커밋되지 않아 언두(undo) 영역의 데이터를 읽었지만, 두 번째 조회 시점에는 해당 데이터가 이미 커밋되어 변경된 결과를 보게 되는 경우에 발생한다.

## REPEATABLE READ

REPEATABLE READ는 MySQL InnoDB 스토리지 엔진에서 기본으로 사용되는 격리 수준이다. 이 격리 수준에서는 NON-REPEATABLE READ 부정합이 발생하지 않는다. InnoDB 스토리지 엔진은 트랜잭션이 ROLLBACK될 가능성을 대비해 변경되기 전 레코드를 언두(Undo) 공간에 백업해두고 실제 레코드 값을 변경한다. 이런 변경 방식을 MVCC라고 한다.

REPEATABLE READ는 이 MVCC를 위해 언두 영역에 백업된 이전 데이터를 이용해 동일 트랜잭션 내에서는 동일한 결과를 보여줄 수 있게 보장한다. 어떤 데디엍

## SERIALIZABLE

SERIALIZABLE 격리 수준은 데이터베이스의 트랜잭션이 순차적으로 실행되는 것처럼 동작하는 가장 엄격한 격리 수준이다. 이 격리 수준에서는 모든 읽기 연산이 공유 잠금(읽기 잠금)을 필요로 하며, 이는 트랜잭션 간의 동시성 처리 성능을 크게 저하시킨다.

SERIALIZABLE 격리 수준은 팬텀 리드(Phantom Read) 문제를 방지하지만 InnoDB 스토리지 엔진에서는 갭 락(Gap Locks)과 넥스트 키 락(Next-Key Locks) 덕분에 REPEATABLE READ 격리 수준에서도 PHONETOM READ가 발생하지 않기에 SERIALIZABLE 격리 수준을 사용할 이유가 없다.

## 참조

- Real MySQL 8.0, 백은빈, 이성욱, 5장 트랜잭션과 잠금
