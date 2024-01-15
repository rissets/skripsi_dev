models = {
    'text-gpt-0040-render-sha-0': 'gpt-4',
    'text-gpt-0035-render-sha-0': 'gpt-3.5-turbo',
    'text-gpt-0035-render-sha-0301': 'gpt-3.5-turbo-0314',
    'text-gpt-0040-render-sha-0314': 'gpt-4-0314',
}

special_instructions = {
    'default': [],
    'Magicoder': [
        {
            'role': 'user',
            'content': 'hello'
        },
        {
            'role': 'assistant',
            'content': 'You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.'
        }
    ]
}
