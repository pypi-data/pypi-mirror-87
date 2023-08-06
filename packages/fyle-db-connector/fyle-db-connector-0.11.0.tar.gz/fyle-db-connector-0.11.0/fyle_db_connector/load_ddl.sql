DROP TABLE IF EXISTS fyle_load_tpa_export_batches;
DROP TABLE IF EXISTS fyle_load_tpa_export_batch_lineitems;

CREATE TABLE fyle_load_tpa_export_batches (
    id INTEGER,
    name TEXT,
    success BOOLEAN,
    description TEXT,
    exported_at DATETIME,
    url Text
);

CREATE TABLE fyle_load_tpa_export_batch_lineitems (
    batch_id INTEGER,
    object_id TEXT,
    object_type TEXT,
    reference TEXT
);