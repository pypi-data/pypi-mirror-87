import sys

from main import CheckPermissions, PrintFileOperations

if CheckPermissions()[0]:
    print("Currently pending file operations: ")
    PrintFileOperations()
    sys.exit(0)
else:
    print("No read permission on registry key!")
    sys.exit(1)