public class Singleton {

    private static Singleton singleton;

    private Singleton() {
        System.out.println("Singleton instance Created");
    }

    public static Singleton getInstance() {
        if(singleton == null) {
            singleton = new Singleton();
        }
        return singleton;
    }
}
