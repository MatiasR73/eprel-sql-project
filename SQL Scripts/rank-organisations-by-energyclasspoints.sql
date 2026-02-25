 SELECT productsTable.[organisation.organisationName], COUNT(*) as occurences, AVG(energyTable.Id) as energypointsavg
 FROM [dbo].[electronicdisplays] as productsTable
 JOIN [dbo].[EnergyClasses] as energyTable
    ON productsTable.energyClass = energyTable.energyClass
WHERE productsTable.energyClass IS NOT NULL
GROUP BY productsTable.[organisation.organisationName]
HAVING COUNT(*) > 50
ORDER BY energypointsavg desc, occurences desc
 
 