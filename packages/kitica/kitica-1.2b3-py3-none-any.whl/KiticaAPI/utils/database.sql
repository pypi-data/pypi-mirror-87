--
-- File generated with SQLiteStudio v3.2.1 on Wed Sep 23 16:46:57 2020
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: device
CREATE TABLE device (deviceId INTEGER PRIMARY KEY AUTOINCREMENT, deviceName VARCHAR NOT NULL, platformName VARCHAR DEFAULT Android, platformVersion VARCHAR, udid VARCHAR NOT NULL, server VARCHAR NOT NULL, port VARCHAR NOT NULL DEFAULT "4723/wd/hub", wdaPort INTEGER, status VARCHAR NOT NULL DEFAULT FREE, teamName VARCHAR NOT NULL DEFAULT "", version INT DEFAULT (1) NOT NULL, borrowerIp VARCHAR, borrowerHostname VARCHAR, lastBorrowed VARCHAR, deviceType VARCHAR DEFAULT Emulator NOT NULL, driverPath VARCHAR DEFAULT "/path/to/webdriver" NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
