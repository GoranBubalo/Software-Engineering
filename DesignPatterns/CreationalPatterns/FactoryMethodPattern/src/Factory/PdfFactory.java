package Factory;

import ConcreateProduct.PDFDocument;
import Factory.MainFactory.DocumentFactory;
import Product.Document;

public class PdfFactory extends DocumentFactory {
    public Document createDocument() {
        return new PDFDocument();
    }
}
