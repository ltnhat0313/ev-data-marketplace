package com.example.dockerexample.Controller;

import com.example.dockerexample.model.BlogPost;
import com.example.dockerexample.model.Product;
import com.example.dockerexample.model.Testimonial;
import com.example.dockerexample.repository.BlogPostRepository;
import com.example.dockerexample.repository.ProductRepository;
import com.example.dockerexample.repository.TestimonialRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class HomeController {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private BlogPostRepository blogPostRepository;

    @Autowired
    private TestimonialRepository testimonialRepository;

    @GetMapping("/")
    public String home(Model model) {
        List<Product> newArrivals = productRepository.findByIsNewArrival(true);
        List<Product> bestSellers = productRepository.findByIsBestSeller(true);
        List<Product> recommendedProducts = productRepository.findByRecommended(true);
        List<BlogPost> blogPosts = blogPostRepository.findAll();
        List<Testimonial> testimonials = testimonialRepository.findAll();

        model.addAttribute("newArrivals", newArrivals);
        model.addAttribute("bestSellers", bestSellers);
        model.addAttribute("youMayLike", recommendedProducts); // Giữ tên attribute là "youMayLike" để không phải sửa file HTML
        model.addAttribute("blogPosts", blogPosts);
        model.addAttribute("testimonials", testimonials);

        return "index";
    }
}