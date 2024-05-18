-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: mrezaznanja
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_igra`
--

DROP TABLE IF EXISTS `app_igra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_igra` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_igra`
--

LOCK TABLES `app_igra` WRITE;
/*!40000 ALTER TABLE `app_igra` DISABLE KEYS */;
INSERT INTO `app_igra` VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15),(16),(17),(18),(19),(20),(21),(22),(23),(24),(25),(26),(27),(28),(29),(30),(31),(32),(33),(34),(35),(36),(37),(38);
/*!40000 ALTER TABLE `app_igra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_mrezabrojeva`
--

DROP TABLE IF EXISTS `app_mrezabrojeva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_mrezabrojeva` (
  `igra_ptr_id` bigint(20) NOT NULL,
  `TrazeniBroj` int(11) NOT NULL,
  `PomocniBroj1` int(11) NOT NULL,
  `PomocniBroj2` int(11) NOT NULL,
  `PomocniBroj3` int(11) NOT NULL,
  `PomocniBroj4` int(11) NOT NULL,
  `PomocniBroj5` int(11) NOT NULL,
  `PomocniBroj6` int(11) NOT NULL,
  PRIMARY KEY (`igra_ptr_id`),
  CONSTRAINT `app_mrezabrojeva_igra_ptr_id_72bdb8b4_fk_app_igra_id` FOREIGN KEY (`igra_ptr_id`) REFERENCES `app_igra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_mrezabrojeva`
--

LOCK TABLES `app_mrezabrojeva` WRITE;
/*!40000 ALTER TABLE `app_mrezabrojeva` DISABLE KEYS */;
INSERT INTO `app_mrezabrojeva` VALUES (1,288,7,7,2,8,10,50),(2,759,5,4,5,8,10,75),(3,671,7,3,3,9,10,50);
/*!40000 ALTER TABLE `app_mrezabrojeva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_paukovasifra`
--

DROP TABLE IF EXISTS `app_paukovasifra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_paukovasifra` (
  `igra_ptr_id` bigint(20) NOT NULL,
  `TrazenaRec` varchar(20) NOT NULL,
  PRIMARY KEY (`igra_ptr_id`),
  CONSTRAINT `app_paukovasifra_igra_ptr_id_b242d0ee_fk_app_igra_id` FOREIGN KEY (`igra_ptr_id`) REFERENCES `app_igra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_paukovasifra`
--

LOCK TABLES `app_paukovasifra` WRITE;
/*!40000 ALTER TABLE `app_paukovasifra` DISABLE KEYS */;
INSERT INTO `app_paukovasifra` VALUES (7,'avion'),(8,'beton'),(9,'labud');
/*!40000 ALTER TABLE `app_paukovasifra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_skoknamrezu`
--

DROP TABLE IF EXISTS `app_skoknamrezu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_skoknamrezu` (
  `igra_ptr_id` bigint(20) NOT NULL,
  `Postavka` longtext NOT NULL,
  `Odgovor` int(11) NOT NULL,
  PRIMARY KEY (`igra_ptr_id`),
  CONSTRAINT `app_skoknamrezu_igra_ptr_id_2dc0dff7_fk_app_igra_id` FOREIGN KEY (`igra_ptr_id`) REFERENCES `app_igra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_skoknamrezu`
--

LOCK TABLES `app_skoknamrezu` WRITE;
/*!40000 ALTER TABLE `app_skoknamrezu` DISABLE KEYS */;
INSERT INTO `app_skoknamrezu` VALUES (4,'Koje godine je palo Zapadno rimsko carstvo?',476),(5,'Koje godine je izbio Prvi balkansi rat?',1912),(6,'Koliko ima kičmenih pršljenova u ljudskom telu?',33),(16,'Koliko prstenova ima na olimpijskoj zastavi',5),(17,'Koliko jezika je zvanično priznatih u Švajcarskoj?',4),(18,'Koje godine je Kolumbo otkrio Ameriku?',1492),(19,'Koje godine je Titanik potonuo?',1912),(20,'Koliko je 2+2/2?',3),(21,'Koliko knjiga ima serijal o Harry Potter-u?',7),(22,'Koliko planeta ima u našem solarnom sistemu?',8),(23,'Koliko simfonija je komponovao Ludvig van Betoven?',9),(24,'Koliko igrača je na terenu u fudbalskom timu?',11),(25,'Koje godine je osnovan Facebook?',2004),(26,'Koliko kilobajt (KB) sadrži bajtova?',1024),(27,'Koliko godina je imao Isus Hrist kad je bio razapet?',33),(28,'Koje godine se održala Kosovska bitka?',1389),(29,'Koliko sekundi ima jedan minut?',60),(30,'Koje godine je završen Drugi svetski rat?',1945),(31,'Koliko pauk ima nogu?',8),(32,'Koliko godina je trajao tridesetogodišnji rat?',30),(33,'Koliko je prstiju imala Mona Liza na svakoj ruci?',5),(34,'Koliko centimetara ima metar?',100),(35,'Koje godine je srušen zid u Berlinu?',1989),(36,'Koje godine je počela pandemija COVID-19?',2019),(37,'Koliko kontinenata postoji na Zemlji?',7),(38,'Koliko kostiju ima odrasli čovek?',206);
/*!40000 ALTER TABLE `app_skoknamrezu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_umrezavanje`
--

DROP TABLE IF EXISTS `app_umrezavanje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_umrezavanje` (
  `igra_ptr_id` bigint(20) NOT NULL,
  `TekstPitanja` longtext NOT NULL,
  `Postavka1` varchar(20) NOT NULL,
  `Odgovor1` varchar(20) NOT NULL,
  `Postavka2` varchar(20) NOT NULL,
  `Odgovor2` varchar(20) NOT NULL,
  `Postavka3` varchar(20) NOT NULL,
  `Odgovor3` varchar(20) NOT NULL,
  `Postavka4` varchar(20) NOT NULL,
  `Odgovor4` varchar(20) NOT NULL,
  `Postavka5` varchar(20) NOT NULL,
  `Odgovor5` varchar(20) NOT NULL,
  `Postavka6` varchar(20) NOT NULL,
  `Odgovor6` varchar(20) NOT NULL,
  `Postavka7` varchar(20) NOT NULL,
  `Odgovor7` varchar(20) NOT NULL,
  `Postavka8` varchar(20) NOT NULL,
  `Odgovor8` varchar(20) NOT NULL,
  `Postavka9` varchar(20) NOT NULL,
  `Odgovor9` varchar(20) NOT NULL,
  `Postavka10` varchar(20) NOT NULL,
  `Odgovor10` varchar(20) NOT NULL,
  PRIMARY KEY (`igra_ptr_id`),
  CONSTRAINT `app_umrezavanje_igra_ptr_id_62ecd5e9_fk_app_igra_id` FOREIGN KEY (`igra_ptr_id`) REFERENCES `app_igra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_umrezavanje`
--

LOCK TABLES `app_umrezavanje` WRITE;
/*!40000 ALTER TABLE `app_umrezavanje` DISABLE KEYS */;
INSERT INTO `app_umrezavanje` VALUES (10,'Spojite znamenitosti sa gradovima u kojima se nalaze','Keopsova piramida','Kairo','Krivi toranj','Piza','Karlov most','Prag','Crveni trg','Moskva','Tadž Mahal','Agra','Kip slobode','Njujork','Ajfelova kula','Pariz','Big Ben','London','Koloseum','Rim','Brandenburška kapija','Berlin'),(11,'Dovršite naslove filmova','Ko to tamo','peva','Povratak u','budućnost','Devojka od milion','dolara','Maratonci trče','počasni krug','Američka','lepota','Blistavi','um','Niske','strasti','Južni','vetar','Engleski','pacijent','Forest','Gamp'),(12,'Spojite visoke građevine u svetu sa državama u kojima se nalaze','Empire State Buildin','SAD','Taipei 101','Tajvan','Oriental Pearl Tower','Kina','Q1','Australija','Petronas Twin Tower','Malezija','CN Tower','Kanada','Ostankino Tower','Rusija','Burj Khalifa','Emirati','Abraj Al-Bait','Saudijska Arabija','Lotte World Tower','Južna Koreja');
/*!40000 ALTER TABLE `app_umrezavanje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_uteknipauku`
--

DROP TABLE IF EXISTS `app_uteknipauku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_uteknipauku` (
  `igra_ptr_id` bigint(20) NOT NULL,
  `TrazenaRec` varchar(20) NOT NULL,
  PRIMARY KEY (`igra_ptr_id`),
  CONSTRAINT `app_uteknipauku_igra_ptr_id_623488c0_fk_app_igra_id` FOREIGN KEY (`igra_ptr_id`) REFERENCES `app_igra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_uteknipauku`
--

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

-- Dump completed on 2024-05-18 12:24:34
