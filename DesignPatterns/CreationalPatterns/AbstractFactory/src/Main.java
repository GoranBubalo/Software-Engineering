import Client.Application;
import Factory.AbstractFactory.GUIFactory;
import Factory.ConcreateFactories.WindowsFactory;

public class Main {
    public static void main(String[] args) {

        GUIFactory factory = new WindowsFactory();
        Application app =  new Application(factory);

        app.renderUI();
    }
}