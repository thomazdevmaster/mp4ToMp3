package org.acme.utils;

import io.minio.MinioClient;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class StorageClient {


    @ConfigProperty(name = "minio.secretkey")
    String secretKey;


    @ConfigProperty(name = "minio.username")
    String rootname;


    @ConfigProperty(name = "minio.endpoint")
    String endpoint;

    public MinioClient getMinioClient() {

        MinioClient minioClient = MinioClient.builder()
                .endpoint(endpoint)
                .credentials(rootname, secretKey)
                .build();

        return minioClient;
    }
}
