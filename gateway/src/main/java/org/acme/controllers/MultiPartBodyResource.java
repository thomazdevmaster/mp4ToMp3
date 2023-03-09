package org.acme.controllers;

import org.acme.MyEntity;
import org.acme.exceptions.StorageException;
import org.acme.models.MultiPartBody;
import org.acme.models.Payload;
import org.acme.models.Status;
import org.acme.services.PayloadService;
import org.jboss.logging.Logger;
import org.jboss.resteasy.annotations.providers.multipart.MultipartForm;

import javax.annotation.security.RolesAllowed;
import javax.inject.Inject;
import javax.transaction.Transactional;
import javax.validation.Valid;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.List;

@Path("/api/v1/convert")
public class MultiPartBodyResource {

    @Inject
    Logger logger;

    @Inject
    PayloadService payloadService;

    @POST
    @Transactional
    @RolesAllowed({"manager"})
    @Produces(MediaType.APPLICATION_JSON)
    public void convertMp4ToMp3(@Valid @MultipartForm MultiPartBody data) throws StorageException {
        logger.info("Starting converting mp4 to mp3 " + data);
        var payloadToPersist = Payload.multiPartToPayload(data);

        payloadToPersist.setStatus(Status.converting);
        payloadToPersist.persist();
        payloadService.sendObjectToStorage(payloadToPersist, data.getFile());
        logger.info("Payload created " + payloadToPersist);
    }

    @GET
    public List<Payload> getAllPayload() {
        logger.info("Getting all payload ");
        return Payload.listAll();
    }

    @POST()
    @Path("/teste")
    @Consumes(MediaType.APPLICATION_JSON)
    public void testeJson(MyEntity my) {
        logger.info("teste " + my);
    }

}
