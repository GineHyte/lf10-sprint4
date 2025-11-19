from app.schemas.credit import Credit

__credits = [
    {
        "number": 1,
        "global_stages": [
            {
                "id": "online_form",
                "status": "done",
                "text": "Sie haben das Formular online ausgefüllt",
            },
            {
                "id": "documents",
                "status": "pending",
                "text": "Wird bei unserer Seite bearbeitet",
            },
            {"id": "tests", "status": "none", "text": ""},
            {"id": "security", "status": "none", "text": ""},
            {"id": "final_decision", "status": "none", "text": ""},
        ],
        "online_form_stages": [],
        "created_at": "2025-11-03 10:00",
        "updated_at": "2025-11-03 12:00",
    },
    {
        "number": 2,
        "global_stages": [
            {
                "id": "online_form",
                "status": "done",
                "text": "Sie haben das Formular online ausgefüllt",
            },
            {
                "id": "documents",
                "status": "pending",
                "text": "Wird bei unserer Seite bearbeitet",
            },
            {"id": "tests", "status": "none", "text": ""},
            {"id": "security", "status": "none", "text": ""},
            {"id": "final_decision", "status": "none", "text": ""},
        ],
        "online_form_stages": [],
        "created_at": "2025-11-03 10:00",
        "updated_at": "2025-11-03 12:00",
    },
    {
        "number": 3,
        "global_stages": [
            {
                "id": "online_form",
                "status": "pending",
                "text": "Das Folmular wird bearbeitet",
            },
            {"id": "documents", "status": "none", "text": ""},
            {"id": "tests", "status": "none", "text": ""},
            {"id": "security", "status": "none", "text": ""},
            {"id": "final_decision", "status": "none", "text": ""},
        ],
        "online_form_stages": [
            {
                "id": "credit_format",
                "status": "done",
                "text": "Hier sollen Sie den Kreditantragsformular auswählen.",
                "title": "Kreditantragsformular",
                "data": {"credit_format": "INSTANT_CREDIT"},
            },
            {
                "id": "personal_data",
                "status": "done",
                "text": "Hier werden pesonbezogene Daten abgefragt.",
                "title": "Personenbezogene Daten",
                "data": {
                    "first_name": "Oleksii",
                    "last_name": "Petrenko",
                    "street": "Amerika Str.",
                    "house_number": "15",
                    "zip": "49681",
                    "city": "Garrel",
                    "business_phone": "(04474) 50519-0",
                    "personal_phone": "+49 1234567891011",
                    "email": "o.petrenko@example.com",
                    "birthday": 1763132391,
                    "homeland": "Ukraine",
                },
            },
        ],
        "created_at": "2025-11-03 10:00",
        "updated_at": "2025-11-03 12:00",
    },
    {
        "number": 4,
        "global_stages": [
            {
                "id": "online_form",
                "status": "done",
                "text": "Sie haben das Formular online ausgefüllt",
            },
            {
                "id": "documents",
                "status": "done",
                "text": "Ihre Dokumente wurden genehmigt",
            },
            {"id": "tests", "status": "done", "text": "Alle Tests wurden bestanden"},
            {
                "id": "security",
                "status": "done",
                "text": "Sicherheitsprüfung bestanden",
            },
            {"id": "final_decision", "status": "done", "text": "Kredit genehmigt"},
        ],
        "online_form_stages": [
            {
                "id": "credit_format",
                "status": "done",
                "text": "Hier sollen Sie den Kreditantragsformular auswählen.",
                "title": "Kreditantragsformular",
                "data": {"credit_format": "INSTANT_CREDIT"},
            },
            {
                "id": "personal_data",
                "status": "done",
                "text": "Hier werden pesonbezogene Daten abgefragt.",
                "title": "Personenbezogene Daten",
                "data": {
                    "first_name": "Oleksii",
                    "last_name": "Petrenko",
                    "street": "Amerika Str.",
                    "house_number": "15",
                    "zip": "49681",
                    "city": "Garrel",
                    "business_phone": "(04474) 50519-0",
                    "personal_phone": "+49 1234567891011",
                    "email": "o.petrenko@example.com",
                    "birthday": 1763132391,
                    "homeland": "Ukraine",
                },
            },
        ],
        "created_at": "2025-11-03 10:00",
        "updated_at": "2025-11-03 12:00",
    },
]


credits = list(map(lambda credit: Credit.model_validate(credit), __credits))
