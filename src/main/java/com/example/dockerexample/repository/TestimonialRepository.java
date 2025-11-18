package com.example.dockerexample.repository;

import com.example.dockerexample.model.Testimonial;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TestimonialRepository extends JpaRepository<Testimonial, Integer> {
}