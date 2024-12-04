package io.quarkiverse.langchain4j.sample.chatbot;

import io.quarkus.logging.Log;
import io.quarkus.websockets.next.OnOpen;
import io.quarkus.websockets.next.OnTextMessage;
import io.quarkus.websockets.next.WebSocket;
import io.smallrye.mutiny.Multi;

@WebSocket(path = "/chatbot")
public class ChatBotWebSocket {

    private final MovieMuse bot;

    public ChatBotWebSocket(MovieMuse bot) {
        this.bot = bot;
    }

    @OnTextMessage
    public Multi<String> onMessage(String message) {
        return bot.chat(message).onFailure().recoverWithItem(t -> {
            Log.warn(t);
            return "There was an error in communicating with the model server";
        });
    }

}
