from app_control import parse_open_close_command

tests = [
    'Open Chrome',
    'Close Chrome',
    'Open VS Code',
    'Close VS Code',
    'Increase volume',
    'Decrease volume',
    'Mute my computer',
    'Unmute my computer',
    'Set volume to 50 percent',
    'Increase brightness',
    'Decrease brightness',
    'Set brightness to 50 percent',
    'Check battery',
    'What is my battery percentage?',
    'Open Downloads',
    'Open Documents',
    'Open Desktop',
    'Open Pictures',
    'Open File Explorer',
    'Find my resume',
    'Find Python files',
    'Create a folder named JarvisTest'
]

for t in tests:
    print(f"[{t}] -> {parse_open_close_command(t)}")
