package ConcreateProduct;

import Product.Document;

public class WordDocument implements Document {
    public void open(){
        System.out.println("Opening word document");
    }
}
