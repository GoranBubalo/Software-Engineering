import AbstractPrototype.Shape;
import ConcreatePrototype.Circle;
import ConcreatePrototype.Rectangle;

public class Main {
    public static void main(String[] args) {
        Shape shape1 = new Circle(5);
        shape1.draw();

        Shape  shape2 = shape1.clone();
        shape2.draw();

        Shape rect1 = new Rectangle(5, 5);
        rect1.draw();

        Shape rect2 = rect1.clone();
        rect2.draw();

        System.out.println("Rect1: " + rect1);
        System.out.println("Rect2: " + rect2);
    }
}