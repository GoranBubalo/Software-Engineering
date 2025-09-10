package Client;

import Factory.AbstractFactory.GUIFactory;
import Products.AbstractProducts.Button;
import Products.AbstractProducts.Checkbox;

public class Application {
    private Button button;
    private Checkbox checkbox;

    public Application(GUIFactory factory) {
        button = factory.createButton();
        checkbox = factory.createCheckbox();
    }

    public void renderUI() {
        button.render();
        checkbox.render();
    }
}
