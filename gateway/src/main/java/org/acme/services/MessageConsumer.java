package org.acme.services;

import org.acme.models.Payload;
import org.acme.models.Status;

import javax.enterprise.context.ApplicationScoped;
import javax.transaction.Transactional;
import java.io.UnsupportedEncodingException;
import org.eclipse.microprofile.reactive.messaging.Incoming;

@ApplicationScoped
public class MessageConsumer {
    @Incoming("id")
    @Transactional
    public void consume(byte[] msg) throws UnsupportedEncodingException {
        String id = new String(msg, "UTF-8");
        System.out.println(id);
        Payload.update("status = '"+ Status.converted.ordinal()+"' where idApp = ?1", id);
    }

    @Incoming("error")
    @Transactional
    public void consumeError(byte[] msg) throws UnsupportedEncodingException {
        String id = new String(msg, "UTF-8");
        System.out.println(id);
        Payload.update("status = '"+Status.error.ordinal()+"' where idApp = ?1", id);
    }
}
