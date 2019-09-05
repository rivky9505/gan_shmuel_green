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
 
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('Q-5722', '307', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('R-7537', '316', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('R-7477', '242', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('L-7747', '226', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('V-7363', '242', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('W-7426', '246', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('S-8553', '243', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('J-2633', '186', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('H-0597', '185', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('G-7490', '185', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('T-4697', '185', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('W-8697', '185', 'kg');
INSERT INTO containers_registered (`container_id`, `weight`, `unit`) VALUES ('R-8597', '255', 'kg');
 
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
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `forc` BOOLEAN NOT NULL DEFAULT 0,
  `produce` varchar(50) DEFAULT NULL, PRIMARY KEY(`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001;




INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','in', 'TRUCKID', 'G-9234', '243', 'kg', '0', 'clementine');
INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','in', 'T-55555', 'T-4256,Y-9270,J-8394,H-1234', '687', 'kg', '0', 'tomatoes');
INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','in', 'T-55432', 'T-4646,Y-9830,J-8434,H-1234', '687', 'kg', '0', 'tomatoes');
INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','in', 'T-55755', 'T-4247,Y-9246,J-8274,H-4334', '724', 'kg', '0', 'tomatoes');
INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','in', 'T-55934', 'T-4246,Y-7573,J-8394,H-3334', '599', 'kg', '0', 'tomatoes');
INSERT INTO weight (`created_at`, `direction`, `truckid`, `containers`, `bruto`, `unit`, `forc`, `produce`) VALUES ('20190905104120','out', 'T-55555', '', '100', 'kg', '0', 'tomatoes');





CREATE TABLE IF NOT EXISTS `sessions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `direction` varchar(10) DEFAULT NULL,
  `truckid` varchar(50) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  `neto` int(12) DEFAULT NULL,
PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001;

INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000101000000', 'N-15311', '24');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000201000000', 'V-86112', '52');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000108000000', 'I-53174', '17');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000225000000', 'Y-92012', '147');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000301000000', 'G-13611', '48');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20000101000000', 'T-03845', '81');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104120', 'N-15311', '24');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104230', 'V-86112', '52');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104320', 'I-53174', '17');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104420', 'Y-92012', '57');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104520', 'G-13611', '48');
INSERT INTO sessions (`created_at`, `truckid`, `truckTara`) VALUES ('20190905104620', 'T-03845', '81');

show tables;

describe containers_registered;
describe transactions;
describe sessions;
describe weight;


