package Factory.AbstractFactory;

import Products.AbstractProducts.Document;

public interface DocumentFactory {
    Document createWord();
    Document createExcel();
    Document createPDF();
}
