package Client;

import Factory.AbstractFactory.DocumentFactory;
import Factory.AbstractFactory.GUIFactory;
import Products.AbstractProducts.Button;
import Products.AbstractProducts.Checkbox;
import Products.AbstractProducts.Document;

// This removes flexibility
public class Application {
    private Button button;
    private Checkbox checkbox;

    private Document word;
    private Document excel;
    private Document pdf;

    public Application(GUIFactory factory) {
        button = factory.createButton();
        checkbox = factory.createCheckbox();
    }

    public Application(DocumentFactory factory) {
        this.word = factory.createWord();
        this.excel = factory.createExcel();
        this.pdf = factory.createPDF();
    }

    public void renderUI() {
        button.render();
        checkbox.render();
    }

    public void run() {
        word.open();
        excel.open();
        pdf.open();
    }
}
