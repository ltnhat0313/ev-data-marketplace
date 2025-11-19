-- SQL Script for EV Data Analytics Marketplace
-- Database: MySQL / MariaDB

-- =============================================
-- 1. CLEANUP (Xóa bảng cũ để tránh xung đột)
-- =============================================
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `transactions`;
DROP TABLE IF EXISTS `two_factor_secrets`;
DROP TABLE IF EXISTS `datasets`; -- Bảng cho Python Backend
DROP TABLE IF EXISTS `products`; -- Bảng cho Java Landing Page
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `blog_posts`;
DROP TABLE IF EXISTS `testimonials`;
DROP TABLE IF EXISTS `users`;

-- =============================================
-- 2. USER MANAGEMENT (Dùng chung)
-- =============================================
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(255) NOT NULL UNIQUE,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `hashed_password` VARCHAR(255) NOT NULL, -- SỬA: Khớp với model Python (User.hashed_password)
  `role` VARCHAR(50) DEFAULT 'consumer',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu mẫu Users (Mật khẩu mặc định: 123456)
INSERT INTO `users` (`id`, `username`, `email`, `hashed_password`, `role`) VALUES
(1, 'admin', 'admin@evdata.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn96pzlkEqLy6Hpnkjo0Agk.K.16', 'admin'),
(2, 'provider', 'provider@evdata.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn96pzlkEqLy6Hpnkjo0Agk.K.16', 'provider'),
(3, 'consumer', 'consumer@evdata.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn96pzlkEqLy6Hpnkjo0Agk.K.16', 'consumer');

-- Bảng 2FA (Cho Auth Service)
CREATE TABLE `two_factor_secrets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `secret` VARCHAR(255),
  `enabled` BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 3. CATEGORIES & FRONTEND CONTENT (Cho Java)
-- =============================================
CREATE TABLE `categories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `slug` VARCHAR(255) UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `categories` (`id`, `name`, `description`, `slug`) VALUES
(1, 'Hành vi lái xe', 'Dữ liệu về thói quen, quãng đường và hành vi của người lái xe điện.', 'driving-behavior'),
(2, 'Hiệu suất pin', 'Dữ liệu chi tiết về tình trạng sức khỏe (SoH), trạng thái sạc (SoC).', 'battery-performance'),
(3, 'Sử dụng trạm sạc', 'Dữ liệu về tần suất, thời gian và địa điểm sạc xe điện công cộng.', 'charging-station-usage'),
(4, 'Giao dịch V2G', 'Dữ liệu về các giao dịch mua bán điện từ xe vào lưới.', 'v2g-transactions'),
(5, 'Bảo trì & Sửa chữa', 'Dữ liệu về lịch sử bảo trì, các lỗi thường gặp.', 'maintenance-repair');

-- Bảng Products (Dành riêng cho Java Landing Page hiển thị mẫu)
CREATE TABLE `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `price` DECIMAL(10, 2) NOT NULL,
  `image_url` VARCHAR(255),
  `category_id` INT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `is_new_arrival` BOOLEAN DEFAULT FALSE,
  `is_best_seller` BOOLEAN DEFAULT FALSE,
  `is_you_may_like` BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `products` (`id`, `name`, `description`, `price`, `image_url`, `category_id`, `is_new_arrival`, `is_best_seller`, `is_you_may_like`) VALUES
(1, 'Dữ liệu Pin VinFast (Quý 3/2024)', 'Bộ dữ liệu chi tiết về hiệu suất pin...', 1500.00, 'images/product-item-1.jpg', 2, TRUE, FALSE, FALSE),
(2, 'Hành vi sạc nhanh tại Hà Nội', 'Phân tích thói quen sử dụng trạm sạc...', 750.00, 'images/product-item-2.jpg', 3, TRUE, TRUE, FALSE),
(3, 'Dữ liệu V2G thử nghiệm', 'Dữ liệu từ chương trình thử nghiệm V2G...', 900.00, 'images/product-item-4.jpg', 4, TRUE, FALSE, TRUE),
(4, 'Phân tích quãng đường', 'Báo cáo phân tích quãng đường di chuyển...', 450.00, 'images/product-item-6.jpg', 1, TRUE, FALSE, FALSE),
(5, 'Dữ liệu hành trình (Raw) - TP.HCM', 'Bộ dữ liệu thô về các chuyến đi...', 2500.00, 'images/product-item-3.jpg', 1, FALSE, TRUE, FALSE);

-- =============================================
-- 4. MARKETPLACE LOGIC (Cho Python Backend)
-- =============================================
-- Bảng Datasets (Khớp với model Python Dataset)
CREATE TABLE `datasets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255),        -- Python dùng 'title' thay vì 'name'
  `description` TEXT,
  `price` FLOAT,               -- Python dùng Float
  `file_path` VARCHAR(500),    -- Đường dẫn file CSV upload
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `owner_id` INT,
  FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu mẫu cho Python Backend (trỏ về user provider)
INSERT INTO `datasets` (`title`, `description`, `price`, `file_path`, `owner_id`) VALUES
('Dataset Pin VinFast Q3', 'Dữ liệu hiệu suất pin thực tế', 1500.0, 'uploads/battery_vf_q3.csv', 2),
('Hành vi sạc Hà Nội', 'Thói quen sạc tại các trạm công cộng', 750.0, 'uploads/charging_hanoi.csv', 2),
('Dữ liệu V2G Pilot', 'Kết quả thử nghiệm V2G tháng 8', 900.0, 'uploads/v2g_pilot.csv', 2);

-- Bảng Transactions (Lịch sử mua bán)
CREATE TABLE `transactions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `dataset_id` INT,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`dataset_id`) REFERENCES `datasets`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 5. BLOG & TESTIMONIALS (Frontend content)
-- =============================================
CREATE TABLE `blog_posts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT,
  `image_url` VARCHAR(255),
  `category` VARCHAR(100),
  `created_at` DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `blog_posts` (`id`, `title`, `content`, `image_url`, `category`, `created_at`) VALUES
(1, 'Xu hướng V2G: Xe điện sẽ thay đổi lưới điện ra sao?', 'Phân tích tiềm năng to lớn...', 'images/post-image1.jpg', 'Phân tích', '2024-07-11'),
(2, 'Top 5 yếu tố ảnh hưởng đến tuổi thọ pin', 'Các yếu tố chính từ thói quen sạc...', 'images/post-image2.jpg', 'Công nghệ', '2024-07-05'),
(3, 'Dự báo nhu cầu hạ tầng sạc', 'Sử dụng mô hình AI để dự báo...', 'images/post-image3.jpg', 'Thị trường', '2024-07-01');

CREATE TABLE `testimonials` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `quote` TEXT NOT NULL,
  `author_name` VARCHAR(255) NOT NULL,
  `author_title` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `testimonials` (`id`, `quote`, `author_name`, `author_title`) VALUES
(1, 'Nguồn dữ liệu giúp chúng tôi rút ngắn thời gian R&D...', 'Giám đốc R&D', 'OEM Lớn'),
(2, 'Việc chia sẻ dữ liệu mang lại nguồn doanh thu mới...', 'CEO', 'Mạng lưới trạm sạc'),
(3, 'Tiếp cận dữ liệu chất lượng cao với chi phí hợp lý...', 'Founder', 'Startup Phân tích EV');