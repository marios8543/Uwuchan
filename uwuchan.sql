-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 12, 2018 at 04:34 PM
-- Server version: 10.1.32-MariaDB
-- PHP Version: 7.2.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uwuchan`
--

-- --------------------------------------------------------

--
-- Table structure for table `boards`
--

CREATE TABLE `boards` (
  `name` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `color` varchar(7) COLLATE utf8_bin NOT NULL DEFAULT '#DCDCDC',
  `pinned` int(10) DEFAULT NULL,
  `admins` varchar(255) COLLATE utf8_bin DEFAULT '[]'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `data` blob,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `og_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `type` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `size` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `author` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `board` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `thread` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '0',
  `subject` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `text` text COLLATE utf8_bin,
  `image` varchar(64) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `restrictions`
--

CREATE TABLE `restrictions` (
  `id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `board` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `duration` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `valid` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(64) COLLATE utf8_bin NOT NULL,
  `ip` varchar(80) COLLATE utf8_bin NOT NULL,
  `first_login` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `banned` tinyint(1) NOT NULL DEFAULT '0',
  `admin` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
