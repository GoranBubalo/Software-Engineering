package Factory.ConcreateFactories;

import Factory.AbstractFactory.DocumentFactory;
import Products.AbstractProducts.Document;
import Products.ConcreateProducts.WordDocument;

public class MicrosoftOfficeFactory implements DocumentFactory {

    @Override
    public Document createWord() {
        return new WordDocument();
    }
    @Override
    public Document createExcel() {
       return null;
    }

    @Override
    public Document createPDF() {
        return null;
    }
}
