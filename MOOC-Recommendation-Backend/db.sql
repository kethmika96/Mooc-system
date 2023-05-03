-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: video_recommendation
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `video_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `video_id` (`video_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`video_id`) REFERENCES `videos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES (1,2,1,1),(14,1,1,2),(15,3,1,3),(16,1,3,4),(17,3,3,5),(18,2,3,6),(19,2,4,7),(20,1,4,8),(21,3,4,9),(22,2,2,10),(23,3,2,11),(24,1,2,12),(25,2,1,13);
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendations`
--

DROP TABLE IF EXISTS `recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `video_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `video_id` (`video_id`),
  CONSTRAINT `recommendations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `recommendations_ibfk_2` FOREIGN KEY (`video_id`) REFERENCES `videos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendations`
--

LOCK TABLES `recommendations` WRITE;
/*!40000 ALTER TABLE `recommendations` DISABLE KEYS */;
INSERT INTO `recommendations` VALUES (1,1,1),(2,1,2),(3,1,13),(4,1,17),(5,1,18),(6,1,1),(7,1,3),(8,1,16),(9,1,17),(10,1,18),(11,1,1),(12,1,3),(13,1,13),(14,1,17),(15,1,18),(16,1,1),(17,1,2),(18,1,3),(19,1,17),(20,1,18),(21,1,1),(22,1,2),(23,1,16),(24,1,17),(25,1,18),(26,1,1),(27,1,2),(28,1,13),(29,1,17),(30,1,18),(31,1,1),(32,1,13),(33,1,16),(34,1,17),(35,1,18);
/*!40000 ALTER TABLE `recommendations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `technologies`
--

DROP TABLE IF EXISTS `technologies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `technologies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tech` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `technologies`
--

LOCK TABLES `technologies` WRITE;
/*!40000 ALTER TABLE `technologies` DISABLE KEYS */;
INSERT INTO `technologies` VALUES (1,'Java'),(2,'Node JS'),(3,'JavaScript'),(4,'Python');
/*!40000 ALTER TABLE `technologies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `email` varchar(32) DEFAULT NULL,
  `password` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'nisal','nisal@gmail.com','12345'),(2,'chinthana','chinthana@gmail.com','23456'),(3,'perera','perera@gmail.com','34567'),(4,'nimal','nimal@gmail.com','45678');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_categories`
--

DROP TABLE IF EXISTS `video_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_categories`
--

LOCK TABLES `video_categories` WRITE;
/*!40000 ALTER TABLE `video_categories` DISABLE KEYS */;
INSERT INTO `video_categories` VALUES (1,'Talking Heads Style'),(2,'Coding Style'),(3,'Animations Style'),(4,'Presentation Slides Style');
/*!40000 ALTER TABLE `video_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `thumb` varchar(255) DEFAULT NULL,
  `category` int DEFAULT NULL,
  `tech` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category` (`category`),
  KEY `tech` (`tech`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`category`) REFERENCES `video_categories` (`id`),
  CONSTRAINT `videos_ibfk_2` FOREIGN KEY (`tech`) REFERENCES `technologies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES (1,'A_Nested_Attention_Neural_Hybrid_Model_for_Grammatical_Error_Correction_','videos\\A_Nested_Attention_Neural_Hybrid_Model_for_Grammatical_Error_Correction_.mp4','videos\\thumbs\\A_Nested_Attention_Neural_Hybrid_Model_for_Grammatical_Error_Correction_thumb.jpg',1,1),(2,'A_Principled_Framework_for_Evaluating_Summarizers_Comparing_Models_of_Summary_Quality_against_Human','videos\\A_Principled_Framework_for_Evaluating_Summarizers_Comparing_Models_of_Summary_Quality_against_Human.mp4','videos\\thumbs\\A_Principled_Framework_for_Evaluating_Summarizers_Comparing_Models_of_Summary_Quality_against_Humanthumb.jpg',4,1),(3,'Abstract_Meaning_Representation_Parsing_using_LSTM_Recurrent_Neural_Networks_','videos\\Abstract_Meaning_Representation_Parsing_using_LSTM_Recurrent_Neural_Networks_.mp4','videos\\thumbs\\Abstract_Meaning_Representation_Parsing_using_LSTM_Recurrent_Neural_Networks_thumb.jpg',2,1),(4,'Abstractive_Document_Summarization_with_a_Graph_Based_Attentional_Neural_Model_','videos\\Abstractive_Document_Summarization_with_a_Graph_Based_Attentional_Neural_Model_.mp4','videos\\thumbs\\Abstractive_Document_Summarization_with_a_Graph_Based_Attentional_Neural_Model_thumb.jpg',3,1),(5,'Adversarial_Multi_task_Learning_for_Text_Classification_','videos\\Adversarial_Multi_task_Learning_for_Text_Classification_.mp4','videos\\thumbs\\Adversarial_Multi_task_Learning_for_Text_Classification_thumb.jpg',4,2),(6,'An_Unsupervised_Neural_Attention_Model_for_Aspect_Extraction_','videos\\An_Unsupervised_Neural_Attention_Model_for_Aspect_Extraction_.mp4','videos\\thumbs\\An_Unsupervised_Neural_Attention_Model_for_Aspect_Extraction_thumb.jpg',2,2),(7,'Attention_over_Attention_Neural_Networks_for_Reading_Comprehension_','videos\\Attention_over_Attention_Neural_Networks_for_Reading_Comprehension_.mp4','videos\\thumbs\\Attention_over_Attention_Neural_Networks_for_Reading_Comprehension_thumb.jpg',3,2),(8,'Cross_Sentence_N_ary_Relation_Extraction_with_Graph_LSTMs_','videos\\Cross_Sentence_N_ary_Relation_Extraction_with_Graph_LSTMs_.mp4','videos\\thumbs\\Cross_Sentence_N_ary_Relation_Extraction_with_Graph_LSTMs_thumb.jpg',1,2),(9,'Deep_Keyphrase_Generation_','videos\\Deep_Keyphrase_Generation_.mp4','videos\\thumbs\\Deep_Keyphrase_Generation_thumb.jpg',2,3),(10,'Discourse_Mode_Identification_in_Essays_','videos\\Discourse_Mode_Identification_in_Essays_.mp4','videos\\thumbs\\Discourse_Mode_Identification_in_Essays_thumb.jpg',3,3),(11,'Diversity_driven_attention_model_for_query_based_abstractive_summarization_','videos\\Diversity_driven_attention_model_for_query_based_abstractive_summarization_.mp4','videos\\thumbs\\Diversity_driven_attention_model_for_query_based_abstractive_summarization_thumb.jpg',4,3),(12,'Exploring_Neural_Text_Simplification_Models_','videos\\Exploring_Neural_Text_Simplification_Models_.mp4','videos\\thumbs\\Exploring_Neural_Text_Simplification_Models_thumb.jpg',1,3),(13,'Friendships_Rivalries_and_Trysts_Characterizing_Relations_between_Ideas_in_Texts_Chenhao_Tan','videos\\Friendships_Rivalries_and_Trysts_Characterizing_Relations_between_Ideas_in_Texts_Chenhao_Tan.mp4','videos\\thumbs\\Friendships_Rivalries_and_Trysts_Characterizing_Relations_between_Ideas_in_Texts_Chenhao_Tanthumb.jpg',2,4),(14,'Get_To_The_Point_Summarization_with_Pointer_Generator_Networks_','videos\\Get_To_The_Point_Summarization_with_Pointer_Generator_Networks_.mp4','videos\\thumbs\\Get_To_The_Point_Summarization_with_Pointer_Generator_Networks_thumb.jpg',3,4),(15,'Neural_AMR_Sequence_to_Sequence_Models_for_Parsing_and_Generation_','videos\\Neural_AMR_Sequence_to_Sequence_Models_for_Parsing_and_Generation_.mp4','videos\\thumbs\\Neural_AMR_Sequence_to_Sequence_Models_for_Parsing_and_Generation_thumb.jpg',1,4),(16,'Selective_Encoding_for_Abstractive_Sentence_Summarization_','videos\\Selective_Encoding_for_Abstractive_Sentence_Summarization_.mp4','videos\\thumbs\\Selective_Encoding_for_Abstractive_Sentence_Summarization_thumb.jpg',1,4),(17,'Supervised_Learning_of_Automatic_Pyramid_for_Optimization_Based_Multi_Document_Summarization','videos\\Supervised_Learning_of_Automatic_Pyramid_for_Optimization_Based_Multi_Document_Summarization.mp4','videos\\thumbs\\Supervised_Learning_of_Automatic_Pyramid_for_Optimization_Based_Multi_Document_Summarizationthumb.jpg',4,4),(18,'TextFlow_A_Text_Similarity_Measure_based_on_Continuous_Sequences_','videos\\TextFlow_A_Text_Similarity_Measure_based_on_Continuous_Sequences_.mp4','videos\\thumbs\\TextFlow_A_Text_Similarity_Measure_based_on_Continuous_Sequences_thumb.jpg',2,4),(19,'Towards_an_Automatic_Turing_Test_Learning_to_Evaluate_Dialogue_Responses_','videos\\Towards_an_Automatic_Turing_Test_Learning_to_Evaluate_Dialogue_Responses_.mp4','videos\\thumbs\\Towards_an_Automatic_Turing_Test_Learning_to_Evaluate_Dialogue_Responses_thumb.jpg',1,4),(20,'Visualizing_and_Understanding_Neural_Machine_Translation_','videos\\Visualizing_and_Understanding_Neural_Machine_Translation_.mp4','videos\\thumbs\\Visualizing_and_Understanding_Neural_Machine_Translation_thumb.jpg',4,4);
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-01 18:16:55
