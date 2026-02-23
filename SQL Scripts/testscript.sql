DECLARE @unionAllTables NVARCHAR(MAX);
DECLARE @mainQuery NVARCHAR(MAX);

SELECT @unionAllTables = STRING_AGG(
    'SELECT organisation.organisationTitle FROM ' + QUOTENAME(name),
    ' UNION ALL '
)
FROM sys.tables;

SET @mainQuery = '
SELECT organisation.organisationTitle, COUNT(*) as occurences
FROM (' + @unionAllTables + ') AS Combined
GROUP BY organisation.organisationTitle
ORDER BY occurences DESC
';

EXEC sp_executesql @mainQuery;
