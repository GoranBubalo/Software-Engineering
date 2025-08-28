import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {

    public static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {


        Scanner scanner = new Scanner(System.in);
        System.out.print("Please enter first number: ");
        int a = scanner.nextInt();
        System.out.print("Please enter second number: ");
        int b = scanner.nextInt();

        FileWriter writer = null;

        try {
            int result = a / b;
            LOGGER.log(Level.INFO, "Result is {0}", result);

            writer = new FileWriter("result.txt");
            writer.write(result);
            LOGGER.log(Level.INFO, "Result written to file successfully");

        } catch (IOException ioException) {
            LOGGER.log(Level.SEVERE, "Error while writing file.", ioException);
        } catch (ArithmeticException arithmeticException) {
            LOGGER.log(Level.WARNING, "Arithmetic Exception, Can't divide with 0", arithmeticException);
        } finally {
            LOGGER.log(Level.INFO, "Exiting...");

            try {
                if(writer != null) {
                    writer.close();
                }
            } catch (IOException ioException) {
                LOGGER.log(Level.SEVERE, "Error while closing file.", ioException);
            }
        }
    }
}