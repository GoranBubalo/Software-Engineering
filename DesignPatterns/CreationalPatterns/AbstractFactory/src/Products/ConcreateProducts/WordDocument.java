package Products.ConcreateProducts;

import Products.AbstractProducts.Document;

public class WordDocument implements Document {

    @Override
    public void open() {
        System.out.println("Opening document");
    }
    @Override
    public void save() {
        System.out.println("Saving document");
    }
    @Override
    public void close() {
        System.out.println("Closing document");
    }
}
