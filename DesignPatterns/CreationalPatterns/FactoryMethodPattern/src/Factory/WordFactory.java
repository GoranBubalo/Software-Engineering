package Factory;

import ConcreateProduct.WordDocument;
import Factory.MainFactory.DocumentFactory;
import Product.Document;

public class WordFactory extends DocumentFactory {
    public Document createDocument() {
        return new WordDocument();
    }
}
