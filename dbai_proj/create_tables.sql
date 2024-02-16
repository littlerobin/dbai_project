CREATE TABLE Plant (
    PlantID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(200),
    Species VARCHAR(200),
    PlantedDate DATE,
    WaterFrequency VARCHAR(100)
);

CREATE TABLE Location (
    LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlantID INTEGER,
    GardenSection VARCHAR(50),
    Row INTEGER,
    Column INTEGER,
    FOREIGN KEY (PlantID) REFERENCES Plant(PlantID)
); 

CREATE TABLE Gardener (
    GardenerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(200),
    Specialization VARCHAR(300)
);

CREATE TABLE PlantGardener (
    PlantGardenerID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlantID INTEGER,
    GardenerID INTEGER,
    LastWateredDate TEXT,
    FOREIGN KEY (PlantID) REFERENCES Plant(PlantID),
    FOREIGN KEY (GardenerID) REFERENCES Gardener(GardenerID)
);
