from nomnomdata.engine.components import Parameter, ParameterGroup, SharedConfig
from nomnomdata.engine.parameters import Code, Enum, Nested, String

FirebaseToDatabase = SharedConfig(
    shared_config_type_uuid="FB2DB-NND3C",
    description="Firebase collection to a relational database table configuration parameters.",
    alias="Firebase to Relational Database",
    categories=[
        "Firebase",
        "Loader",
        "Relational Database",
    ],
    parameters=[
        ParameterGroup(
            Parameter(
                name="collection_name",
                display_name="Collection",
                description="Name of the collection in the Firebase app.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="tracking_field",
                display_name="Tracking Field",
                description="Name of the field in the Collection to use for sorting and tracking documents processed.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="tracking_field_type",
                display_name="Tracking Field Type",
                description="Select the data type of the Tracking Field.",
                required=False,
                type=Enum(
                    choices=[
                        "NONE",
                        "DATETIME",
                        "STRING",
                        "PUSHID",
                    ],
                ),
                default="NONE",
            ),
            name="collection_parameters",
            display_name="Collection Parameters",
            description="Collection configuration information.",
        ),
        ParameterGroup(
            Parameter(
                name="load_pattern",
                display_name="Load Pattern",
                description="Select the pattern to use when loading the data.",
                type=Enum(
                    choices=[
                        "INSERT",
                        "LOAD_ALL",
                        "TRUNCATE_LOAD_ALL",
                    ]
                ),
                default="INSERT",
            ),
            Parameter(
                name="documentid_field",
                display_name="DocumentId Column",
                description="Map the DocumentId field to this column in the relational database.  Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="date_processed_column",
                display_name="Date Processed Column",
                description="If specified, a date column representing when data was processed will be added to the relational database. Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            name="load_parameters",
            display_name="Load Parameters",
            description="Options for loading data into the relational database.",
        ),
        ParameterGroup(
            Parameter(
                name="column_parameters",
                display_name="Column Parameters",
                description="Details about each column within the relational database.",
                required=True,
                many=True,
                type=Nested(
                    Parameter(
                        name="column_name",
                        display_name="Column Name",
                        description="Specify the name of the column.",
                        type=String(max=128),
                        required=True,
                    ),
                    Parameter(
                        name="column_type",
                        display_name="Column Data Type",
                        description="Select the data type of the column. If type selected is not supported, the closest matching type will be used.",
                        type=Enum(
                            choices=[
                                "VARCHAR",
                                "INTEGER",
                                "BIGINT",
                                "DATETIME",
                                "DATE",
                                "TIME",
                                "TIMESTAMP",
                                "BOOLEAN",
                                "NUMERIC",
                                "FLOAT",
                                "BYTES",
                                "ARRAY",
                                "STRUCT",
                                "GEOGRAPHY",
                                # STRING
                            ]
                        ),
                        required=True,
                    ),
                    Parameter(
                        name="column_config",
                        display_name="Column Configuration",
                        description="Specify a configuration for the column. For example, VARCHAR could be (128), NUMERIC could be (12,2), ARRAY could be <STRING>, STRUCT could be <DATE, STRING>.",
                        type=String(),
                        required=False,
                    ),
                    Parameter(
                        name="json_path",
                        display_name="JSON Path",
                        description="Firebase field to map to the column. For example, ['store']['book']['title'] or store.book.title.",
                        type=String(),
                        required=False,
                    ),
                ),
            )
        ),
        ParameterGroup(
            Parameter(
                name="custom_parameter",
                display_name="Custom Parameters",
                description="Specify each parameter and value in quotes, separated by a colon.  Separate each pair with a comma and enclose all of the pairs in curly braces.",
                type=Code(),
                required=False,
            ),
            name="additional_parameters",
            display_name="Additional Parameters",
            description="Any additional parameters not described above.",
        ),
    ],
)
