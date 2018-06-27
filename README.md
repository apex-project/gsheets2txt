# gsheets2txt
Utility to download Google spreadsheet content into txt/csv file. 

- Easily configurable
- Compares differences
- Encodes and deals with encoding errors

The script is useful to collaborate on shared parameters file, keynotes etc. while working in Revit

[Download as .exe for Windows](https://github.com/apex-project/gsheets2txt/releases)

## Settings

Config API access and generate credentials file using this guide http://gspread.readthedocs.io/en/latest/oauth2.html

Set target file path and link to google spreadsheet in `gsheets2txt.ini` (use sample file). Only first sheet of the table will be downloaded.

To provide access to specific table share it to email-address which you use in credentials.json. In case of problems please double check that address appeared in Share settings.

### Default settings. Can be overrided in `gsheets2txt.ini`

```
'output_file_path': '_output.txt'
'separator': '\t'
'line_end': '\t\n',
'google_credentials_path': 'credentials.json'
'google_sheet_url': None
'columns_count': 3
'encoding': 'utf-8'
```

## Extra information

### Scheduled run

If you want to run it scheduled, you should set parent directory.
It is necessary to provide access to correct config and credential files.

### How to compile with pyinstaller

These keys might be useful for compilations
-  --onefile
-  --noconsole
-   -i icon.ico

## Dependencies

The script is based on [gspread](https://github.com/burnash/gspread) python library which designed perfectly and works as magic. Thanks for it!

Icon by Icons8 https://icons8.com/

## Contribution

Feel free to report about bugs to issues tab.
You're also welcome to make any contributions - add comments, fork and make pull-requests. 
