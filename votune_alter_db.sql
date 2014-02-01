ALTER TABLE `votune`.`votune_song` 
CHANGE COLUMN `checksum` `hash` VARCHAR(32) NOT NULL ,
ADD COLUMN `source` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 0 AFTER `account_id`;

ALTER TABLE `votune`.`votune_account` 
ADD COLUMN `spotify_username` VARCHAR(50) NOT NULL AFTER `phone`,
ADD COLUMN `spotify_password` VARCHAR(50) NOT NULL AFTER `spotify_username`;

