-- Known state-event categories, seeded as reference data.
--
-- These are deliberately NOT a CHECK constraint: the module spec requires
-- the category list to stay extensible, so unknown codes are accepted and
-- this table exists for validation hints and UI grouping only.

INSERT INTO state_event_category (code, applies_to, description) VALUES
    ('COSTUME_CHANGE',          'CHARACTER', 'Zmiana kostiumu'),
    ('WETNESS',                 'CHARACTER', 'Zmoczenie'),
    ('BLOOD',                   'CHARACTER', 'Krew'),
    ('INJURY',                  'CHARACTER', 'Rana lub uraz'),
    ('DIRT',                    'CHARACTER', 'Zabrudzenie'),
    ('HAIR_CHANGE',             'CHARACTER', 'Zmiana fryzury'),
    ('MAKEUP_CHANGE',           'CHARACTER', 'Zmiana charakteryzacji'),
    ('AGING',                   'CHARACTER', 'Zmiana wieku'),
    ('PHYSICAL_TRANSFORMATION', 'CHARACTER', 'Przemiana fizyczna'),
    ('DISGUISE',                'CHARACTER', 'Przebranie'),
    ('UNIFORM_CHANGE',          'CHARACTER', 'Zmiana munduru'),
    ('CARRIED_OBJECT_CHANGE',   'CHARACTER', 'Zmiana niesionego przedmiotu'),
    ('MISSING_OBJECT',          'CHARACTER', 'Utrata przedmiotu'),

    ('TIME_OF_DAY',        'LOCATION', 'Pora dnia'),
    ('WEATHER',            'LOCATION', 'Pogoda'),
    ('SEASON',             'LOCATION', 'Pora roku'),
    ('DAMAGE',             'LOCATION', 'Uszkodzenie'),
    ('DESTRUCTION',        'LOCATION', 'Zniszczenie'),
    ('FIRE',               'LOCATION', 'Pożar'),
    ('FLOOD',              'LOCATION', 'Zalanie'),
    ('OCCUPATION',         'LOCATION', 'Zajęcie przestrzeni'),
    ('FURNITURE_CHANGE',   'LOCATION', 'Zmiana umeblowania'),
    ('DECORATION_CHANGE',  'LOCATION', 'Zmiana wystroju'),
    ('CONSTRUCTION_STATE', 'LOCATION', 'Stan budowy'),
    ('LIGHTING_STATE',     'LOCATION', 'Stan oświetlenia'),

    ('INTACT',            'PROP', 'Nienaruszony'),
    ('DAMAGED',           'PROP', 'Uszkodzony'),
    ('OPEN',              'PROP', 'Otwarty'),
    ('CLOSED',            'PROP', 'Zamknięty'),
    ('FULL',              'PROP', 'Pełny'),
    ('EMPTY',             'PROP', 'Pusty'),
    ('CLEAN',             'PROP', 'Czysty'),
    ('DIRTY',             'PROP', 'Brudny'),
    ('BLOODIED',          'PROP', 'Zakrwawiony'),
    ('BURNED',            'PROP', 'Spalony'),
    ('BROKEN',            'PROP', 'Złamany'),
    ('MISSING_COMPONENT', 'PROP', 'Brakujący element'),
    ('LOCATION_CHANGE',   'PROP', 'Zmiana miejsca'),
    ('OWNERSHIP_CHANGE',  'PROP', 'Zmiana właściciela'),

    ('OTHER', 'ANY', 'Inne');
