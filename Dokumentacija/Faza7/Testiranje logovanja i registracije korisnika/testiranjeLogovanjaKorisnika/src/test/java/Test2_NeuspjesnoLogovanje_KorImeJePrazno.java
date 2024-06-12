import static main.Testovi.baseUrl;
import static main.Testovi.driver;
import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import static org.testng.Assert.*;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

/**
 *
 * @author skoko
 */
public class Test2_NeuspjesnoLogovanje_KorImeJePrazno {
    
    public Test2_NeuspjesnoLogovanje_KorImeJePrazno() { }

    
    @Test
    public void logovanjeTest() {
        System.setProperty("webdriver.chrome.driver","C:\\chromedriver-win64\\chromedriver.exe");
        try{
            driver=new ChromeDriver();
            driver.get(baseUrl);

            String user="";
            String password="lukalt123";
            String poruka="Dobrodošao nazad lukalt";

            driver.findElement(By.name("username")).sendKeys(user);
            driver.findElement(By.name("password")).sendKeys(password);
            driver.findElement(By.xpath("/html/body/div/div/form/button")).click();
            

            String welcomeMsg=driver.findElement(By.xpath("//div[contains(text(),'Pogresno korisnicko ime ili sifra')]")).getText();
            Assert.assertTrue(welcomeMsg.contains(poruka));


        } catch(Throwable e){
                System.out.println(e.getMessage());
        }
            
        if(driver!=null){
            driver.quit();
        }
    }

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @BeforeMethod
    public void setUpMethod() throws Exception {
    }

    @AfterMethod
    public void tearDownMethod() throws Exception {
    }
}