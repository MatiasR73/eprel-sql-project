CREATE TABLE dbo.EnergyClasses
(
    Id INT PRIMARY KEY,
    EnergyClass CHAR(1) NOT NULL UNIQUE
);

INSERT INTO dbo.EnergyClasses (Id, EnergyClass)
VALUES
(1, 'G'),
(2, 'F'),
(3, 'E'),
(4, 'D'),
(5, 'C'),
(6, 'B'),
(7, 'A');