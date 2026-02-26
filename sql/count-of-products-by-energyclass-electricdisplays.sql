SELECT energyClass, COUNT(*) AS numProducts
FROM [dbo].[electronicdisplays]
WHERE energyClass IS NOT NULL
GROUP BY energyClass
ORDER BY energyClass;