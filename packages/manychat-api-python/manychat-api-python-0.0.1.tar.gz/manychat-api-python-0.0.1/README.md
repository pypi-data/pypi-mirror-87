# ManyChat API Python library

## Installation

Using pip (recommended):

    python3 -m pip install manychat-api-python

Manually:

    python3 setup.py install

## Usage

After installing the library, you need to get the ManyChat API token in the API tab of the settings of your page at manychat.com.
Here are some examples of the library usage with `1234567890123456:1234567890ABCDEFGHIJKLMNOPQRSTUV` API token:

As an instance (recommended):

    import ManyChat
    
    api = ManyChat.API('1234567890123456:1234567890ABCDEFGHIJKLMNOPQRSTUV')
    page_info = api.fb.page.getInfo()

As a singleton:

    import ManyChat
    
    ManyChat.API.init('1234567890123456:1234567890ABCDEFGHIJKLMNOPQRSTUV')
    page_info = ManyChat.API.fb.page.getInfo()

## Documentation

List of available ManyChat API methods you can get at the [ManyChat API homepage](https://api.manychat.com/).
