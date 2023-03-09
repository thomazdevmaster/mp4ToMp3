package org.acme.utils;

import io.minio.MinioClient;

import javax.inject.Singleton;

@Singleton
public class StorageClient {

    public MinioClient getMinioClient() {
        MinioClient minioClient = MinioClient.builder()
                .endpoint("http://localhost:9000")
                .credentials("ROOTNAME", "CHANGEME123")
                .build();

        return minioClient;
    }
}
