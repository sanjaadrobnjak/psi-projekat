
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

LOCK TABLES `app_igra` WRITE;
/*!40000 ALTER TABLE `app_igra` DISABLE KEYS */;
INSERT INTO `app_igra` VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15);
/*!40000 ALTER TABLE `app_igra` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `app_mrezabrojeva` WRITE;
/*!40000 ALTER TABLE `app_mrezabrojeva` DISABLE KEYS */;
INSERT INTO `app_mrezabrojeva` VALUES (1,288,7,7,2,8,10,50),(2,759,5,4,5,8,10,75),(3,671,7,3,3,9,10,50);
/*!40000 ALTER TABLE `app_mrezabrojeva` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `app_skoknamrezu` WRITE;
/*!40000 ALTER TABLE `app_skoknamrezu` DISABLE KEYS */;
INSERT INTO `app_skoknamrezu` VALUES (4,'Koje godine je palo Zapadno rimsko carstvo?',476),(5,'Koje godine je izbio Prvi balkansi rat?',1912),(6,'Koliko ima kičmenih pršljenova u ljudskom telu?',33);
/*!40000 ALTER TABLE `app_skoknamrezu` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `app_paukovasifra` WRITE;
/*!40000 ALTER TABLE `app_paukovasifra` DISABLE KEYS */;
INSERT INTO `app_paukovasifra` VALUES (7,'avion'),(8,'beton'),(9,'labud');
/*!40000 ALTER TABLE `app_paukovasifra` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `app_umrezavanje` WRITE;
/*!40000 ALTER TABLE `app_umrezavanje` DISABLE KEYS */;
INSERT INTO `app_umrezavanje` VALUES (10,'Spojite znamenitosti sa gradovima u kojima se nalaze','Keopsova piramida','Kairo','Krivi toranj','Piza','Karlov most','Prag','Crveni trg','Moskva','Tadž Mahal','Agra','Kip slobode','Njujork','Ajfelova kula','Pariz','Big Ben','London','Koloseum','Rim','Brandenburška kapija','Berlin'),(11,'Dovršite naslove filmova','Ko to tamo','peva','Povratak u','budućnost','Devojka od milion','dolara','Maratonci trče','počasni krug','Američka','lepota','Blistavi','um','Niske','strasti','Južni','vetar','Engleski','pacijent','Forest','Gamp'),(12,'Spojite visoke građevine u svetu sa državama u kojima se nalaze','Empire State Buildin','SAD','Taipei 101','Tajvan','Oriental Pearl Tower','Kina','Q1','Australija','Petronas Twin Tower','Malezija','CN Tower','Kanada','Ostankino Tower','Rusija','Burj Khalifa','Emirati','Abraj Al-Bait','Saudijska Arabija','Lotte World Tower','Južna Koreja');
/*!40000 ALTER TABLE `app_umrezavanje` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `app_uteknipauku` WRITE;
/*!40000 ALTER TABLE `app_uteknipauku` DISABLE KEYS */;
INSERT INTO `app_uteknipauku` VALUES (13,'redosled'),(14,'vinograd'),(15,'dočekati');
/*!40000 ALTER TABLE `app_uteknipauku` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

