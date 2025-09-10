package Products.ConcreateProducts;

import Products.AbstractProducts.Document;

public class PDFDocument implements Document {

    @Override
    public void open() {
        System.out.println("Opening PDF Document");
    }

    @Override
    public void close() {
        System.out.println("Closing PDF Document");
    }

    @Override
    public void save() {
        System.out.println("Saving PDF Document");
    }
}
