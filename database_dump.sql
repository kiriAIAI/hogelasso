-- MySQL dump 10.11
--
-- Host: localhost    Database: kakikko
-- ------------------------------------------------------
-- Server version	5.0.45-community-nt

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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Sample Book','This is a test book.','Test Category','10.00','test_cover.jpg',1),(2,'Python入門','Pythonプログラミングを基礎から学べる初心者向けのガイドです。','プログラミング','2200.00','/images/python_intro.jpg',20000),(3,'MySQL完全攻略','MySQLのデータベース管理を深く理解するための実践的な書籍です。','データベース','3500.00','/images/mysql_mastery.jpg',20000),(4,'ウェブ開発の基礎','HTML、CSS、JavaScriptの基本を学べる初心者向けの一冊です。','ウェブ開発','2800.00','/images/web_basics.jpg',20000),(5,'AIと機械学習の基礎','人工知能と機械学習の基本的な仕組みをわかりやすく解説します。','人工知能','4500.00','/images/ai_ml.jpg',20000),(6,'サイバーセキュリティの基礎','ネットワークや情報セキュリティの重要な概念を網羅した一冊です。','セキュリティ','3200.00','/images/cybersecurity.jpg',20000),(7,'あああ','ああ','lifestyle','280000.00','GGG.jpg',20000),(8,'直った！！','aa','lifestyle','0.00','G (3).jpg',20000),(9,'aaa','aaaa','lifestyle','0.00','unnamed.jpg',20000),(10,'aa','aa','lifestyle','280000.00','unnamed.jpg',20000),(11,'a','aaa','certification','280000.00','G (3).jpg',20000),(12,'aa','aa','lifestyle','280000.00','GGG.jpg',20000),(13,'a','aaa','lifestyle','0.00','GGG.jpg',20000),(14,'aa','aa','social','280000.00','スクショ.png',20000),(15,'a','aaa','history','280000.00','file',20000),(16,'a','aa','lifestyle','0.00','GGG.jpg',20000),(17,'a','aa','social','0.00','file',20000),(18,'a','aa','history','280000.00','GGG.jpg',20000),(19,'きたこれ','あああ','lifestyle','222.00','G (3).jpg',20000),(20,'皆ホントにありがとう','aaa','lifestyle','0.00','GGG.jpg',100000),(21,'今日も今日とて','aa','certification','280000.00','スクリーンショット 2023-03-19 004028.png',100000),(22,'基本情報取らなければならない','ああ','lifestyle','303000.00','スクリーンショット 2024-04-26 224626.png',100000),(23,'kakikko','あああ','lifestyle','280000.00','スクリーンショット 2024-11-13 190333.png',100000),(24,'test','<div style=\"text-align: right;\"><i style=\"font-size: 1.7rem; color: var(--dark-gray);\">test</i></div>','literature','3000.00','133571682160460525.jpg',1),(25,'test2','test2','history','2000.00','133590530057476704.jpg',1),(26,'<font color=\"#f50000\">順調の極み</font>','<div style=\"text-align: center;\"><span style=\"font-size: 1rem;\"><span style=\"font-size: 2rem;\"><font color=\"#0008ff\"><b>順調の極み</b></font></span></span></div>','lifestyle','303000.00','26_image_fx_ (3).jpg',20000),(27,'aa','aaa','lifestyle','303000.00','27_image_fx_ (3).jpg',20000),(28,'aa','aaa','lifestyle','303000.00','28_image_fx_ (4).jpg',20000),(29,'<font color=\"#ff0000\">順調の極み</font>','<div style=\"text-align: center;\"><span style=\"font-size: 2rem;\"><b style=\"\"><font color=\"#0011ff\">順調の極み</font></b></span></div><div style=\"text-align: center;\"><span style=\"font-size: 32px;\"><b style=\"\"><u style=\"\"><font color=\"#00d624\"></font></u><span style=\"font-size: 2.1rem;\"><span style=\"font-size: 1.5rem;\"><u style=\"\"><font color=\"#00d624\">マジで天才←これ</font></u></span></span></b></span></div>','lifestyle','100.00','29_image_fx_ (3).jpg',20000);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`comment_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,20000,23,'はろ','2024-11-29 07:04:23'),(2,20000,28,'スマホ溶接中？','2024-11-29 07:21:02'),(3,100000,28,'そうっぽい','2024-11-29 07:21:32'),(4,100000,14,'わわわ','2024-11-29 07:27:59'),(5,20000,14,'wawaaaa','2024-11-29 07:28:33');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direct_messages`
--

DROP TABLE IF EXISTS `direct_messages`;
CREATE TABLE `direct_messages` (
  `message_id` int(11) NOT NULL auto_increment,
  `sender_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`message_id`),
  KEY `sender_id` (`sender_id`),
  KEY `recipient_id` (`recipient_id`),
  CONSTRAINT `direct_messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  CONSTRAINT `direct_messages_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `direct_messages`
--

LOCK TABLES `direct_messages` WRITE;
/*!40000 ALTER TABLE `direct_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `direct_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes` (
  `like_id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`like_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
CREATE TABLE `quizzes` (
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `points` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,2,1,'2024-11-15 03:00:00'),(2,1,20000,20000,'2024-11-15 12:23:22'),(3,1,2,20000,'2024-11-16 04:04:46'),(4,1,99999,20000,'2024-11-16 04:05:46'),(5,1,99999,20000,'2024-11-16 04:17:32'),(6,1,99999,20000,'2024-11-16 05:04:32'),(7,1,99999,NULL,'2024-11-16 05:46:07'),(8,1,99999,1,'2024-11-16 05:58:44'),(9,6,99999,20000,'2024-11-16 06:06:09'),(10,4,2,20000,'2024-11-16 06:06:43'),(11,23,1,100000,'2024-11-21 02:15:44'),(12,23,1,100000,'2024-11-21 02:15:49'),(13,24,1,1,'2024-11-21 02:18:39');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profiles`
--

DROP TABLE IF EXISTS `user_profiles`;
CREATE TABLE `user_profiles` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(255) default NULL,
  `last_name` varchar(255) default NULL,
  `birthday` date default NULL,
  `gender` varchar(50) default NULL,
  `address` varchar(255) default NULL,
  `phone` varchar(50) default NULL,
  `bio` text,
  `profile_image` varchar(255) default 'default-profile.jpg',
  PRIMARY KEY  (`user_id`),
  CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_profiles`
--

LOCK TABLES `user_profiles` WRITE;
/*!40000 ALTER TABLE `user_profiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_profiles` ENABLE KEYS */;
UNLOCK TABLES;


-- Table structure for table `user_quiz_scores`
--

DROP TABLE IF EXISTS `user_quiz_scores`;
CREATE TABLE `user_quiz_scores` (
  `user_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_quiz_scores`
--

LOCK TABLES `user_quiz_scores` WRITE;
/*!40000 ALTER TABLE `user_quiz_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_quiz_scores` ENABLE KEYS */;
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
INSERT INTO `user_security_questions` VALUES (1,'小学校の時のあだ名','平平','将来の夢','金持ちなりたい'),(2,'小学校の時のあだ名','111','高校の時のあだ名','111'),(3,'小学校の時のあだ名','123','高校の時のあだ名','123'),(4,'小学校の時のあだ名','123','高校の時のあだ名','123'),(5,'小学校の時のあだ名','123','高校の時のあだ名','123'),(6,'小学校の時のあだ名','test1','将来の夢','test1'),(100000,'小学校の時のあだ名','ぼで','高校の時のあだ名','ぼで'),(100001,'小学校の時のあだ名','haha','高校の時のあだ名','haha');
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
) ENGINE=InnoDB AUTO_INCREMENT=100002 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'翔平','xiangping@gmail.com','xiangping'),(2,'trump','president@gmail.com','maga'),(3,'123','123@gmail.com','123'),(4,'test','9196723@ha.com','test'),(5,'222','222@gmail.com','222'),(6,'test1','test1@gmail.com','test1'),(20000,'BuyerUser','buyer@example.com','buyerpassword'),(99999,'kazuto','kazuto@gmail.com','kazuto0330'),(100000,'bode','bode@gmail.com','bode'),(100001,'haha','haha@qq.com','haha');
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

-- Dump completed on 2024-11-29  7:47:36
