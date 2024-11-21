FROM registry.access.redhat.com/ubi8/openjdk-21:latest
WORKDIR /app
COPY --chown=185:0 --chmod=744 . .
RUN mvn package
EXPOSE 8080
ENV JAVA_OPTS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
ENV JAVA_APP_JAR="/app/target/quarkus-app/quarkus-run.jar"
