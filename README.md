System for generating static template of smith.edu/libraries.

Fetches a page from the live site, updates includes and paths to be non-relative and not reliant on temporary cached locations.

# To run
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 make-static-template.py
```

# Known issues
Today's Hours ajax request not functioning. This is likely due to incorrect ordering of js includes.
