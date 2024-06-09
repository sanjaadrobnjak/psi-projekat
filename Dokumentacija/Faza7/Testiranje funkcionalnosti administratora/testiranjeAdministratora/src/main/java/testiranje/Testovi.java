
package main;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 *
 * @author sanja
 */
public class Testovi {
    public static String baseUrl="http://127.0.0.1:8000/admin/login/?next=/admin/";
    public static WebDriver driver;
    
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\chromedriver-win64\\chromedriver.exe");
        driver=new ChromeDriver();
        
        driver.get(baseUrl); 
    }
    
}
