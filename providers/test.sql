--
-- Database: `Weight`
--
 
CREATE DATABASE IF NOT EXISTS `weight`;
 
-- --------------------------------------------------------
 
--
-- Table structure for table `containers-registered`
--
 
USE weight;
 
 
CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;
 
-- --------------------------------------------------------
 
--
-- Table structure for table `transactions`
--
 
CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;
 
show tables;
 
describe containers_registered;
describe transactions;
 
 
 --
-- Database: `billdb`
--
 
CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;
 
-- --------------------------------------------------------
 
--
-- Table structure
--
 
CREATE TABLE IF NOT EXISTS `Provider` (
  `id` int(11)   NOT NULL AUTO_INCREMENT,
  `name` varchar(255)   DEFAULT NULL ,
   PRIMARY KEY (`id`)
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;
 

CREATE TABLE IF NOT EXISTS `Rates` (
  `product_id` varchar(50) NOT NULL,
  `rate` int(11) DEFAULT 0,
  `scope` varchar(50) DEFAULT NULL,
  FOREIGN KEY (scope) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;
 
CREATE TABLE IF NOT EXISTS `Trucks` (
  `id` varchar(10) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;
--
-- Dumping data
--
 
INSERT INTO Provider (`name`) VALUES ('ALL'), ('provider 1'), ('provider 2'), ('provider 3'), ('provider 4');
 
INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES ('Navel', '93', 'All'), ('Blood', '112', 'All'), ('Mandarin', '104', 'All'), 
('Shamuti', '84', 'All'), ('Tangerine', '92', 'All'), ('Clementine', '113', 'All'), 
('Grapefruit', '88', 'All'), ('Valencia', '87', 'All'), ('Mandarin', '102', '43'), 
('Mandarin', '120', '45'), ('Tangerine', '85', '12'), ('Valencia', '90', '45');
 
INSERT INTO Trucks (`id`, `provider_id`) VALUES ('134-33-443', 10001), ('124-55-443', 10003),
('222-33-111', 10003), ('212-33-441', 10004),('432-98-541', 10001), ('212-99-466', 10002);

--
-- Dumping data for table `test`
--
 
-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
