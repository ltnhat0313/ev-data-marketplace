-- SQL Script for EV Data Analytics Marketplace
-- Database: MySQL / MariaDB

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `blog_posts`;
DROP TABLE IF EXISTS `testimonials`;
DROP TABLE IF EXISTS `users`;

--
-- Table structure for table `categories`
--
CREATE TABLE `categories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `slug` VARCHAR(255) UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--
INSERT INTO `categories` (`id`, `name`, `description`, `slug`) VALUES
(1, 'Hành vi lái xe', 'Dữ liệu về thói quen, quãng đường và hành vi của người lái xe điện.', 'driving-behavior'),
(2, 'Hiệu suất pin', 'Dữ liệu chi tiết về tình trạng sức khỏe (SoH), trạng thái sạc (SoC) và các yếu tố ảnh hưởng đến pin.', 'battery-performance'),
(3, 'Sử dụng trạm sạc', 'Dữ liệu về tần suất, thời gian và địa điểm sạc xe điện công cộng.', 'charging-station-usage'),
(4, 'Giao dịch V2G', 'Dữ liệu về các giao dịch mua bán điện từ xe vào lưới (Vehicle-to-Grid).', 'v2g-transactions'),
(5, 'Bảo trì & Sửa chữa', 'Dữ liệu về lịch sử bảo trì, các lỗi thường gặp và chi phí sửa chữa.', 'maintenance-repair');

--
-- Table structure for table `products`
--
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

--
-- Dumping data for table `products`
--
INSERT INTO `products` (`id`, `name`, `description`, `price`, `image_url`, `category_id`, `is_new_arrival`, `is_best_seller`, `is_you_may_like`) VALUES
-- New Arrivals
(1, 'Dữ liệu Pin VinFast (Quý 3/2024)', 'Bộ dữ liệu chi tiết về hiệu suất pin của các dòng xe VinFast trong quý 3 năm 2024.', 1500.00, 'images/product-item-1.jpg', 2, TRUE, FALSE, FALSE),
(2, 'Hành vi sạc nhanh tại Hà Nội', 'Phân tích thói quen sử dụng trạm sạc nhanh của người dùng xe điện tại Hà Nội.', 750.00, 'images/product-item-2.jpg', 3, TRUE, TRUE, FALSE),
(3, 'Dữ liệu V2G thử nghiệm (Tháng 8)', 'Dữ liệu từ chương trình thử nghiệm Vehicle-to-Grid trong tháng 8.', 900.00, 'images/product-item-4.jpg', 4, TRUE, FALSE, TRUE),
(4, 'Phân tích quãng đường di chuyển', 'Báo cáo phân tích quãng đường di chuyển trung bình hàng ngày của người dùng EV.', 450.00, 'images/product-item-6.jpg', 1, TRUE, FALSE, FALSE),

-- Best Sellers
(5, 'Dữ liệu hành trình (Raw) - TP.HCM', 'Bộ dữ liệu thô về các chuyến đi trong khu vực TP.HCM, bao gồm GPS, tốc độ, gia tốc.', 2500.00, 'images/product-item-3.jpg', 1, FALSE, TRUE, FALSE),
(6, 'Dashboard Hiệu suất Pin Toàn quốc', 'Dashboard tương tác phân tích hiệu suất pin trên nhiều dòng xe khác nhau.', 950.00, 'images/product-item-5.jpg', 2, FALSE, TRUE, TRUE),
(7, 'Tần suất sử dụng trạm sạc công cộng', 'Dữ liệu về mật độ và tần suất sử dụng các trạm sạc công cộng trên toàn quốc.', 800.00, 'images/product-item-7.jpg', 3, FALSE, TRUE, FALSE),

-- You May Like
(8, 'Ảnh hưởng thời tiết đến Pin', 'Phân tích mối tương quan giữa điều kiện thời tiết và hiệu suất pin xe điện.', 600.00, 'images/product-item-8.jpg', 2, FALSE, FALSE, TRUE),
(9, 'Mô hình dự báo lỗi bảo trì', 'Mô hình AI dự báo các lỗi có thể xảy ra dựa trên dữ liệu vận hành.', 1800.00, 'images/product-item-9.jpg', 5, FALSE, FALSE, TRUE),
(10, 'So sánh hành vi lái xe các vùng miền', 'Báo cáo so sánh thói quen lái xe điện giữa các khu vực Bắc, Trung, Nam.', 450.00, 'images/product-item-10.jpg', 1, FALSE, FALSE, TRUE);

--
-- Table structure for table `blog_posts`
--
CREATE TABLE `blog_posts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT,
  `image_url` VARCHAR(255),
  `category` VARCHAR(100),
  `created_at` DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `blog_posts`
--
INSERT INTO `blog_posts` (`id`, `title`, `content`, `image_url`, `category`, `created_at`) VALUES
(1, 'Xu hướng V2G: Xe điện sẽ thay đổi lưới điện ra sao?', 'Phân tích dữ liệu giao dịch V2G cho thấy tiềm năng to lớn của xe điện trong việc ổn định lưới điện và tạo ra nguồn thu nhập thụ động cho chủ xe.', 'images/post-image1.jpg', 'Phân tích', '2024-07-11'),
(2, 'Top 5 yếu tố ảnh hưởng đến tuổi thọ pin xe điện', 'Dựa trên dữ liệu thực tế, bài viết này chỉ ra các yếu tố chính từ thói quen sạc đến điều kiện lái xe ảnh hưởng đến tuổi thọ pin.', 'images/post-image2.jpg', 'Công nghệ', '2024-07-05'),
(3, 'Dự báo nhu cầu hạ tầng sạc tại các đô thị lớn', 'Sử dụng mô hình AI và dữ liệu hành trình để dự báo các điểm nóng cần xây dựng trạm sạc mới trong 5 năm tới.', 'images/post-image3.jpg', 'Thị trường', '2024-07-01');

--
-- Table structure for table `testimonials`
--
CREATE TABLE `testimonials` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `quote` TEXT NOT NULL,
  `author_name` VARCHAR(255) NOT NULL,
  `author_title` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `testimonials`
--
INSERT INTO `testimonials` (`id`, `quote`, `author_name`, `author_title`) VALUES
(1, 'Nguồn dữ liệu từ marketplace đã giúp chúng tôi rút ngắn thời gian nghiên cứu và phát triển (R&D) cho dòng pin mới tới 30%.', 'Giám đốc R&D', 'OEM Lớn'),
(2, 'Việc chia sẻ dữ liệu ẩn danh từ trạm sạc không chỉ mang lại nguồn doanh thu mới mà còn giúp chúng tôi hiểu rõ hơn về nhu cầu của khách hàng.', 'CEO', 'Mạng lưới trạm sạc'),
(3, 'Là một startup, việc tiếp cận dữ liệu chất lượng cao với chi phí hợp lý là yếu tố sống còn. Nền tảng này đã giải quyết bài toán đó cho chúng tôi.', 'Founder', 'Startup Phân tích EV');

--
-- Table structure for table `users` (Optional, for future expansion)
--
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('customer', 'provider', 'admin') NOT NULL DEFAULT 'customer',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
