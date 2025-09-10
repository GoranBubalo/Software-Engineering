package Factory.AbstractFactory;

import Products.AbstractProducts.Button;
import Products.AbstractProducts.Checkbox;

public interface GUIFactory {

    Button createButton();
    Checkbox createCheckbox();
}
