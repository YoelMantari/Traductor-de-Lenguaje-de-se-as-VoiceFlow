import requests
import json
import os
import sys

# Try to import configuration from config.py, fallback to inline config
try:
    from config import API_KEY, PROJECT_ID, VERSION_ID, RUNTIME_ENDPOINT, VERSION_ALIAS
    api_key = API_KEY
    projectID = PROJECT_ID
    versionID = VERSION_ID
    runtime_endpoint = RUNTIME_ENDPOINT
    version_alias = VERSION_ALIAS
except ImportError:
    # Fallback to inline configuration
    api_key = 'YOUR_API_KEY_HERE'  # it should look like this: VF.DM.XXXXXXX.XXXXXX... keep this a secret!
    projectID = "YOUR_PROJECT_ID_HERE"
    versionID = "YOUR_VERSION_ID_HERE"
    runtime_endpoint = "https://general-runtime.voiceflow.com"
    version_alias = "production"

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
    
    try:
        response = requests.post(
            f'{runtime_endpoint}/state/user/{user_id}/interact',
            json={'request': request},
            headers={
                'Authorization': api_key,
                'versionID': version_alias
            },
        )
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        traces = response.json()
        
        # Handle empty response
        if not traces:
            print("No response from Voiceflow. Make sure your agent is published.")
            return False
        
        # Process each trace in the response
        for trace in traces:
            if trace['type'] == 'text':
                print(f"Bot: {trace['payload']['message']}")
            elif trace['type'] == "choice":
                buttons = trace['payload']['buttons']
                print("\nChoose one of the following:")
                for i in range(len(buttons)):
                    print(f"  {i+1}. {buttons[i]['name']}")
            elif trace['type'] == 'visual':
                # Handle images and other visual content
                visual_type = trace['payload'].get('visualType', 'unknown')
                if visual_type == 'image':
                    image_url = trace['payload'].get('image', '')
                    print(f"Image: {image_url}")
                else:
                    print(f"Visual content: {visual_type}")
            elif trace['type'] == 'end':
                # An end trace means the Voiceflow dialog has ended
                print("Conversation ended by Voiceflow")
                return False
            elif trace['type'] == 'path':
                # Path trace - usually can be ignored, just shows navigation
                pass
            else:
                print(f"Unhandled trace type '{trace['type']}':")
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
            print(f"Transcript saved (status: {response.status_code})")
        else:
            print(f"Failed to save transcript (status: {response.status_code})")
            if response.status_code == 401:
                print("   Check your API key authorization")
            elif response.status_code == 400:
                print("   Check your project ID and version ID")
            
    except requests.exceptions.RequestException as e:
        print(f"Error saving transcript: {e}")
    except Exception as e:
        print(f"Unexpected error saving transcript: {e}")

def validate_configuration():
    """
    Validate that the required configuration is set up properly
    
    Returns:
        str: 'valid', 'partial', or 'invalid'
    """
    if api_key == 'YOUR_API_KEY_HERE' or not api_key:
        print("Error: Please set your Voiceflow API key")
        print("   1. Get your API key from: Voiceflow Project > Settings > API Keys")
        print("   2. Either update the config.py file or edit the api_key variable")
        print("   3. Your API key should look like: VF.DM.XXXXXXX.XXXXXX...")
        return 'invalid'
    
    if not api_key.startswith('VF.DM.'):
        print("Error: API key format appears to be incorrect")
        print("   Your API key should start with 'VF.DM.'")
        return 'invalid'
    
    # For transcript functionality, we need project and version IDs
    if projectID == "YOUR_PROJECT_ID_HERE" or versionID == "YOUR_VERSION_ID_HERE":
        print("Warning: Project ID and Version ID not configured")
        print("   - Chat functionality will work")
        print("   - Transcript saving will be disabled")
        print("   - To enable transcripts, set PROJECT_ID and VERSION_ID")
        return 'partial'
    
    return 'valid'

def print_help():
    """Print help information about using the application"""
    print("\n" + "=" * 60)
    print("VOICEFLOW API GUIDE - HELP")
    print("=" * 60)
    print("\nDuring conversation, you can:")
    print("  - Type any message to chat with your Voiceflow agent")
    print("  - When buttons appear, type the number (1, 2, 3...) to select")
    print("  - Type 'quit', 'exit', or 'bye' to end the conversation")
    print("  - Press Ctrl+C to force quit")
    print("\nSetup Instructions:")
    print("  1. Get your API key from Voiceflow Project > Settings > API Keys")
    print("  2. Create a 'config.py' file from 'config_template.py'")
    print("  3. Update config.py with your actual API key")
    print("  4. Publish your Voiceflow project")
    print("  5. Run this script!")
    print("\n" + "=" * 60)

def main():
    """
    Main function to run the Voiceflow API guide
    """
    print("Voiceflow API Guide - Python Implementation")
    print("=" * 60)
    
    # Check for help argument
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print_help()
        return
    
    # Validate configuration
    config_status = validate_configuration()
    if config_status == 'invalid':
        print("\nTip: Run 'python VoiceflowAPIGuide.py --help' for setup instructions")
        return
    
    # Get user name for the session
    print(f"\nAPI Key: {api_key[:15]}..." + "*" * 20)
    print(f"Runtime: {runtime_endpoint}")
    print(f"Version: {version_alias}")
    
    name = input('\nWhat is your name? ').strip()
    if not name:
        name = "anonymous_user"
    
    print(f"\nStarting conversation for: {name}")
    print("-" * 40)
    
    # Start the conversation with a launch request
    isRunning = interact(name, {'type': 'launch'})
    
    if not isRunning:
        print("\nFailed to start conversation.")
        print("   - Check that your API key is correct")
        print("   - Make sure your Voiceflow project is published")
        print("   - Verify your internet connection")
        return
    
    # Main conversation loop
    conversation_count = 0
    while isRunning:
        try:
            conversation_count += 1
            
            if len(buttons) > 0:
                # Handle button selection
                user_input = input('\nChoose button number or type message: ').strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                # Try to parse as button selection
                try:
                    button_index = int(user_input) - 1
                    if 0 <= button_index < len(buttons):
                        print(f"Selected: {buttons[button_index]['name']}")
                        isRunning = interact(name, buttons[button_index]["request"])
                    else:
                        print(f"Invalid button selection. Please choose 1-{len(buttons)}")
                        continue
                except ValueError:
                    # Not a number, treat as text input
                    isRunning = interact(name, {'type': 'text', 'payload': user_input})
                
                # Clear buttons after use
                buttons = []
            else:
                # Handle regular text input
                user_input = input('\nYou: ').strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif not user_input:
                    print("Please enter a message or 'quit' to exit")
                    continue
                
                isRunning = interact(name, {'type': 'text', 'payload': user_input})
            
            # Save transcript after each interaction (if configured)
            if config_status == 'valid':
                save_transcript(name)
                
        except KeyboardInterrupt:
            print("\n\nConversation interrupted by user.")
            break
        except Exception as e:
            print(f"Error during conversation: {e}")
            print("Continuing conversation...")
            continue
    
    print("\n" + "=" * 60)
    print(f"Conversation Summary:")
    print(f"   - User: {name}")
    print(f"   - Interactions: {conversation_count}")
    print(f"   - Transcripts saved: {'Yes' if config_status == 'valid' else 'No'}")
    print("\nThank you for using the Voiceflow API Guide!")

if __name__ == "__main__":
    main()