-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: camila_db
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
-- Table structure for table `sensores`
--

DROP TABLE IF EXISTS `sensores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_hora` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estoque_status` varchar(50) DEFAULT NULL,
  `manipulacao_status` varchar(50) DEFAULT NULL,
  `separacao_status` varchar(50) DEFAULT NULL,
  `status_geral` varchar(50) DEFAULT NULL,
  `pecas_aguardando` varchar(50) DEFAULT NULL,
  `qualidade_sensor` varchar(50) DEFAULT NULL,
  `temperatura` float DEFAULT NULL,
  `umidade` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=288 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensores`
--

LOCK TABLES `sensores` WRITE;
/*!40000 ALTER TABLE `sensores` DISABLE KEYS */;
INSERT INTO `sensores` VALUES (228,'2025-10-14 16:40:56','N/A','N/A','N/A','N/A','0','Desconhecida',0,54),(229,'2025-10-14 16:41:06','N/A','N/A','N/A','N/A','0','Desconhecida',0,54),(230,'2025-10-14 16:41:16','N/A','N/A','N/A','N/A','0','Desconhecida',0,54),(231,'2025-10-14 16:41:27','N/A','N/A','N/A','N/A','0','Desconhecida',0,54),(232,'2025-10-14 16:41:37','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(233,'2025-10-14 16:41:47','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(234,'2025-10-14 16:41:57','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(235,'2025-10-14 16:42:07','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(236,'2025-10-14 16:42:17','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(237,'2025-10-14 16:42:27','N/A','N/A','N/A','N/A','0','Desconhecida',26,54),(238,'2025-10-14 16:42:37','N/A','N/A','N/A','N/A','0','Desconhecida',26,55),(239,'2025-10-14 16:42:47','N/A','N/A','N/A','N/A','0','Desconhecida',26,55),(240,'2025-10-14 16:42:57','N/A','N/A','N/A','N/A','0','Desconhecida',26,55),(241,'2025-10-14 16:43:07','N/A','N/A','N/A','N/A','0','Desconhecida',26,55),(242,'2025-10-14 16:43:17','N/A','N/A','N/A','N/A','0','Desconhecida',26,56),(243,'2025-10-14 16:43:27','N/A','N/A','N/A','N/A','0','Desconhecida',26,56),(244,'2025-10-14 16:43:37','N/A','N/A','N/A','N/A','0','Desconhecida',26,56),(245,'2025-10-14 16:43:47','N/A','N/A','N/A','N/A','0','Desconhecida',26,56),(246,'2025-10-14 16:43:57','N/A','N/A','N/A','N/A','0','Desconhecida',26,56),(247,'2025-10-14 16:44:07','N/A','N/A','N/A','N/A','0','Desconhecida',26,57),(248,'2025-10-14 16:44:17','N/A','N/A','N/A','N/A','0','Boa',26,57),(249,'2025-10-14 16:44:27','N/A','N/A','N/A','N/A','0','Boa',26,57),(250,'2025-10-14 16:44:37','N/A','N/A','N/A','N/A','0','Boa',26,57),(251,'2025-10-14 16:44:48','N/A','N/A','N/A','N/A','0','Boa',26,57),(252,'2025-10-14 16:44:58','N/A','N/A','N/A','N/A','0','Boa',26,57),(253,'2025-10-14 16:45:08','N/A','N/A','N/A','N/A','0','Boa',26,57),(254,'2025-10-14 16:45:18','N/A','N/A','N/A','N/A','0','Boa',26,57),(255,'2025-10-14 16:45:28','N/A','N/A','N/A','N/A','0','Boa',26,57),(256,'2025-10-14 16:45:38','N/A','N/A','N/A','N/A','0','Boa',26,58),(257,'2025-10-14 16:45:48','N/A','N/A','N/A','N/A','0','',26,58),(258,'2025-10-14 16:45:58','N/A','N/A','N/A','N/A','0','Boa',26,58),(259,'2025-10-14 17:28:13','N/A','N/A','N/A','N/A','0','',0,0),(260,'2025-10-14 17:28:23','N/A','N/A','N/A','N/A','0','Boa',0,0),(261,'2025-10-14 17:28:33','N/A','N/A','N/A','N/A','0','Boa',0,52),(262,'2025-10-14 17:28:43','N/A','N/A','N/A','N/A','0','Boa',0,52),(263,'2025-10-14 17:28:53','N/A','N/A','N/A','N/A','0','Boa',0,52),(264,'2025-10-14 17:29:03','N/A','N/A','N/A','N/A','0','Boa',0,52),(265,'2025-10-14 17:29:13','N/A','N/A','N/A','N/A','0','Boa',0,53),(266,'2025-10-14 17:29:23','N/A','N/A','N/A','N/A','0','Boa',0,53),(267,'2025-10-14 17:29:33','N/A','N/A','N/A','N/A','0','Boa',0,54),(268,'2025-10-14 17:29:43','N/A','N/A','N/A','N/A','0','Boa',0,54),(269,'2025-10-14 17:29:53','N/A','N/A','N/A','N/A','0','Boa',0,54),(270,'2025-10-14 17:30:03','N/A','N/A','N/A','N/A','0','Boa',0,55),(271,'2025-10-14 17:30:13','N/A','N/A','N/A','N/A','0','Boa',0,55),(272,'2025-10-14 17:30:23','N/A','N/A','N/A','N/A','0','Boa',0,55),(273,'2025-10-14 17:30:34','N/A','N/A','N/A','N/A','0','Boa',0,55),(274,'2025-10-14 17:30:44','N/A','N/A','N/A','N/A','0','Boa',0,55),(275,'2025-10-14 17:30:54','N/A','N/A','N/A','N/A','0','Boa',0,56),(276,'2025-10-14 17:31:04','N/A','N/A','N/A','N/A','0','Boa',0,56),(277,'2025-10-14 17:31:14','N/A','N/A','N/A','N/A','0','Boa',0,56),(278,'2025-10-14 17:31:24','N/A','N/A','N/A','N/A','0','Boa',0,56),(279,'2025-10-14 17:31:34','N/A','N/A','N/A','N/A','0','Boa',0,56),(280,'2025-10-14 17:31:44','N/A','N/A','N/A','N/A','0','Boa',0,56),(281,'2025-10-14 17:31:54','N/A','N/A','N/A','N/A','0','Boa',0,56),(282,'2025-10-14 17:32:04','N/A','N/A','N/A','N/A','0','Boa',0,56),(283,'2025-10-14 17:32:14','N/A','N/A','N/A','N/A','0','Boa',0,57),(284,'2025-10-14 17:32:24','N/A','N/A','N/A','N/A','0','Boa',0,57),(285,'2025-10-14 17:32:34','N/A','N/A','N/A','N/A','0','Boa',0,57),(286,'2025-10-14 17:32:44','N/A','N/A','N/A','N/A','0','Boa',0,57),(287,'2025-10-14 17:32:54','N/A','N/A','N/A','N/A','0','Boa',0,57);
/*!40000 ALTER TABLE `sensores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'camila_db'
--

--
-- Dumping routines for database 'camila_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-20 10:29:56
