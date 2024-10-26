-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: rule_engine
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `node`
--

DROP TABLE IF EXISTS `node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `node` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  `left_id` int DEFAULT NULL,
  `right_id` int DEFAULT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `left_id` (`left_id`),
  KEY `right_id` (`right_id`),
  CONSTRAINT `node_ibfk_1` FOREIGN KEY (`left_id`) REFERENCES `node` (`id`),
  CONSTRAINT `node_ibfk_2` FOREIGN KEY (`right_id`) REFERENCES `node` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node`
--

LOCK TABLES `node` WRITE;
/*!40000 ALTER TABLE `node` DISABLE KEYS */;
INSERT INTO `node` VALUES (1,'operator',2,4,'AND'),(2,'operand',NULL,NULL,'((age > 30'),(3,'operand',NULL,NULL,'department = \'Marketing\'))'),(4,'operator',5,6,'OR'),(5,'operand',NULL,NULL,'(salary >  20000'),(6,'operand',NULL,NULL,'experience > 5)'),(7,'operator',8,10,'AND'),(8,'operand',NULL,NULL,'((age > 30'),(9,'operand',NULL,NULL,'department = \'Marketing\'))'),(10,'operator',11,12,'OR'),(11,'operand',NULL,NULL,'(salary >  20000'),(12,'operand',NULL,NULL,'experience > 5)'),(13,'operator',14,18,'AND'),(14,'operand',NULL,NULL,'(age > 30'),(15,'operator',16,17,'OR'),(16,'operand',NULL,NULL,'department = \'Sales\')'),(17,'operand',NULL,NULL,'(age < 25'),(18,'operand',NULL,NULL,'department = \'Marketing\')'),(19,'operator',7,13,'AND');
/*!40000 ALTER TABLE `node` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-26 20:45:11
