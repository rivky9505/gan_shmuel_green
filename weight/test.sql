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
 
show tables;
 
describe containers_registered;
describe transactions;
describe unknown;
 
 
 
INSERT INTO unknown (container_id , weight ,unit) VALUES ('1c' , '400' , 'NULL');
INSERT INTO unknown (container_id , weight ,unit) VALUES ('1d' , '800' , 'NULL');

 
