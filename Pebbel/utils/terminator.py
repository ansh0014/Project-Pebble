# from utils.ai_integration import init_ai, ask_groq, clean_response  # Adjust path as needed
# from utils.speak import say

from desktop_use import DesktopUseClient, Locator, ApiError, sleep, ElementResponse
# import other response models or exceptions as needed

client = DesktopUseClient() # connects to default 127.0.0.1:3000
# client = DesktopUseClient(base_url='127.0.0.1:3001') # or specify host:port

def launch_apps():
    try:
        # open windows calculator
        print('opening calculator...')
        client.open_application('calc')
        print('calculator opened.')

        # wait a bit
        sleep(1000)

        # open notepad
        print('opening notepad...')
        client.open_application('notepad')
        print('notepad opened.')

        # open a url
        print('opening url...')
        client.open_url('https://github.com/mediar-ai/terminator')
        print('url opened.')

    except ApiError as e:
        print(f'api error (status: {e.status}): {e}')
    except Exception as e:
        print(f'an unexpected error occurred: {e}')

# launch_apps()

# locate the calculator window (windows 11 example)
calc_window = client.locator('window:Calculator')

# locate the 'seven' button within the calculator window
seven_button = calc_window.locator('role:button').locator('name:Seven')

# locate the main text area in notepad (use accessibility insights tool to find correct class/id)
notepad_editor = client.locator('window:Notepad').locator('role:richedit')

# directly locate the 'eight' button
eight_button = client.locator('window:Calculator').locator('role:button').locator('name:Eight')

def interact_with_calc():
    try:
        print('opening calculator...')
        client.open_application('calc')
        sleep(1500) # give calc time to open

        # locate elements
        calc_window = client.locator('window:Calculator')
        seven = calc_window.locator('role:Button').locator('name:Seven')
        plus = calc_window.locator('role:Button').locator('name:Plus')
        eight = calc_window.locator('role:Button').locator('name:Eight')
        equals = calc_window.locator('role:Button').locator('name:Equals')
        display = calc_window.locator('name:CalculatorResults')

        print('clicking 7...')
        seven.click()
        sleep(200)

        print('clicking +...')
        plus.click()
        sleep(200)

        print('clicking 8...')
        eight.click()
        sleep(200)

        print('clicking =...')
        equals.click()
        sleep(500)

        # get the result
        result = display.get_text()
        print(f'calculation result: {result.text}') # e.g., "display is 15"

    except ApiError as e:
        print(f'api error interacting with calculator: {e}')
    except Exception as e:
        print(f'an unexpected error occurred: {e}')

# interact_with_calc()

def interact_with_notepad():
    try:
        print('opening notepad...')
        client.open_application('notepad')
        sleep(1000)

        editor = client.locator('window:Notepad').locator('role:RichEdit')

        print('typing text...')
        editor.type_text('hello from terminator!\nthis is a python test.')
        sleep(500)

        print('pressing enter...')
        editor.press_key('{Enter}')
        sleep(200)

        editor.type_text('done.')

        content = editor.get_text()
        print(f'notepad content retrieved: {content.text}')

    except ApiError as e:
        print(f'api error interacting with notepad: {e}')
    except Exception as e:
        print(f'an unexpected error occurred: {e}')

# interact_with_notepad()

def check_element_state():
    try:
        client.open_application('calc')
        sleep(1000)
        equals_button = client.locator('window:Calculator').locator('role:Button').locator('Name:Equals')

        visible = equals_button.is_visible()
        print(f'is equals button visible? {visible}')

        attributes = equals_button.get_attributes()
        print(f'equals button attributes: {attributes}') # attributes is a dataclass

        bounds = equals_button.get_bounds()
        print(f'equals button bounds: x={bounds.x}, y={bounds.y}, width={bounds.width}, height={bounds.height}')

    except ApiError as e:
        print(f'api error checking element state: {e}')
    except Exception as e:
        print(f'an unexpected error occurred: {e}')

# check_element_state()

def use_expectations():
    try:
        print('opening notepad...')
        client.open_application('notepad')

        editor_locator = client.locator('window:Notepad').locator('role:RichEdit')

        # wait for the editor element to be visible (default timeout)
        print('waiting for editor to be visible...')
        editor_element: ElementResponse = editor_locator.expect_visible()
        print(f'editor is visible! id: {editor_element.id}')

        # wait for it to be enabled (with a 5-second timeout)
        print('waiting for editor to be enabled...')
        editor_locator.expect_enabled(timeout=5000)
        print('editor is enabled!')

        editor_locator.type_text('initial text.')
        sleep(1000)

        # wait for the text to exactly match 'initial text.'
        print('waiting for text to match...')
        editor_locator.expect_text_equals('initial text.', timeout=3000)
        print('text matched!')

        # this would likely fail and raise ApiError after the timeout
        # print('waiting for incorrect text (will timeout)...')
        # editor_locator.expect_text_equals('wrong text', timeout=2000)

    except ApiError as e:
        print(f'expectation error: {e}')
    except Exception as e:
        print(f'an unexpected error occurred: {e}')

# use_expectations()

try:
    # attempt to find a non-existent element
    non_existent = client.locator('name:DoesNotExist')
    non_existent.click()
except ApiError as e:
    # handle specific api errors (e.g., element not found, timeout)
    print(f'terminator api error (status: {e.status}): {e}')
except ConnectionError as e:
    print(f'connection error: {e}. is the server running?')
except Exception as e:
    # handle other unexpected errors
    print(f'an unexpected python error occurred: {e}')