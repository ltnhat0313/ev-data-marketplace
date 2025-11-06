package com.example.dockerexample.repository;

import com.example.dockerexample.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Integer> {
    List<Product> findByIsNewArrival(boolean isNewArrival);
    List<Product> findByIsBestSeller(boolean isBestSeller);
    List<Product> findByRecommended(boolean recommended);
}
