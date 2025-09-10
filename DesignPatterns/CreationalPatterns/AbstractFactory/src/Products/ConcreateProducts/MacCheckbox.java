package Products.ConcreateProducts;

import Products.AbstractProducts.Checkbox;

public class MacCheckbox implements Checkbox {

    @Override
    public void render() {
        System.out.println("Mac Checkbox");
    }
}
