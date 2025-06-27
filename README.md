## PEAK Steam Launch Metadata Swapper
_Only for windows_
### When to use this
Currently (6/26/2025), when you launch PEAK directly, Steam will automatically use the first launch option for the game, meaning the game will always use Vulkan if launched directly. This causes an issue with mods that use `DX12` to draw on the screen, etc. This simple command-line app will swap the launch options so that when launched directly, it will not append the `-force-vulkan` parameter and use `DX12`.

### How do I use it?
1. Download the latest executable [here](https://github.com/CyR1en/PEAKLaunchSwapper/releases/download/0.1.0/peakls.exe)
2. Once downloaded, open `Windows Terminal`
3. Change directory to `Downloads` (assuming that peakls.exe is in downloads folder)
    ```
    cd Downloads
    ```
4. Swap the launch options using the following command:
    ```
    ./peakls
    ```

Optional:
- Revert to original:
    ```
    ./peakls -r
    ```
- Show current launch config:
    ```
    ./peakls --print-only
    ```



### How does it work?
Currently, the launch configuration for PEAK on Steam is as follows:

`appinfo.vdf` viewed as `json`
```json
{
    "5": {
        "executable": "PEAK.exe",
        "arguments": "-force-vulkan",
        "type": "option1",
        "config": {
            "oslist": "windows",
            "osarch": "64"
        },
        "description_loc": {
            "english": "PEAK using Vulkan"
        },
        "description": "PEAK using Vulkan"
    },
    "6": {
        "executable": "PEAK.exe",
        "type": "option2",
        "config": {
            "oslist": "windows"
        },
        "description_loc": {
            "english": "PEAK using DX12"
        },
        "description": "PEAK using DX12"
    }
}
```
So all I had to do was to swap these two and make it look like this:
```json
{
    "5": {
        "executable": "PEAK.exe",
        "type": "option1",
        "config": {
            "oslist": "windows"
        },
        "description_loc": {
            "english": "PEAK using DX12"
        },
        "description": "PEAK using DX12"
    },
    "6": {
        "executable": "PEAK.exe",
        "arguments": "-force-vulkan",
        "type": "option2",
        "config": {
            "oslist": "windows",
            "osarch": "64"
        },
        "description_loc": {
            "english": "PEAK using Vulkan"
        },
        "description": "PEAK using Vulkan"
    }
}
```
With the launch configuration above, PEAK will now use the `DX12` option to run the game if launched directly.

### Is it safe?
Absolutely! The codebase is open source, so you can see if anything fishy is going on. The executable is automatically built by GitHub, so I personally do not upload it myself from my computer. The changes that this app does can be reverted by using the revert argument or just deleting `appinfo.vdf` (since Steam will generate a fresh one anyway)

If Windows scream that it contains virus, it definitely does not. If you want to use this app, you can add an exception to your anti-virus software.

## Attribution
Thanks to for [tralph3](https://github.com/tralph3) for their amazing module `appinfo.py` for parsing and updating `appinfo.vdf`
