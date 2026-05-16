-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 16, 2026 at 09:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `train_chatbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `additional_charges`
--

DROP TABLE IF EXISTS `additional_charges`;
CREATE TABLE `additional_charges` (
  `charge_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `charge_type` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `additional_charges`
--

INSERT INTO `additional_charges` (`charge_id`, `charge_type`, `description`, `amount`) VALUES
(1, 'luggage', 'Large luggage above free limit', 200.00),
(2, 'booking_fee', 'Online reservation service fee', 50.00),
(3, 'tax', 'Government tax percentage may apply', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `fares`
--

DROP TABLE IF EXISTS `fares`;
CREATE TABLE `fares` (
  `fare_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `from_station_id` int(11) NOT NULL,
  `to_station_id` int(11) NOT NULL,
  `first_class_price` decimal(8,2) DEFAULT NULL,
  `second_class_price` decimal(8,2) DEFAULT NULL,
  `third_class_price` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `fares`
--

INSERT INTO `fares` (`fare_id`, `from_station_id`, `to_station_id`, `first_class_price`, `second_class_price`, `third_class_price`) VALUES
(1, 1, 10, 2000.00, 1200.00, 900.00),
(2, 1, 12, 3000.00, 2000.00, 1500.00),
(3, 1, 13, 3000.00, 2000.00, 1500.00),
(4, 1, 14, 3000.00, 2000.00, 1500.00),
(5, 1, 7, 1100.00, 500.00, 240.00),
(6, 1, 8, 1400.00, 600.00, 300.00),
(7, 1, 18, 2800.00, 1900.00, 1200.00),
(8, 1, 21, 3000.00, 2000.00, 1400.00),
(9, 1, 22, 2900.00, 1800.00, 1300.00),
(10, 1, 24, 1050.00, 550.00, 260.00),
(11, 1, 23, 600.00, 300.00, 160.00),
(12, 1, 2, 100.00, 50.00, 20.00),
(13, 1, 3, 200.00, 100.00, 40.00),
(14, 1, 4, 300.00, 150.00, 80.00),
(15, 1, 5, 400.00, 200.00, 100.00),
(16, 1, 6, 650.00, 350.00, 180.00),
(17, 1, 7, 950.00, 500.00, 240.00),
(18, 1, 8, 1450.00, 750.00, 360.00),
(19, 1, 9, 1600.00, 800.00, 400.00),
(20, 1, 10, 1750.00, 900.00, 440.00),
(21, 1, 11, 1800.00, 900.00, 460.00),
(22, 16, 18, 650.00, 500.00, 200.00);

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes` (
  `route_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `route_name` varchar(100) NOT NULL UNIQUE,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`route_id`, `route_name`, `description`) VALUES
(1, 'Colombo-Kandy-Badulla', 'Hill country railway line'),
(2, 'Colombo-Galle-Matara', 'Southern coastal railway'),
(3, 'Colombo-Jaffna', 'Northern railway route'),
(4, 'Colombo-Batticaloa', 'Eastern railway route'),
(5, 'Colombo-Trincomalee', 'Eastern coastal route'),
(6, 'Colombo-Puttalam', 'Puttalam coastal railway line');

-- --------------------------------------------------------

--
-- Table structure for table `seat_classes`
--

DROP TABLE IF EXISTS `seat_classes`;
CREATE TABLE `seat_classes` (
  `class_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `class_name` varchar(50) DEFAULT NULL UNIQUE,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `seat_classes`
--

INSERT INTO `seat_classes` (`class_id`, `class_name`, `description`) VALUES
(1, 'First Class', 'Air Conditioned Premium'),
(2, 'Second Class', 'Reserved / Standard'),
(3, 'Third Class', 'Economy');

-- --------------------------------------------------------

--
-- Table structure for table `stations`
--

DROP TABLE IF EXISTS `stations`;
CREATE TABLE `stations` (
  `station_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `station_name` varchar(100) NOT NULL UNIQUE,
  `distance_from_colombo` decimal(8,2) DEFAULT NULL,
  `Telephone_no` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `stations`
--

INSERT INTO `stations` (`station_id`, `station_name`, `distance_from_colombo`, `Telephone_no`) VALUES
(1, 'Colombo Fort', 0.00, '0113 070 447'),
(2, 'Maradana', 2.00, '011-2965230'),
(3, 'Mount Lavinia', 14.00, '0112 712 271'),
(4, 'Panadura', 27.00, '038-2232222'),
(5, 'Kalutara South', 44.00, '0342 222 271'),
(6, 'Bentota', 63.00, '0342 275 271'),
(7, 'Galle', 116.00, '0912 232 271'),
(8, 'Matara', 160.00, '+94 412 222 271'),
(9, 'Peradeniya Junction', 114.00, '081-2388271'),
(10, 'Kandy', 121.00, '0812 222 271'),
(11, 'Hatton', 173.00, '075 511 9185'),
(12, 'Nanu Oya', 207.00, '0522 222 873'),
(13, 'Ella', 271.00, '0572 228 571'),
(14, 'Badulla', 292.00, ''),
(15, 'Anuradhapura', 205.00, ''),
(16, 'Vavuniya', 255.00, ''),
(17, 'Kilinochchi', 332.00, ''),
(18, 'Jaffna', 398.00, ''),
(19, 'Habarana', 210.00, ''),
(20, 'Polonnaruwa', 260.00, ''),
(21, 'Batticaloa', 350.00, ''),
(22, 'Trincomalee', 296.00, ''),
(23, 'Chilaw', 82.00, ''),
(24, 'Puttalam', 135.12, ''),
(25, 'Negombo', 38.00, ''),
(26, 'Noor Nagar', 139.10, ''),
(27, 'Palavi', 113.39, ''),
(63, 'Ragama', 15.55, ''),
(64, 'Gampaha', 27.54, ''),
(65, 'Veyangoda', 37.48, ''),
(66, 'Polgahawela', 73.83, ''),
(67, 'Nanuoya', 207.06, ''),
(68, 'Haputale', 247.97, '');

-- --------------------------------------------------------

--
-- Table structure for table `terms_conditions`
--

DROP TABLE IF EXISTS `terms_conditions`;
CREATE TABLE `terms_conditions` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  `section_no` varchar(20) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `terms_conditions`
--

INSERT INTO `terms_conditions` (`id`, `category`, `section_no`, `title`, `description`) VALUES
(1, 'General Reservation', '01', 'Maximum Reservation', 'Maximum of 5 seats can be reserved at once.'),
(2, 'General Reservation', '02', 'NIC Requirement', 'NIC numbers are required for all adult passengers.'),
(3, 'General Reservation', '03', 'Payment Methods', 'Accepted payment methods are VISA, MasterCard and American Express.'),
(4, 'General Reservation', '04', 'Cancellation Refund', '75% refund before 7 days and 50% refund before 48 hours.'),
(5, 'General Reservation', '05', 'Child Policy', 'Children below 3 years travel free when sharing seats.'),
(6, 'General Reservation', '06', 'Dangerous Goods', 'Firearms and dangerous materials are prohibited onboard.'),
(7, 'General Reservation', '07', 'Pets', 'Pets are not allowed onboard trains.'),
(8, 'General Reservation', '08', 'Luggage', 'Free luggage allowance depends on travel class.'),
(9, 'General Reservation', '09', 'Ticket Usage', 'Tickets are valid only for specified train and date.'),
(10, 'General Reservation', '10', 'Governing Law', 'Services are governed under Sri Lankan law.');

-- --------------------------------------------------------

--
-- Table structure for table `trains`
--

DROP TABLE IF EXISTS `trains`;
CREATE TABLE `trains` (
  `train_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `train_name` varchar(100) NOT NULL,
  `route_id` int(11) NOT NULL,
  `train_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `trains`
--

INSERT INTO `trains` (`train_id`, `train_name`, `route_id`, `train_type`) VALUES
(1001, 'Dunhinda Odyssey', 1, 'Blue Train'),
(1005, 'Podi Menike', 1, 'Express'),
(1015, 'Udarata Menike', 1, 'Express'),
(1045, 'Night Mail', 1, 'Sleeper'),
(3402, 'Puttalam-Maradana Morning', 6, 'Commuter'),
(3408, 'Puttalam-Maradana Evening', 6, 'Commuter'),
(3411, 'Puttalam Early Bird', 6, 'Express'),
(3425, 'Puttalam Weekday Express', 6, 'Express'),
(4077, 'Yal Devi', 3, 'Long Distance'),
(5001, 'Batticaloa Express', 4, 'Long Distance'),
(7083, 'Trincomalee Night Mail', 5, 'Night Train'),
(8056, 'Southern Express', 2, 'Intercity');

-- --------------------------------------------------------

--
-- Table structure for table `train_schedules`
--

DROP TABLE IF EXISTS `train_schedules`;
CREATE TABLE `train_schedules` (
  `schedule_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `train_id` int(11) NOT NULL,
  `station_id` int(11) NOT NULL,
  `arrival_time` time DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `running_days` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `train_schedules`
--

INSERT INTO `train_schedules` (`schedule_id`, `train_id`, `station_id`, `arrival_time`, `departure_time`, `running_days`) VALUES
(1, 1001, 1, NULL, '05:30:00', 'Daily'),
(2, 1001, 10, '08:11:00', '08:25:00', 'Daily'),
(3, 1001, 11, '10:40:00', '10:45:00', 'Daily'),
(4, 1001, 12, '12:06:00', '12:10:00', 'Daily'),
(5, 1001, 13, '14:41:00', '14:45:00', 'Daily'),
(6, 1001, 14, '15:43:00', NULL, 'Daily'),
(7, 1005, 1, NULL, '05:55:00', 'Tue,Fri,Sun'),
(8, 1005, 10, '08:48:00', '08:55:00', 'Tue,Fri,Sun'),
(9, 1005, 11, '11:19:00', '11:25:00', 'Tue,Fri,Sun'),
(10, 1005, 12, '12:50:00', '12:55:00', 'Tue,Fri,Sun'),
(11, 1005, 13, '16:18:00', '16:20:00', 'Tue,Fri,Sun'),
(12, 1005, 14, '17:30:00', NULL, 'Tue,Fri,Sun'),
(13, 1015, 1, NULL, '08:30:00', 'Daily'),
(14, 1015, 10, '11:15:00', '11:20:00', 'Daily'),
(15, 1015, 14, '18:00:00', NULL, 'Daily'),
(16, 8056, 1, NULL, '14:40:00', 'Mon-Fri'),
(17, 8056, 7, '16:57:00', '17:05:00', 'Mon-Fri'),
(18, 8056, 8, '18:15:00', NULL, 'Mon-Fri'),
(19, 4077, 1, NULL, '20:00:00', 'Daily'),
(20, 4077, 15, '00:30:00', '00:40:00', 'Daily'),
(21, 4077, 16, '03:10:00', '03:15:00', 'Daily'),
(22, 4077, 17, '05:30:00', '05:35:00', 'Daily'),
(23, 4077, 18, '06:30:00', NULL, 'Daily'),
(24, 5001, 1, NULL, '19:00:00', 'Daily'),
(25, 5001, 19, '01:00:00', '01:05:00', 'Daily'),
(26, 5001, 20, '03:45:00', '03:50:00', 'Daily'),
(27, 5001, 21, '06:00:00', NULL, 'Daily'),
(28, 7083, 1, NULL, '21:00:00', 'Daily'),
(29, 7083, 19, '02:00:00', '02:10:00', 'Daily'),
(30, 7083, 22, '06:30:00', NULL, 'Daily'),
(55, 3411, 1, NULL, '07:40:00', 'Daily'),
(56, 3411, 24, '12:38:00', NULL, 'Daily'),
(57, 3425, 1, NULL, '17:18:00', 'Mon-Fri'),
(58, 3425, 24, '21:05:00', NULL, 'Mon-Fri'),
(59, 3402, 24, NULL, '09:56:00', 'Daily'),
(60, 3402, 2, '14:20:00', NULL, 'Daily'),
(61, 3408, 24, NULL, '16:45:00', 'Daily'),
(62, 3408, 2, '21:17:00', NULL, 'Daily'),
(63, 7083, 1, NULL, '20:30:00', 'Daily'),
(64, 7083, 10, '01:30:00', '01:45:00', 'Daily'),
(65, 7083, 15, '04:15:00', '04:30:00', 'Daily'),
(66, 7083, 22, '07:15:00', NULL, 'Daily'),
(67, 1015, 1, NULL, '08:30:00', 'Daily'),
(68, 1015, 10, '11:15:00', '11:20:00', 'Daily'),
(69, 1015, 22, '17:45:00', NULL, 'Daily');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fares`
--
ALTER TABLE `fares`
  ADD CONSTRAINT `fares_ibfk_1` FOREIGN KEY (`from_station_id`) REFERENCES `stations` (`station_id`),
  ADD CONSTRAINT `fares_ibfk_2` FOREIGN KEY (`to_station_id`) REFERENCES `stations` (`station_id`);

--
-- Constraints for table `trains`
--
ALTER TABLE `trains`
  ADD CONSTRAINT `trains_ibfk_1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`);

--
-- Constraints for table `train_schedules`
--
ALTER TABLE `train_schedules`
  ADD CONSTRAINT `train_schedules_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`),
  ADD CONSTRAINT `train_schedules_ibfk_2` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`);
--
-- Table structure for table `unknown_questions`
--

DROP TABLE IF EXISTS `unknown_questions`;
CREATE TABLE `unknown_questions` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `question` text NOT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;


