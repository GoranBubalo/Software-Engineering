package Products.ConcreateProducts;

import Products.AbstractProducts.Button;

public class MacButton implements Button {

    @Override
    public void render() {
        System.out.println("MacButton");
    }
}
