BEGIN TRANSACTION;
DROP TABLE IF EXISTS `yeast`;
CREATE TABLE IF NOT EXISTS `yeast` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS `styles`;
CREATE TABLE IF NOT EXISTS `styles` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS `recipes`;
CREATE TABLE IF NOT EXISTS `recipes` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`styleID`	INTEGER NOT NULL,
	`og`	REAL,
	`fg`	REAL,
	`ibu`	INTEGER,
	`srm`	INTEGER
);
DROP TABLE IF EXISTS `recipe_yeast`;
CREATE TABLE IF NOT EXISTS `recipe_yeast` (
	`recipeID`	INTEGER NOT NULL,
	`yeastID`	INTEGER NOT NULL,
	FOREIGN KEY(`recipeID`) REFERENCES `recipes`(`id`),
	FOREIGN KEY(`yeastID`) REFERENCES `yeast`(`id`)
);
DROP TABLE IF EXISTS `recipe_hops`;
CREATE TABLE IF NOT EXISTS `recipe_hops` (
	`recipeID`	INTEGER NOT NULL,
	`hopID`	INTEGER NOT NULL,
	`ounces`	REAL NOT NULL,
	`minutes`	INTEGER NOT NULL,
	FOREIGN KEY(`recipeID`) REFERENCES `recipes`(`id`),
	FOREIGN KEY(`hopID`) REFERENCES `hops`(`id`)
);
DROP TABLE IF EXISTS `recipe_fermentables`;
CREATE TABLE IF NOT EXISTS `recipe_fermentables` (
	`recipeID`	INTEGER NOT NULL,
	`fermentableID`	INTEGER NOT NULL,
	`pounds`	REAL NOT NULL,
	FOREIGN KEY(`fermentableID`) REFERENCES `fermentables`(`id`),
	FOREIGN KEY(`recipeID`) REFERENCES `recipes`(`id`)
);
DROP TABLE IF EXISTS `hops`;
CREATE TABLE IF NOT EXISTS `hops` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`alphaAcidPercentage`	INTEGER
);
DROP TABLE IF EXISTS `fermentables`;
CREATE TABLE IF NOT EXISTS `fermentables` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE
);
DROP INDEX IF EXISTS `unique_hop_alpha`;
CREATE UNIQUE INDEX IF NOT EXISTS `unique_hop_alpha` ON `hops` (
	`name`,
	`alphaAcidPercentage`
);
DROP INDEX IF EXISTS `recipe_yeast_index`;
CREATE UNIQUE INDEX IF NOT EXISTS `recipe_yeast_index` ON `recipe_yeast` (
	`recipeID`,
	`yeastID`
);
DROP INDEX IF EXISTS `recipe_hop_index`;
CREATE INDEX IF NOT EXISTS `recipe_hop_index` ON `recipe_hops` (
	`recipeID`,
	`hopID`
);
DROP INDEX IF EXISTS `recipe_fermentable_index`;
CREATE UNIQUE INDEX IF NOT EXISTS `recipe_fermentable_index` ON `recipe_fermentables` (
	`recipeID`,
	`fermentableID`
);
COMMIT;
