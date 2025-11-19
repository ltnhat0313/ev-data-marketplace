# --- Giai đoạn 1: Build (Dùng Maven với JDK 17 của Eclipse Temurin) ---
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy file cấu hình và tải thư viện trước (để cache)
COPY pom.xml .
# Lệnh này để tải dependencies về mà chưa cần code nguồn
RUN mvn dependency:go-offline -B

# Copy toàn bộ source code
COPY src ./src

# Build ra file .jar (bỏ qua test để chạy cho nhanh)
RUN mvn clean package -DskipTests

# --- Giai đoạn 2: Run (Dùng JRE 17 bản nhẹ của Eclipse Temurin) ---
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Copy file .jar từ giai đoạn build sang
COPY --from=build /app/target/*.jar app.jar

# Mở cổng 8080
EXPOSE 8080

# Lệnh chạy ứng dụng
ENTRYPOINT ["java", "-jar", "app.jar"]