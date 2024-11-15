Poc 실습

1. Kubernetes 설치
    1.1 도커 데스크탑
    1.2 Kubernetes 활성화
2. Helm 차트 설치
    2.1.1 Helm 차트 (공식사이트)(windows) 설치 및 환경변수 추가 (C:\helm)
    2.1.2 Linux
           curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
           chmod 700 get_helm.sh
           ./get_helm.sh

3. Strimzi operator 설치
    3.1 kubectl create namespace kafka
    3.2 kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
    3.3 kubectl logs deployment/strimzi-cluster-operator -n kafka -f

4. Kafka cluster 설치
    4.1 kafka cluster with strimzi: kubectl apply -f kafka_cluster_test_v3.yaml -n kafka
    4.2 kafka-broker port-forwarding: kubectl port-forward svc/my-cluster-kafka-brokers 9092:9092 -n kafka
    4.3 kafka-ui 설치: kubectl apply -f kafka_ui.yaml -n kafka
    4.4 kafka-ui port-forward: kubectl port-forward -n kafka svc/kafka-ui-service 8082:8082

5. Kafka connect cluster 설치
    5.1 kafka connect cluster: kubectl apply -f kafka_connect.yaml -n kafka   (tjdwoocn/my-debezium-image_v3:latest 이미지 이용)(Docker login 필요)

6. Oracle db 설치 (아마 오라클 계정 로그인 해야할것임)
    6.0 oracle namespace 생성: kubectl create namespace oracle
    6.1 oracle 도커 이미지 21 버전 사용: oracle/database:21.3.0-ee, 또는 tjdwoocn/oracle-database:tagname 사용
    6.2 pv-pvc 설정: kubectl apply -f oracle_pv_pvc.yaml -n oracle
    6.3 oracle secret 배포: kubectl apply -f oracle_secret.yaml -n oracle
    6.4 oracle cluster 설치: kubectl apply -f oracle_deployment.yaml -n oracle

7. Oracle 계정 생성 및 권한부여
    7.1 oracle pod 접속: kubectl exec -it oracle-db-0 -n oracle
    7.2 sqlplus 접속: sqlplus sys/OraclePassword123! as sysdba
    7.3 계정 생성 및 권한 부여, CDB/PDB 등

8. Debezium connector 등록
    8.1 oracle_connector.json / oracle_connector_v2.json 등록
        curl -X POST -H "Content-Type: application/json" --data @oracle_connector.json http://localhost:8083/connectors/
        curl -X POST -H "Content-Type: application/json" --data @oracle_connector_v2.json http://localhost:8083/connectors/

        ## Connector 삭제
        curl -X DELETE http://localhost:8083/connectors/oracle-connector-debezium_v2-original  
        curl -X DELETE http://localhost:8083/connectors/oracle-connector-debezium_v2-transformed

    8.2 kafka-connect port-forward: kubectl port-forward -n kafka svc/kafka-connect-service 8083:8083
    8.3 Connector 등록 확인: http://localhost:8083/connectors/oracle-connector-debezium_v2-original/status
    8.4 Kafka-Ui에서 cdc 진행상황 확인

9. Airflow 설치 및 dag 등록
    9.1 Helm 사용 Airflow repo 추가: Apache-airflow repo
        helm repo add apache-airflow https://airflow.apache.org
        helm repo update
        helm show values apache-airflow/airflow
    9.2 custom airflow 이미지 사용: tjdwoocn/airflow-custom
        helm upgrade --install airflow apache-airflow/airflow -f airflow_values.yaml -n airflow
    9.3 pv,pvc 관련 설정
         dags, logs 등
    9.4 Airflow Webserver port-forwarding & log-in
         kubectl port-forward svc/airflow-webserver 8081:8080 -n airflow
         id: admin
         pwd: admin
    9.4 DAGs 등록 및 실행, 결과 확인

10. Prometheus, grafana 설치 및 모니터링
      - 진행중
