BEGIN;
CREATE TABLE `qofdb_organisation` (
    `orgcode` varchar(8) NOT NULL PRIMARY KEY
)
;
CREATE TABLE `qofdb_address` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `orgcode_id` varchar(8) NOT NULL,
    `year` smallint UNSIGNED NOT NULL,
    `name` varchar(30) NOT NULL,
    `building` varchar(30) NOT NULL,
    `street` varchar(30) NOT NULL,
    `locality` varchar(30) NOT NULL,
    `region` varchar(30) NOT NULL,
    `postcode` varchar(10) NOT NULL,
    `website` varchar(200) NOT NULL
)
;
ALTER TABLE `qofdb_address` ADD CONSTRAINT `orgcode_id_refs_orgcode_4a441a8e` FOREIGN KEY (`orgcode_id`) REFERENCES `qofdb_organisation` (`orgcode`);
CREATE TABLE `qofdb_indicator` (
    `flavour` smallint UNSIGNED NOT NULL,
    `areaid` varchar(15) NOT NULL PRIMARY KEY,
    `short_description` varchar(100) NOT NULL,
    `long_description` varchar(1024) NOT NULL,
    `area` varchar(15) NOT NULL,
    `sort_order` smallint UNSIGNED NOT NULL,
    `prevtext` varchar(20) NOT NULL
)
;
CREATE TABLE `qofdb_achievement` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `year` smallint UNSIGNED NOT NULL,
    `numerator` integer NOT NULL,
    `denominator` integer NOT NULL,
    `ratio` double precision NOT NULL,
    `centile` double precision NOT NULL,
    `orgcode_id` varchar(8) NOT NULL,
    `areaid_id` varchar(15) NOT NULL
)
;
ALTER TABLE `qofdb_achievement` ADD CONSTRAINT `areaid_id_refs_areaid_6810db97` FOREIGN KEY (`areaid_id`) REFERENCES `qofdb_indicator` (`areaid`);
ALTER TABLE `qofdb_achievement` ADD CONSTRAINT `orgcode_id_refs_orgcode_299923e7` FOREIGN KEY (`orgcode_id`) REFERENCES `qofdb_organisation` (`orgcode`);
CREATE TABLE `qofdb_threshold` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `lower` integer NOT NULL,
    `upper` integer NOT NULL,
    `points` numeric(4, 1) NOT NULL,
    `year` smallint UNSIGNED NOT NULL,
    `areaid_id` varchar(15) NOT NULL
)
;
ALTER TABLE `qofdb_threshold` ADD CONSTRAINT `areaid_id_refs_areaid_275da1d` FOREIGN KEY (`areaid_id`) REFERENCES `qofdb_indicator` (`areaid`);
CREATE TABLE `qofdb_orgheirarchy` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `year` smallint UNSIGNED NOT NULL,
    `orgcode_id` varchar(8) NOT NULL,
    `parent_id` varchar(8) NOT NULL
)
;
ALTER TABLE `qofdb_orgheirarchy` ADD CONSTRAINT `orgcode_id_refs_orgcode_1168008c` FOREIGN KEY (`orgcode_id`) REFERENCES `qofdb_organisation` (`orgcode`);
ALTER TABLE `qofdb_orgheirarchy` ADD CONSTRAINT `parent_id_refs_orgcode_1168008c` FOREIGN KEY (`parent_id`) REFERENCES `qofdb_organisation` (`orgcode`);
CREATE TABLE `qofdb_distance` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `org1_id` varchar(8) NOT NULL,
    `org2_id` varchar(8) NOT NULL,
    `dist` double precision NOT NULL
)
;
ALTER TABLE `qofdb_distance` ADD CONSTRAINT `org1_id_refs_orgcode_4bd8ec9a` FOREIGN KEY (`org1_id`) REFERENCES `qofdb_organisation` (`orgcode`);
ALTER TABLE `qofdb_distance` ADD CONSTRAINT `org2_id_refs_orgcode_4bd8ec9a` FOREIGN KEY (`org2_id`) REFERENCES `qofdb_organisation` (`orgcode`);
COMMIT;
