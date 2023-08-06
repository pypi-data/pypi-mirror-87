configMap = (
    {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {'name': 'the-map'},
        'data': {'altGreeting': 'Good Morning!', 'enableRisky': 'false'}
    },
    {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {'name': 'another-map'},
        'data': {'altGreeting': 'Good Evening!', 'enableRisky': 'true'}
    },
)
