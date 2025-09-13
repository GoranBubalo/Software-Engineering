package ConcreatePrototype;

import AbstractPrototype.Shape;

public class Rectangle implements Shape {

    private int width,height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public Shape clone() {
        return new Rectangle(this.width,this.height);
    }

    @Override
    public void draw() {
        System.out.println("Drawing rectangle " + width + "x" + height);
    }
}
