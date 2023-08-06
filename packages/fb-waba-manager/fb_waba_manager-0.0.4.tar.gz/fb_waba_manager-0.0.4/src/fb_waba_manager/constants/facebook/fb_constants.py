class FbConstants:

    GRAPH_API_BASE_URL = 'https://graph.facebook.com'

    WABAS_EDGE = 'whatsapp_business_accounts'

    # validate the fields to get (such as status and message throughput)
    WABAS_FIELDS = [
        'verified_name',
        'status',
        'quality_rating',
        'id',
        'display_phone_number',
        'thread_limit_per_day'
    ]

    PHONE_NUMBERS_EDGE = 'phone_numbers'

    MESSAGE_TEMPLATES_EDGE = 'message_templates'
