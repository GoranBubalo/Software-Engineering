package Products.ConcreateProducts;

import Products.AbstractProducts.Checkbox;

public class WindowsCheckbox implements Checkbox {

    @Override
    public void render() {
        System.out.println("Windows Checkbox");
    }
}
