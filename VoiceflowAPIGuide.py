import requests
import json

# Configuration - Replace these with your actual values
api_key = 'VF.DM.690eb8bacad6447f197bc440.8qEEd1un1cCrHJZe'  # it should look like this: VF.DM.XXXXXXX.XXXXXX... keep this a secret!
projectID = "690e74e30a1a5baa66b1a7ae"
versionID = "690e74e30a1a5baa66b1a7af"

# Global variables
buttons = []

def interact(user_id, request):
    """
    Interact with the Voiceflow Dialog Manager API
    
    Args:
        user_id (str): Unique identifier for the user conversation
        request (dict): The request payload to send to Voiceflow
    
    Returns:
        bool: True if conversation is still running, False if ended
    """
    global buttons
    
    # Initialize buttons if not already initialized
    if 'buttons' not in globals():
        buttons = []
    
    try:
        response = requests.post(
            f'https://general-runtime.voiceflow.com/state/user/{user_id}/interact',
            json={'request': request},
            headers={
                'Authorization': api_key,
                'versionID': 'production'
            },
        )
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        traces = response.json()
        
        # Process each trace in the response
        for trace in traces:
            if trace['type'] == 'text':
                print(trace['payload']['message'])
            elif trace['type'] == "choice":
                buttons = trace['payload']['buttons']
                print("\nChoose one of the following:")
                for i in range(len(buttons)):
                    print(f"{i+1}. {buttons[i]['name']}")
            elif trace['type'] == 'end':
                # An end trace means the Voiceflow dialog has ended
                return False
            else:
                print("Unhandled trace:")
                print(json.dumps(trace, indent=2))
        
        # The dialog is still running
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Voiceflow API: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def save_transcript(user_id):
    """
    Save the conversation transcript using the Voiceflow Transcripts API
    
    Args:
        user_id (str): The session ID (same as user_id) for the conversation
    """
    try:
        url = "https://api.voiceflow.com/v2/transcripts"
        
        payload = {
            "projectID": projectID,
            "versionID": versionID,
            "sessionID": user_id
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": api_key
        }
        
        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"Saved transcript with status code {response.status_code}")
        else:
            print(f"Failed to save transcript. Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error saving transcript: {e}")
    except Exception as e:
        print(f"Unexpected error saving transcript: {e}")

def validate_configuration():
    """
    Validate that the required configuration is set up properly
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if api_key == 'YOUR_API_KEY_HERE' or not api_key:
        print("Error: Please set your Voiceflow API key in the configuration section")
        print("   Your API key should look like: VF.DM.XXXXXXX.XXXXXX...")
        return False
    
    if not api_key.startswith('VF.DM.'):
        print("Error: API key format appears to be incorrect")
        print("   Your API key should start with 'VF.DM.'")
        return False
    
    # For transcript functionality, we need project and version IDs
    if projectID == "YOUR_PROJECT_ID_HERE" or versionID == "YOUR_VERSION_ID_HERE":
        print("Warning: Project ID and Version ID not set. Transcript saving will be disabled.")
        print("   You can still use the basic chat functionality.")
        return "partial"
    
    return True

def main():
    """
    Main function to run the Voiceflow API guide
    """
    print("Voiceflow API Guide - Python Implementation")
    print("=" * 50)
    
    # Validate configuration
    config_status = validate_configuration()
    if config_status == False:
        return
    
    # Get user name for the session
    name = input('\n> What is your name? ')
    if not name.strip():
        name = "anonymous_user"
    
    print(f"\nStarting conversation for user: {name}")
    print("-" * 30)
    
    # Start the conversation with a launch request
    isRunning = interact(name, {'type': 'launch'})
    
    if not isRunning:
        print("Failed to start conversation. Please check your API key and try again.")
        return
    
    # Main conversation loop
    while isRunning:
        try:
            global buttons
            if len(buttons) > 0:
                # Handle button selection
                buttonSelection = input('\n> Choose a button number, or type a reply: ')
                
                # Try to parse as button selection
                try:
                    button_index = int(buttonSelection) - 1
                    if 0 <= button_index < len(buttons):
                        isRunning = interact(name, buttons[button_index]["request"])
                    else:
                        print(f"Invalid button selection. Please choose 1-{len(buttons)}")
                        continue
                except ValueError:
                    # Not a number, treat as text input
                    isRunning = interact(name, {'type': 'text', 'payload': buttonSelection})
                
                # Clear buttons after use
                buttons = []
            else:
                # Handle regular text input
                nextInput = input('\n> Say something: ')
                
                # Handle special commands
                if nextInput.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                isRunning = interact(name, {'type': 'text', 'payload': nextInput})
            
            # Save transcript after each interaction (if configured)
            if config_status == True:  # Full configuration available
                save_transcript(name)
                
        except KeyboardInterrupt:
            print("\n\nConversation interrupted by user.")
            break
        except Exception as e:
            print(f"Error during conversation: {e}")
            break
    
    print("\n" + "=" * 50)
    print("The conversation has ended.")
    print("Thank you for using the Voiceflow API Guide!")

if __name__ == "__main__":
    main()