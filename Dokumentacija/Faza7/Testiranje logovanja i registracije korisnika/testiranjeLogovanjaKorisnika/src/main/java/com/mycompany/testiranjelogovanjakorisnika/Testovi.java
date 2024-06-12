package main;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 *
 * @author skoko
 */
public class Testovi {
    public static String baseUrl="http://127.0.0.1:8000/accounts/login";
    public static WebDriver driver;
    
    public static void main(String[] args){
        System.setProperty("webdriver.chrome.driver", "C:\\chromedriver-win64\\chromedriver.exe");
        // C:\\chromedriver-win64\\chromedriver.exe
        driver=new ChromeDriver();   
        driver.get(baseUrl);
        driver.manage().window().maximize();
    }
}
