package ConcreateProduct;

import Product.Document;

public class PDFDocument implements Document {
    public void open(){
        System.out.println("Opening pdf document");
    }
}
