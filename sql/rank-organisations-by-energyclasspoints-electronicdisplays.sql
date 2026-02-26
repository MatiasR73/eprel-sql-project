 SELECT productsTable.[organisation.organisationName], COUNT(*) as occurences, CAST(AVG(1.0 * energyTable.Id) as DECIMAL(5,2)) AS energypointsAVGoutof7
 FROM [dbo].[electronicdisplays] as productsTable
 JOIN [dbo].[EnergyClasses] as energyTable
    ON productsTable.energyClass = energyTable.energyClass
WHERE productsTable.energyClass IS NOT NULL
GROUP BY productsTable.[organisation.organisationName]
HAVING COUNT(*) >= 50
ORDER BY energypointsAVGoutof7 desc, occurences desc
 
 