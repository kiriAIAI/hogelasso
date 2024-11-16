-- MySQL dump 10.11
--
-- Host: localhost    Database: kakikko
-- ------------------------------------------------------
-- Server version	5.0.45-community-nt

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES gbk */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `book_id` int(11) NOT NULL auto_increment,
  `book_title` varchar(255) NOT NULL,
  `book_content` text NOT NULL,
  `book_category` varchar(255) NOT NULL,
  `book_price` decimal(10,2) NOT NULL,
  `book_cover_image` varchar(255) NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY  (`book_id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `transaction_id` int(11) NOT NULL auto_increment,
  `book_id` int(11) NOT NULL,
  `buyer_id` int(11) default NULL,
  `seller_id` int(11) default NULL,
  `transaction_date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`transaction_id`),
  KEY `book_id` (`book_id`),
  KEY `buyer_id` (`buyer_id`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`id`),
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_security_questions`
--

DROP TABLE IF EXISTS `user_security_questions`;
CREATE TABLE `user_security_questions` (
  `user_id` int(11) default NULL,
  `question1` varchar(255) NOT NULL,
  `answer1` varchar(255) NOT NULL,
  `question2` varchar(255) NOT NULL,
  `answer2` varchar(255) NOT NULL,
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_security_questions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_security_questions`
--

LOCK TABLES `user_security_questions` WRITE;
/*!40000 ALTER TABLE `user_security_questions` DISABLE KEYS */;
INSERT INTO `user_security_questions` VALUES (1,'СѧУ�Εr�Τ�����','ƽƽ','�����Ή�','��֤��ʤꤿ��'),(2,'СѧУ�Εr�Τ�����','111','��У�Εr�Τ�����','111'),(3,'СѧУ�Εr�Τ�����','123','��У�Εr�Τ�����','123'),(4,'СѧУ�Εr�Τ�����','123','��У�Εr�Τ�����','123'),(5,'СѧУ�Εr�Τ�����','123','��У�Εr�Τ�����','123'),(6,'СѧУ�Εr�Τ�����','test1','�����Ή�','test1');
/*!40000 ALTER TABLE `user_security_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'��ƽ','xiangping@gmail.com','xiangping'),(2,'trump','president@gmail.com','maga'),(3,'123','123@gmail.com','123'),(4,'test','9196723@ha.com','test'),(5,'222','222@gmail.com','222'),(6,'test1','test1@gmail.com','test1');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-15  6:13:49
