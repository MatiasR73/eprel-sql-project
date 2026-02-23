DECLARE @unionAllTables NVARCHAR(MAX);
DECLARE @mainQuery NVARCHAR(MAX);

SELECT @unionAllTables = STRING_AGG(
    'SELECT CAST([organisation.organisationName] AS NVARCHAR(500)) AS organisationName FROM ' + QUOTENAME(name),
    ' UNION ALL '
)
FROM sys.tables;

SET @mainQuery = '
SELECT organisationName, COUNT(*) as occurences
FROM (' + @unionAllTables + ') AS Combined
GROUP BY organisationName
ORDER BY occurences DESC
';

EXEC sp_executesql @mainQuery;
