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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-13 18:11:34
