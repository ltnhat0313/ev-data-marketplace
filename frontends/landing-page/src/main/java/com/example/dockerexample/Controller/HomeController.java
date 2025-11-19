package com.example.dockerexample.Controller;

import com.example.dockerexample.model.BlogPost;
import com.example.dockerexample.model.Product;
import com.example.dockerexample.model.Testimonial;
import com.example.dockerexample.repository.BlogPostRepository;
import com.example.dockerexample.repository.ProductRepository;
import com.example.dockerexample.repository.TestimonialRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller; // <--- QUAN TRỌNG: Phải là Controller
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller // <--- KHÔNG ĐƯỢC DÙNG @RestController
public class HomeController {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private BlogPostRepository blogPostRepository;

    @Autowired
    private TestimonialRepository testimonialRepository;

    @GetMapping("/")
    public String home(Model model) {
        try {
            // Lấy dữ liệu (có thể rỗng nếu DB chưa có gì)
            List<Product> newArrivals = productRepository.findByIsNewArrival(true);
            List<Product> bestSellers = productRepository.findByIsBestSeller(true);
            List<Product> recommendedProducts = productRepository.findByRecommended(true);
            List<BlogPost> blogPosts = blogPostRepository.findAll();
            List<Testimonial> testimonials = testimonialRepository.findAll();

            model.addAttribute("newArrivals", newArrivals);
            model.addAttribute("bestSellers", bestSellers);
            model.addAttribute("youMayLike", recommendedProducts);
            model.addAttribute("blogPosts", blogPosts);
            model.addAttribute("testimonials", testimonials);
        } catch (Exception e) {
            // Log lỗi nếu DB connection có vấn đề, nhưng vẫn trả về trang chủ
            e.printStackTrace();
        }
        
        return "index"; // Trả về file index.html trong thư mục templates
    }
}