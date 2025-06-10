import ctypes
import ctypes.wintypes
from pathlib import Path
from uuid import UUID

def get_known_folder(folder_guid_str: str) -> Path:
    """Gets the absolute path to a Windows known folder using its GUID."""
    # Convert the GUID string to a ctypes GUID
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_ulong),
            ("Data2", ctypes.c_ushort),
            ("Data3", ctypes.c_ushort),
            ("Data4", ctypes.c_ubyte * 8)
        ]

        def __init__(self, guid_string):
            uuid = UUID(guid_string)
            self.Data1 = uuid.time_low
            self.Data2 = uuid.time_mid
            self.Data3 = uuid.time_hi_version
            self.Data4 = (ctypes.c_ubyte * 8).from_buffer_copy(uuid.bytes[8:])

    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID),
        ctypes.wintypes.DWORD,
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p)
    ]
    SHGetKnownFolderPath.restype = ctypes.HRESULT

    folder_guid = GUID(folder_guid_str)
    path_ptr = ctypes.c_wchar_p()

    result = SHGetKnownFolderPath(
        ctypes.byref(folder_guid), 0, 0, ctypes.byref(path_ptr)
    )
    if result != 0:
        raise ctypes.WinError(result)

    return Path(path_ptr.value)

# List of common folder GUIDs
KNOWN_FOLDER_IDS = {
    "Downloads": "{374DE290-123F-4565-9164-39C4925E467B}",
    "Documents": "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}",
    "Pictures":  "{33E28130-4E1E-4676-835A-98395C3BC3BB}",
}

# Example usage
if __name__ == "__main__":
    documents_dir = get_known_folder(KNOWN_FOLDER_IDS["Documents"])
    print("Downloads folder:", documents_dir)
