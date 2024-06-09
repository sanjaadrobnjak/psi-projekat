/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/EmptyTestNGTest.java to edit this template
 */

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
 * @author sanja
 */
public class T4NeuspesnoPrijavljivanjePogresnaLozinka {
    
    public T4NeuspesnoPrijavljivanjePogresnaLozinka() {
    }

    @Test
    public void testPrijavljivanje() {
        System.setProperty("webdriver.chrome.driver","C:\\chromedriver-win64\\chromedriver.exe");
        try{
            driver=new ChromeDriver();

            //dohvati nam sajt za testiranje
            driver.get(baseUrl);

            //popunjavanje podataka forme i slanje forme
            String user="sanjica";
            String pass="sanja";
            String poruka="Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.";

            driver.findElement(By.name("username")).sendKeys(user);
            driver.findElement(By.name("password")).sendKeys(pass);
            
            driver.findElement(By.xpath("//*[@id=\"login-form\"]/div[3]/input")).click();
            
            String welcomeMsg=driver.findElement(By.xpath("//p[contains(text(),'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')]")).getText();
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
