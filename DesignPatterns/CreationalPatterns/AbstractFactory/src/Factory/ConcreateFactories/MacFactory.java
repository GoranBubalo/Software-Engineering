package Factory.ConcreateFactories;

import Factory.AbstractFactory.GUIFactory;
import Products.AbstractProducts.Button;
import Products.AbstractProducts.Checkbox;
import Products.ConcreateProducts.MacButton;
import Products.ConcreateProducts.MacCheckbox;

public class MacFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new MacButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }
}
