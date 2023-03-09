package org.acme.services;

import io.minio.ObjectWriteResponse;
import io.minio.UploadObjectArgs;
import org.acme.exceptions.StorageException;
import org.acme.models.Payload;
import org.acme.utils.StorageClient;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.io.File;

@ApplicationScoped
public class PayloadService {
    @Inject
    StorageClient storageClient;

    public void sendObjectToStorage(Payload payload, File file) throws StorageException {
        try {
            UploadObjectArgs uploadObjectArgs = UploadObjectArgs.builder()
                    .bucket("teste")
                    .object(payload.fileName)
                    .filename(file.getAbsolutePath())
                    .contentType("application/pdf")
                    .build();
            ObjectWriteResponse response = storageClient.getMinioClient().uploadObject(uploadObjectArgs);
            System.out.println(response.versionId());
        } catch (Exception e) {
            throw new StorageException("Error upload file to storage. Please try again");
        }
    }
}
