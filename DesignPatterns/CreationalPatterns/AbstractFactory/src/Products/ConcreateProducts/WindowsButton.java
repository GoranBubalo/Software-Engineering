package Products.ConcreateProducts;

import Products.AbstractProducts.Button;

public class WindowsButton implements Button {

    @Override
    public void render() {
        System.out.println("Windows Button");
    }
}
