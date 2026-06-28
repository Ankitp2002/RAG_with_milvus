# RUN milvus DB
docker run -d \
  --name milvus-standalone \
  --security-opt seccomp:unconfined \
  -e ETCD_USE_EMBED=true \
  -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
  -e COMMON_STORAGETYPE=local \
  -v $HOME/milvus_data:/var/lib/milvus \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:v2.4.0 milvus run standalone
