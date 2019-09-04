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
  `weight` varchar(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('c-11111', 'na', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('c-22222', 'na', 'kg');
 
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
  `produce` varchar(50) DEFAULT NULL, PRIMARY KEY(`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001;




INSERT INTO weight (`direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('in', 'T-55555', 'containers', '10', 'kg', '0', 'tomatoes');
INSERT INTO weight (`direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('in', 'TRUCKID', 'containers', '10', 'kg', '0', 'tomatoes');





CREATE TABLE IF NOT EXISTS `sessions` (
  `id` int(12) NOT NULL AUTO_INCREMENT, 
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  `truckid` varchar(50) DEFAULT NULL, 
  `bruto` int(12) DEFAULT NULL, 
  `truckTara` int(12) DEFAULT NULL, 
  `neto` int(12) DEFAULT NULL, 
PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001;

INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000101000000', 'C-11111', '10');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000201000000', 'C-11112', '20');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000108000000', 'C-11111', '12');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000225000000', 'C-11112', '150');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000301000000', 'C-11111', '40');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000101000000', 't-55555', '8');

show tables;
 
describe containers_registered;
describe transactions;
describe sessions;
describe weight;


