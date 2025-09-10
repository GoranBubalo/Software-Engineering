package Factory.ConcreateFactories;

import Factory.AbstractFactory.GUIFactory;
import Products.AbstractProducts.Button;
import Products.AbstractProducts.Checkbox;
import Products.ConcreateProducts.WindowsButton;
import Products.ConcreateProducts.WindowsCheckbox;

public class WindowsFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new WindowsButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }
}
