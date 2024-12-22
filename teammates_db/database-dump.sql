-- MySQL dump 10.13  Distrib 9.1.0, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: teammates
-- ------------------------------------------------------
-- Server version	9.0.1

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
-- Table structure for table `Questionnaires`
--

DROP TABLE IF EXISTS `Questionnaires`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Questionnaires` (
  `author_public_id` int NOT NULL,
  `id` varchar(36) DEFAULT NULL,
  `header` varchar(127) DEFAULT NULL,
  `description` text,
  `image_path` varchar(255) DEFAULT NULL,
  `game` varchar(63) NOT NULL,
  KEY `author_public_id` (`author_public_id`),
  CONSTRAINT `Questionnaires_ibfk_1` FOREIGN KEY (`author_public_id`) REFERENCES `Users` (`public_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questionnaires`
--

LOCK TABLES `Questionnaires` WRITE;
/*!40000 ALTER TABLE `Questionnaires` DISABLE KEYS */;
INSERT INTO `Questionnaires` VALUES (1,'b919dd3b-a8d8-4d71-97f3-19c8a3b33e1c','Wanna find teammate Dota 2','string','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/b919dd3b-a8d8-4d71-97f3-19c8a3b33e1c.jpg','CS2'),(1,'2dd49f69-6359-4416-9d02-3cb262f8fba9','Wanna find tefsdfhhdfate Dota 2','string','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/2dd49f69-6359-4416-9d02-3cb262f8fba9.jpg','CS2'),(1,'35238b66-78bb-4621-b8c3-cc21e8b3be86','Wafhhdfate Dota 2','string','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/35238b66-78bb-4621-b8c3-cc21e8b3be86.jpg','CS2'),(1,'391f1b33-c523-4466-bda8-484e3392d87e','Wafhhdfate Dodffdghgfhfvhbfjjta 2','string','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/391f1b33-c523-4466-bda8-484e3392d87e.jpg','CS2'),(1,'8a3413ea-781c-4574-8887-1206d8deb0a3','Wanna find fdgdfgdfgdfteammate Dota 2','ssdfdsfdsf','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/8a3413ea-781c-4574-8887-1206d8deb0a3.jpg','CS2'),(1,'41632fea-2a14-43e9-8117-8bf5341d1c4e','Wanna find fdgdfgdfgdfteammate Dota 2','ssdfdsfdsf','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/41632fea-2a14-43e9-8117-8bf5341d1c4e.jpg','CS2'),(1,'03dbfa8d-9223-41b9-8697-9b46ecf87689','Wanna find teammate Dota 2','string','/Users/decobraz/Coding/TeamMates/questionnaires_service/questionnaires_photos/03dbfa8d-9223-41b9-8697-9b46ecf87689.jpg','CS2'),(1,'fdc7815c-a210-47a2-9bcc-94abc994f31d','Wanna find teammate Dota 2','string','/questionnaires_service/questionnaires_photos/fdc7815c-a210-47a2-9bcc-94abc994f31d.jpg','CS2'),(1,'b00b1fd1-ae21-455d-b77e-adbf08ec7bd6','Wanna fdsfdsfmate Dota 2','string','/questionnaires_service/questionnaires_photos/b00b1fd1-ae21-455d-b77e-adbf08ec7bd6.jpg','CS2'),(1,'3ce4fb4e-27a3-4111-8f98-3a86620f4d6d','Wannasdfdgdgsgdsd teammate Dota 2','string','/questionnaires_service/questionnaires_photos/3ce4fb4e-27a3-4111-8f98-3a86620f4d6d.jpg','CS2'),(1,'d20dda6a-05f8-4564-9efe-55fb2ebaf5b0','Wannasdfdgdgsgdsd teammate Dota 2','string','/questionnaires_service/questionnaires_photos/d20dda6a-05f8-4564-9efe-55fb2ebaf5b0.jpg','CS2'),(1,'a46756a4-907e-4c8f-a382-927c8d6d60ce','Wannasdfdgdgsgdsd teammate Dota 2','string','/questionnaires_service/questionnaires_photos/a46756a4-907e-4c8f-a382-927c8d6d60ce.jpg','CS2'),(1,'af321d87-d5ac-4f44-b856-a5b762797b61','Wanna find teammate Dota 2','string','http://localhost:8000/questionnaire/questionnaires_photos/af321d87-d5ac-4f44-b856-a5b762797b61.jpg','CS2'),(1,'33acadf1-436f-49a9-ad46-674fa6f7e689','Wanna find teammate Dota 2','string','localhost/questionnaires_photos/33acadf1-436f-49a9-ad46-674fa6f7e689.jpg','CS2'),(1,'7dbf0ad3-bb6e-4b19-a873-64010b716bd0','Wanna find teammate Dota 2','string','/questionnaire/questionnaires_photos/7dbf0ad3-bb6e-4b19-a873-64010b716bd0.jpg','CS2'),(1,'9225cbc6-f3ec-46de-95cb-29b32173b826','Wanna find teammate Dota 2','string','/questionnaires_photos/9225cbc6-f3ec-46de-95cb-29b32173b826.jpg','CS2'),(1,'5ec9e522-7c6d-47eb-bdfa-bc2d019ac82b','Wanna find teascscffsdmmate Dota 2','string','/questionnaires_photos/5ec9e522-7c6d-47eb-bdfa-bc2d019ac82b.jpg','CS2'),(1,'76230e7c-40d7-4424-9343-13ad0fe13018','Wanna find teascscffsdmmate Dota 2','string','[\'http:\', \'\', \'localhost:8000\']/questionnaires_photos/76230e7c-40d7-4424-9343-13ad0fe13018.jpg','CS2'),(1,'762d49b0-55dd-42c2-9e08-d8e86adf8895','Wanna find teascscffsdmmate Dota 2','string','http:localhost:8000/questionnaires_photos/762d49b0-55dd-42c2-9e08-d8e86adf8895.jpg','CS2'),(1,'c1aa96cd-1d92-4628-8bd0-f918d8314f4e','Wanna find teammate Dota 2','string','http:0.0.0.0:8000/questionnaires_photos/c1aa96cd-1d92-4628-8bd0-f918d8314f4e.jpg','CS2'),(1,'68a9e4e7-8941-43de-a004-6cedf40dae73','Wanna find teammate Dota 2','string','http:0.0.0.0:8000/questionnaires_photos/68a9e4e7-8941-43de-a004-6cedf40dae73.jpg','CS2');
/*!40000 ALTER TABLE `Questionnaires` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `public_id` int NOT NULL AUTO_INCREMENT,
  `secret_id` varchar(36) DEFAULT NULL,
  `nickname` varchar(127) NOT NULL,
  `email` varchar(255) NOT NULL,
  `description` text,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`public_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'fb6d4b27-5cb1-4207-bce1-8b461921142e','abia','abobasf@gmail.com','adfdfdsg','asfdsfsdgdsgdgsdg');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UsersPasswords`
--

DROP TABLE IF EXISTS `UsersPasswords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UsersPasswords` (
  `public_id` int NOT NULL,
  `password` varchar(64) NOT NULL,
  UNIQUE KEY `public_id` (`public_id`),
  CONSTRAINT `UsersPasswords_ibfk_1` FOREIGN KEY (`public_id`) REFERENCES `Users` (`public_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UsersPasswords`
--

LOCK TABLES `UsersPasswords` WRITE;
/*!40000 ALTER TABLE `UsersPasswords` DISABLE KEYS */;
INSERT INTO `UsersPasswords` VALUES (1,'d620fe2cdb06cfd0eff49a33db7c876ebb64ac51a3c6b6f8e68d23db1bc022f0');
/*!40000 ALTER TABLE `UsersPasswords` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-22 21:48:57
