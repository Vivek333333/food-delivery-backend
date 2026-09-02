-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: mfd
-- ------------------------------------------------------
-- Server version	8.0.46

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

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `uid` int NOT NULL,
  `pid` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (3,2),(3,2),(3,1),(3,1),(4,1),(4,2),(4,2),(4,1),(11,20),(9,19);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `catid` int NOT NULL AUTO_INCREMENT,
  `rid` int NOT NULL,
  `cat` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `images` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`catid`),
  KEY `rid` (`rid`),
  CONSTRAINT `rid` FOREIGN KEY (`rid`) REFERENCES `restaurants` (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (14,20,'Pasta','cat_ea96e10cb88b4cc7a35be5b9cf67b84a.jpeg'),(15,25,'Papad','cat_a148a42cb3e04fe3ad56b8c7e406c494.jpeg'),(16,25,'French Fries ','cat_57c63c2ac547427cb2dbe17e90915ab0.jpeg'),(17,25,'Beverages','cat_1135469bc8c1451ea65383fc13565fe6.jpeg'),(18,25,'Pulav','cat_c4f0ce0925664194979fd82c0f424a2d.jpeg'),(19,25,'Sp. Matka Biryani','cat_e5804e6a167e43a184faae5eada6c04a.jpeg'),(20,25,'Pav Bhaji','cat_2b6f80a379ff420fbc9fa14ac6b6203f.jpeg'),(21,25,'Surati Ghotala','cat_93ca4115eb0d4b6182b1437b7a8a7e7f.jpeg'),(22,25,'Chinese Fusion','cat_e4e7e7e1c4204d10b5612416067b212d.jpeg'),(23,25,'Uttapam','cat_647181cb2d7445de832799db22f249dc.jpeg'),(24,25,'Mr. Dosa G Sp.','cat_4d0feaab63bc459aad90d567b6d0f815.jpeg'),(25,25,'Mysore Dosa (Separate Bhaji)','cat_74ea2bb1a3dc4b70a3321bc4dafdd017.jpeg'),(26,25,'Fancy Dosa','cat_40b810a7e8b94279be2660bdb39589ee.jpeg'),(27,25,'Masala Dosa','cat_0e411eb4e17847d9a2db5281854a40d0.jpeg'),(28,25,'Plain Dosa','cat_9eb16104f14e4a19bf5a9988d5b0d823.jpeg');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `oid` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `uid` int NOT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `paymenttype` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`oid`),
  KEY `pid` (`pid`),
  KEY `orders_ibfk_1` (`uid`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,2,522,1,'mansa','COD','delivered'),(46,1,9,200,1,'CJ4X+CFV Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(47,17,9,85500,14,'CJ4X+QGH Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(48,17,9,85500,3,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(49,17,9,85500,1,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(50,18,9,250,2,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(51,18,9,250,2,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(52,18,9,250,3,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(53,18,9,250,1,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(54,19,9,100,1,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(55,19,9,100,3,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(56,20,9,86,2,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(57,19,9,100,4,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(58,19,9,100,8,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(59,19,9,100,9,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(60,19,9,100,10,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(61,19,9,100,6,'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845','COD','delivered'),(63,19,2,100,2,'Fi','COD','delivered'),(64,18,2,250,1,'Fi','COD','delivered'),(65,19,2,100,3,'Fi','COD','delivered'),(66,20,2,86,1,'Fi','COD','delivered'),(67,18,2,250,1,'Fi','COD','delivered'),(68,21,2,240,2,'Fi','COD','delivered'),(69,18,2,250,1,'Fi','COD','delivered'),(70,19,2,100,2,'Fi','COD','delivered');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `rid` int NOT NULL,
  `catid` int NOT NULL,
  `product` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `price` int NOT NULL,
  `images` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `rid` (`rid`),
  KEY `products_ibfk_2` (`catid`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `restaurants` (`rid`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`catid`) REFERENCES `category` (`catid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurants` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `rname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `images` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurants`
--

LOCK TABLES `restaurants` WRITE;
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` VALUES (20,'Pizza House','rest_163bae1de93844888d202f2bdbade15e.jpeg'),(25,'Mr. Dosa G','rest_ed280a20e6ab4b82b6f389a6d0b07b24.jpeg');
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'Deepu','9978590175'),(7,'Manan','7359237995'),(9,'Vivek','8511916534'),(10,'Visu','7096220564');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-02  5:11:07
