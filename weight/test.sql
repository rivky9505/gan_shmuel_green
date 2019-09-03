--
-- Database: `Weight`
--
 
CREATE DATABASE IF NOT EXISTS `weight`;
 
 
-- --------------------------------------------------------
 
--
-- Table structure for table `containers-registered`
--
 
 
USE weight;
 
CREATE TABLE IF NOT EXISTS `unknown` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;
 
 
CREATE TABLE IF NOT EXISTS `containers_registered` (
  `id` varchar(15) NOT NULL,
  `kg` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
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
 

INSERT INTO transactions(`id`, `datetime`, `direction`) VALUES ('10', '2011-12-18 13:17:17', 'in');

show tables;
 
describe containers_registered;
describe transactions;
describe unknown;
 
 
-- Table structure for table 'weight'
 
CREATE TABLE IF NOT EXISTS `weight` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `direction` varchar(10) DEFAULT NULL,
  `truckid` varchar(50) DEFAULT NULL,
  `containers` varchar(1000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `forc` BOOLEAN NOT NULL DEFAULT 0,
  `produce` varchar(50) DEFAULT NULL, PRIMARY KEY(`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001 ;





INSERT INTO weight (`direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('in', 'truckID', 'str10', '10', 'unit', '0', 'tomatoes');

----Table structure for sessions

CREATE TABLE IF NOT EXISTS 'sessions' (
  `id` int(12) NOT NULL AUTO_INCREMENT, 
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  `truckid` varchar(50) DEFAULT NULL, 
  `bruto` int(12) DEFAULT NULL, 
  `truckTara` int(12) DEFAULT NULL, 
  `neto` int(12) DEFAULT NULL, 
PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001
