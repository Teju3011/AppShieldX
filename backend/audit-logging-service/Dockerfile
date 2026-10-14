FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for principle of least privilege
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY target/audit-logging-service-1.0.0.jar app.jar

USER appuser

EXPOSE 8085

ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
