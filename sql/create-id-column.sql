DECLARE @createEmptyIDColumn NVARCHAR(MAX) = '';

SELECT @createEmptyIDColumn += '
ALTER TABLE ' + QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + ' ADD Id INT;
'
FROM sys.columns c
JOIN sys.tables t ON c.object_id = t.object_id
WHERE c.name = 'eprelRegistrationNumber';

EXEC sp_executesql @createEmptyIDColumn;

GO

DECLARE @copyRegistrationNumberToIDColumn NVARCHAR(MAX) = '';

SELECT @copyRegistrationNumberToIDColumn += '
UPDATE ' + QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + '
SET Id = ' + QUOTENAME('eprelRegistrationNumber') + ';
'
FROM sys.columns c
JOIN sys.tables t ON c.object_id = t.object_id
WHERE c.name = 'eprelRegistrationNumber';

EXEC sp_executesql @copyRegistrationNumberToIDColumn;