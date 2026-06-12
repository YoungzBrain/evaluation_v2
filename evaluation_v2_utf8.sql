-- MySQL dump 10.13  Distrib 9.7.0, for Win64 (x86_64)
--
-- Host: localhost    Database: evaluation_v2
-- ------------------------------------------------------
-- Server version	9.7.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '6aa3bb18-4983-11f1-8248-d481d78caa7e:1-380';

--
-- Table structure for table `accounts_department`
--

DROP TABLE IF EXISTS `accounts_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_department`
--

LOCK TABLES `accounts_department` WRITE;
/*!40000 ALTER TABLE `accounts_department` DISABLE KEYS */;
INSERT INTO `accounts_department` VALUES (1,'INFOTEL','Informatique et Telecommunication','2026-06-05 20:21:29.876308','2026-06-05 20:21:29.876308'),(2,'ENREN','ENERGY RENOUVELABLE','2026-06-05 20:22:27.549539','2026-06-05 20:22:27.549539');
/*!40000 ALTER TABLE `accounts_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_level`
--

DROP TABLE IF EXISTS `accounts_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_level` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `accounts_level_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_level`
--

LOCK TABLES `accounts_level` WRITE;
/*!40000 ALTER TABLE `accounts_level` DISABLE KEYS */;
INSERT INTO `accounts_level` VALUES (1,'Annee 1',1),(2,'Annee 2',2),(3,'Annee 3',3),(4,'Annee 4',4),(5,'Annee 5',5);
/*!40000 ALTER TABLE `accounts_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_specialization`
--

DROP TABLE IF EXISTS `accounts_specialization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_specialization` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_specialization_name_department_id_10013917_uniq` (`name`,`department_id`),
  KEY `accounts_specializat_department_id_e0896fc0_fk_accounts_` (`department_id`),
  CONSTRAINT `accounts_specializat_department_id_e0896fc0_fk_accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_specialization`
--

LOCK TABLES `accounts_specialization` WRITE;
/*!40000 ALTER TABLE `accounts_specialization` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_specialization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_studentprofile`
--

DROP TABLE IF EXISTS `accounts_studentprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_studentprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `department_id` bigint DEFAULT NULL,
  `level_id` bigint DEFAULT NULL,
  `specialization_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_studentprof_department_id_340eacd0_fk_accounts_` (`department_id`),
  KEY `accounts_studentprofile_level_id_983f1d8a_fk_accounts_level_id` (`level_id`),
  KEY `accounts_studentprof_specialization_id_d313cb07_fk_accounts_` (`specialization_id`),
  CONSTRAINT `accounts_studentprof_department_id_340eacd0_fk_accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `accounts_studentprof_specialization_id_d313cb07_fk_accounts_` FOREIGN KEY (`specialization_id`) REFERENCES `accounts_specialization` (`id`),
  CONSTRAINT `accounts_studentprofile_level_id_983f1d8a_fk_accounts_level_id` FOREIGN KEY (`level_id`) REFERENCES `accounts_level` (`id`),
  CONSTRAINT `accounts_studentprofile_user_id_04a48d2e_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_studentprofile`
--

LOCK TABLES `accounts_studentprofile` WRITE;
/*!40000 ALTER TABLE `accounts_studentprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_studentprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_teacherprofile`
--

DROP TABLE IF EXISTS `accounts_teacherprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_teacherprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_teacherprofile_user_id_9582b3e8_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_teacherprofile`
--

LOCK TABLES `accounts_teacherprofile` WRITE;
/*!40000 ALTER TABLE `accounts_teacherprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_teacherprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_teacherprofile_departments`
--

DROP TABLE IF EXISTS `accounts_teacherprofile_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_teacherprofile_departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `teacherprofile_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_teacherprofile__teacherprofile_id_depart_509cfbe8_uniq` (`teacherprofile_id`,`department_id`),
  KEY `accounts_teacherprof_department_id_1b2fa9c2_fk_accounts_` (`department_id`),
  CONSTRAINT `accounts_teacherprof_department_id_1b2fa9c2_fk_accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `accounts_teacherprof_teacherprofile_id_9a0b0720_fk_accounts_` FOREIGN KEY (`teacherprofile_id`) REFERENCES `accounts_teacherprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_teacherprofile_departments`
--

LOCK TABLES `accounts_teacherprofile_departments` WRITE;
/*!40000 ALTER TABLE `accounts_teacherprofile_departments` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_teacherprofile_departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1200000$VGFhGgpoHM2BDCdkMw6sdu$e5AwCFxpSDZ53Z06OugP+Tkc0pkI2+ckZM1MdnD5k2E=','2026-06-05 20:22:13.627475',1,'Admin','','','Admin@gmail.com',1,'2026-06-05 09:50:19.038028','student',1),(2,'pbkdf2_sha256$1200000$8L7pzYnHKdOj3a1JBMUiJT$k980mBJCqQA8Y7yONtHOpqq6cZ9tHGZk+GHQ2f7AUt0=','2026-06-05 20:11:46.245016',0,'student@gmail.co','Jeam','Dupont','student@gmail.co',0,'2026-06-05 20:11:44.982404','student',1),(3,'pbkdf2_sha256$1200000$GTz7Flt9qSRp8s772YOzNs$5bLKKcoeQbKUM2ac4eZ6I27P9b3cD0MSmgbs4iviVUs=','2026-06-05 20:24:31.472220',0,'youngzbrain1@gmail.com','JEAN','DUPONT','youngzbrain1@gmail.com',0,'2026-06-05 20:24:30.372112','student',1);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add department',6,'add_department'),(22,'Can change department',6,'change_department'),(23,'Can delete department',6,'delete_department'),(24,'Can view department',6,'view_department'),(25,'Can add level',7,'add_level'),(26,'Can change level',7,'change_level'),(27,'Can delete level',7,'delete_level'),(28,'Can view level',7,'view_level'),(29,'Can add user',11,'add_user'),(30,'Can change user',11,'change_user'),(31,'Can delete user',11,'delete_user'),(32,'Can view user',11,'view_user'),(33,'Can add specialization',8,'add_specialization'),(34,'Can change specialization',8,'change_specialization'),(35,'Can delete specialization',8,'delete_specialization'),(36,'Can view specialization',8,'view_specialization'),(37,'Can add student profile',9,'add_studentprofile'),(38,'Can change student profile',9,'change_studentprofile'),(39,'Can delete student profile',9,'delete_studentprofile'),(40,'Can view student profile',9,'view_studentprofile'),(41,'Can add teacher profile',10,'add_teacherprofile'),(42,'Can change teacher profile',10,'change_teacherprofile'),(43,'Can delete teacher profile',10,'delete_teacherprofile'),(44,'Can view teacher profile',10,'view_teacherprofile'),(45,'Can add course',12,'add_course'),(46,'Can change course',12,'change_course'),(47,'Can delete course',12,'delete_course'),(48,'Can view course',12,'view_course'),(49,'Can add teacher course',13,'add_teachercourse'),(50,'Can change teacher course',13,'change_teachercourse'),(51,'Can delete teacher course',13,'delete_teachercourse'),(52,'Can view teacher course',13,'view_teachercourse'),(53,'Can add question',14,'add_question'),(54,'Can change question',14,'change_question'),(55,'Can delete question',14,'delete_question'),(56,'Can view question',14,'view_question'),(57,'Can add evaluation',16,'add_evaluation'),(58,'Can change evaluation',16,'change_evaluation'),(59,'Can delete evaluation',16,'delete_evaluation'),(60,'Can view evaluation',16,'view_evaluation'),(61,'Can add evaluation pdf',17,'add_evaluationpdf'),(62,'Can change evaluation pdf',17,'change_evaluationpdf'),(63,'Can delete evaluation pdf',17,'delete_evaluationpdf'),(64,'Can view evaluation pdf',17,'view_evaluationpdf'),(65,'Can add answer',15,'add_answer'),(66,'Can change answer',15,'change_answer'),(67,'Can delete answer',15,'delete_answer'),(68,'Can view answer',15,'view_answer');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_course`
--

DROP TABLE IF EXISTS `courses_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `is_general` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id` bigint NOT NULL,
  `level_id` bigint NOT NULL,
  `specialization_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `courses_course_department_id_efdfb636_fk_accounts_department_id` (`department_id`),
  KEY `courses_course_level_id_be3d7088_fk_accounts_level_id` (`level_id`),
  KEY `courses_course_specialization_id_4b7b2518_fk_accounts_` (`specialization_id`),
  CONSTRAINT `courses_course_department_id_efdfb636_fk_accounts_department_id` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `courses_course_level_id_be3d7088_fk_accounts_level_id` FOREIGN KEY (`level_id`) REFERENCES `accounts_level` (`id`),
  CONSTRAINT `courses_course_specialization_id_4b7b2518_fk_accounts_` FOREIGN KEY (`specialization_id`) REFERENCES `accounts_specialization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_course`
--

LOCK TABLES `courses_course` WRITE;
/*!40000 ALTER TABLE `courses_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_teachercourse`
--

DROP TABLE IF EXISTS `courses_teachercourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_teachercourse` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_teachercourse_teacher_id_course_id_1de2d568_uniq` (`teacher_id`,`course_id`),
  KEY `courses_teachercourse_course_id_a677a249_fk_courses_course_id` (`course_id`),
  CONSTRAINT `courses_teachercourse_course_id_a677a249_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `courses_teachercourse_teacher_id_c302c09a_fk_accounts_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_teachercourse`
--

LOCK TABLES `courses_teachercourse` WRITE;
/*!40000 ALTER TABLE `courses_teachercourse` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_teachercourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-06-05 20:21:29.876967','1','INFOTEL',1,'[{\"added\": {}}]',6,1),(2,'2026-06-05 20:22:27.550543','2','ENREN',1,'[{\"added\": {}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','department'),(7,'accounts','level'),(8,'accounts','specialization'),(9,'accounts','studentprofile'),(10,'accounts','teacherprofile'),(11,'accounts','user'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(12,'courses','course'),(13,'courses','teachercourse'),(15,'evaluations','answer'),(16,'evaluations','evaluation'),(17,'evaluations','evaluationpdf'),(14,'questions','question'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-06-05 09:48:50.816807'),(2,'contenttypes','0002_remove_content_type_name','2026-06-05 09:48:50.930756'),(3,'auth','0001_initial','2026-06-05 09:48:51.206860'),(4,'auth','0002_alter_permission_name_max_length','2026-06-05 09:48:51.278786'),(5,'auth','0003_alter_user_email_max_length','2026-06-05 09:48:51.282378'),(6,'auth','0004_alter_user_username_opts','2026-06-05 09:48:51.293903'),(7,'auth','0005_alter_user_last_login_null','2026-06-05 09:48:51.300627'),(8,'auth','0006_require_contenttypes_0002','2026-06-05 09:48:51.306607'),(9,'auth','0007_alter_validators_add_error_messages','2026-06-05 09:48:51.308999'),(10,'auth','0008_alter_user_username_max_length','2026-06-05 09:48:51.321087'),(11,'auth','0009_alter_user_last_name_max_length','2026-06-05 09:48:51.326082'),(12,'auth','0010_alter_group_name_max_length','2026-06-05 09:48:51.349326'),(13,'auth','0011_update_proxy_permissions','2026-06-05 09:48:51.351706'),(14,'auth','0012_alter_user_first_name_max_length','2026-06-05 09:48:51.365700'),(15,'accounts','0001_initial','2026-06-05 09:48:52.354919'),(16,'admin','0001_initial','2026-06-05 09:48:52.515161'),(17,'admin','0002_logentry_remove_auto_add','2026-06-05 09:48:52.526328'),(18,'admin','0003_logentry_add_action_flag_choices','2026-06-05 09:48:52.541789'),(19,'courses','0001_initial','2026-06-05 09:48:52.966231'),(20,'questions','0001_initial','2026-06-05 09:48:52.990956'),(21,'evaluations','0001_initial','2026-06-05 09:48:53.479199'),(22,'sessions','0001_initial','2026-06-05 09:48:53.518904');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('36c34ngeis8kps8r8tzqohlrlqpajx11','.eJxVjEEOwiAQRe_C2hAQLIxL9z0DGWYYqZo2Ke3KeHfbpAvdvvf-f6uE61LT2sqcBlZX5dTpl2WkZxl3wQ8c75OmaVzmIes90Ydtup-4vG5H-3dQsdVtHclJ9mAccwHryUpnJVrErghn8iiYLxAASggmigvZbSiQEIA5E6vPFw41OTc:1wVb5j:WlLDVL3xnIKI-GERY-Hlm4QtK_ejOfe5e9wlDFa2uPI','2026-06-19 20:24:31.477394');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluations_answer`
--

DROP TABLE IF EXISTS `evaluations_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluations_answer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` smallint unsigned DEFAULT NULL,
  `text_answer` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL,
  `evaluation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evaluations_answer_evaluation_id_question_id_279d01ff_uniq` (`evaluation_id`,`question_id`),
  KEY `evaluations_answer_question_id_263cf922_fk_questions_question_id` (`question_id`),
  CONSTRAINT `evaluations_answer_evaluation_id_ebc91e73_fk_evaluatio` FOREIGN KEY (`evaluation_id`) REFERENCES `evaluations_evaluation` (`id`),
  CONSTRAINT `evaluations_answer_question_id_263cf922_fk_questions_question_id` FOREIGN KEY (`question_id`) REFERENCES `questions_question` (`id`),
  CONSTRAINT `evaluations_answer_chk_1` CHECK ((`score` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluations_answer`
--

LOCK TABLES `evaluations_answer` WRITE;
/*!40000 ALTER TABLE `evaluations_answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluations_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluations_evaluation`
--

DROP TABLE IF EXISTS `evaluations_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluations_evaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evaluations_evaluation_student_id_teacher_id_co_ddce4e6a_uniq` (`student_id`,`teacher_id`,`course_id`),
  KEY `evaluations_evaluation_course_id_36fdff26_fk_courses_course_id` (`course_id`),
  KEY `evaluations_evaluation_teacher_id_8234ac54_fk_accounts_user_id` (`teacher_id`),
  CONSTRAINT `evaluations_evaluation_course_id_36fdff26_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `evaluations_evaluation_student_id_0029cb85_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `evaluations_evaluation_teacher_id_8234ac54_fk_accounts_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluations_evaluation`
--

LOCK TABLES `evaluations_evaluation` WRITE;
/*!40000 ALTER TABLE `evaluations_evaluation` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluations_evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluations_evaluationpdf`
--

DROP TABLE IF EXISTS `evaluations_evaluationpdf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluations_evaluationpdf` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `generated_at` datetime(6) NOT NULL,
  `evaluation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evaluation_id` (`evaluation_id`),
  CONSTRAINT `evaluations_evaluati_evaluation_id_a06a3f31_fk_evaluatio` FOREIGN KEY (`evaluation_id`) REFERENCES `evaluations_evaluation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluations_evaluationpdf`
--

LOCK TABLES `evaluations_evaluationpdf` WRITE;
/*!40000 ALTER TABLE `evaluations_evaluationpdf` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluations_evaluationpdf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions_question`
--

DROP TABLE IF EXISTS `questions_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions_question`
--

LOCK TABLES `questions_question` WRITE;
/*!40000 ALTER TABLE `questions_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `questions_question` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-05 22:27:27
