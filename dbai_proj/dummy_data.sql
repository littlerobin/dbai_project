INSERT INTO Plant (Name, Species, PlantedDate, WaterFrequency) VALUES 
('Rose', 'Rosa', '2023-05-15', 'Twice a week'),
('Lily', 'Lilium', '2023-06-20', 'Once a week'),
('Tulip', 'Tulipa', '2022-04-10', 'Every three days'),
('Tomato', 'Solanum lycopersicum', '2023-03-01', 'Every other day'),
('Carrot', 'Daucus carota', '2023-04-05', 'Twice a week'),
('Lettuce', 'Lactuca sativa', '2023-04-25', 'Once a day'),
('Butterfly Bush', 'Buddleja davidii', '2022-05-20', 'Once a week'),
('Milkweed', 'Asclepias', '2022-06-01', 'Every other day');

INSERT INTO Location (PlantID, GardenSection, Row, Column) VALUES 
(1, 'Rose Garden', 1, 3),
(2, 'Lily Patch', 2, 1),
(3, 'Tulip Bed', 3, 2),
(4, 'Vegetable Patch', 1, 2),
(5, 'Vegetable Patch', 2, 3),
(6, 'Vegetable Patch', 3, 1),
(7, 'Butterfly Garden', 1, 1),
(8, 'Butterfly Garden', 2, 2);

INSERT INTO Gardener (FirstName, LastName, Email, Specialization) VALUES 
('John', 'Smith', 'john@example.com', 'Landscaping'),
('Emily', 'Johnson', 'emily@example.com', 'Botany'),
('Michael', 'Brown', 'michael@example.com', 'Horticulture');

INSERT INTO PlantGardener (PlantID, GardenerID, LastWateredDate) VALUES 
(1, 1, '2024-01-10 08:00:00'),
(1, 2, '2024-01-10 10:00:00'),
(2, 2, '2024-01-12 09:30:00'),
(3, 3, '2024-01-15 11:45:00'),
(4, 1, '2024-01-10 08:00:00'),
(5, 2, '2024-01-12 09:30:00'),
(6, 3, '2024-01-15 11:45:00'),
(7, 1, '2024-01-10 08:00:00'),
(8, 2, '2024-01-12 09:30:00');